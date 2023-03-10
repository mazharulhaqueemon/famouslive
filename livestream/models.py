from django.db import models

class ActiveCall(models.Model):
    action = models.CharField(max_length=255, blank=True, null=True)
    uid = models.CharField(max_length=255,null=True)
    full_name = models.CharField(max_length=255,null=True)
    profile_image = models.CharField(max_length=255,null=True)
    call_type = models.CharField(max_length=255,null=True)
    muted = models.BooleanField()
    video_disabled = models.BooleanField()
    datetime = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.call_type})"

class ActiveCalls(models.Model):
    active_calls = models.ManyToManyField(ActiveCall)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.active_calls.count()} Active Calls"


# Create your models here.


# Create your models here.
