from pickle import FALSE
import datetime
from django.db import models
from relays.models import *

# Create your models here.

class Triggers(models.Model):
    LOGIC_OR = 'OR'
    LOGIC_AND = 'AND'
    CHILD_MODE_CHOICES = {
        (LOGIC_OR,'Logic OR'),
        (LOGIC_AND,'Logic AND')
    }

    parent_id = models.ForeignKey('self',null=True,on_delete=models.CASCADE)
    child_modes = models.CharField(
        max_length=3,
        choices=CHILD_MODE_CHOICES,
        default=LOGIC_OR,
        )
    name = models.CharField(max_length=20,blank=True,null=True)
    description = models.TextField(max_length=300,blank=True,null=True)
    active = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['parent_id','name','description','child_modes','active']

    def getTriggerChildsIds(self):
        res = []
        table_Triggers_ids = Triggers.objects.filter(parent_id=self.id)
        for trig_id in table_Triggers_ids:
            res.append(trig_id)
        return res
        

    def isfulfilled(self):
        if self.child_modes == self.LOGIC_OR:
            return self.isfulfilledOR()
        elif self.child_modes == self.LOGIC_AND:
            return self.isfulfilledAND()

    
    def isfulfilledOR(self):
        res = False
        # Triggers
        # table_Triggers = self.isfulfilled_Triggers()
        # for trig_Trig in table_Triggers:
        #     res |= trig_Trig
        # Users
        table_Users = self.isfulfilled_Users()
        for trig_User in table_Users:
            res |= trig_User
        # TimeTriggers
        table_Times = self.isfulfilled_Times()
        for trig_Time in table_Times:
            res |= trig_Time
        return res

    def isfulfilledAND(self):
        res = True
        # Triggers
        # table_Triggers = self.isfulfilled_Triggers()
        # for trig_Trig in table_Triggers:
        #     res &= trig_Trig
        # Users
        table_Users = self.isfulfilled_Users()
        for trig_User in table_Users:
            res &= trig_User
        # TimeTriggers
        table_Times = self.isfulfilled_Times()
        for trig_Time in table_Times:
            res &= trig_Time
        return res

    def isfulfilled_Triggers(self):
        res = []
        try:
            childs_User = Triggers.objects.filter(parent_id = self.id)
            for child_User in childs_User:
                res.append(child_User.isfulfilled())
        except Triggers.DoesNotExist:
            None
        return res 

    def isfulfilled_Users(self):
        res = []
        try:
            childs_User = UserTriggers.objects.filter(trigger_id = self.id)
            for child_User in childs_User:
                res.append(child_User.isfulfilled())
        except UserTriggers.DoesNotExist:
            None
        return res

    def isfulfilled_Times(self):
        res = []
        try:
            childs_User = TimeTriggers.objects.filter(trigger_id = self.id)
            for child_Time in childs_User:
                res.append(child_Time.isfulfilled())
        except TimeTriggers.DoesNotExist:
            None
        return res



class UserTriggers(models.Model):
    trigger_id = models.ForeignKey('Triggers',on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    def isfulfilled(self):
        if self.state == True:
            return True
        else:
            return False

class TimeTriggers(models.Model):
    trigger_id = models.ForeignKey('Triggers',on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now=False)
    end_time = models.TimeField(auto_now=False)

    def isfulfilled(self):
        current_time = datetime.datetime.now().time()
        if self.start_time > self.end_time:
            if self.start_time <=current_time or self.end_time >= current_time:
                return True
            else:
                return False
        else:    
            if self.start_time <= current_time <= self.end_time:
                return True
            else:
                return False

class WeeklyTriggers(models.Model):
    trigger_id = models.ForeignKey('Triggers',on_delete=models.CASCADE)

class RelayTriggers(models.Model):
    FORCE_ON = 'ON'
    FORCE_OFF = 'OFF'
    FORCE_NONE = 'None'
    FORCE_MODES = {
        (FORCE_ON,'Force ON'),
        (FORCE_OFF,'Force OFF'),
        (FORCE_NONE,'None'),
    }
    force_state = models.CharField(
        max_length=4,
        choices=FORCE_MODES,
        default=FORCE_NONE,
        null=True
        )
    trigger_id = models.ForeignKey('Triggers',on_delete=models.CASCADE,null=True)
    relay_id = models.ForeignKey('relays.RelayDevices',on_delete=models.CASCADE)
    bus = models.IntegerField(default = None, null=True)

    def isfulfilled(self):
        res = False
        try:
            requested_trigger = Triggers.objects.get(id=self.trigger_id.id)
            res = requested_trigger.isfulfilled()
        except (Triggers.DoesNotExist) as err:
            None
            # print(err)
        if self.force_state == self.FORCE_ON:
            res = True
        elif self.force_state == self.FORCE_OFF:
            res = False
        return res

