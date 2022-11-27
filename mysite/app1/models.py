"""Schema Definition"""
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# basic details of job giver and job seeker.
class Applications(models.Model):
    """Basic Details Of User"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # one to one with user model
    contact_no = models.IntegerField(default=0)
    type = models.CharField(
        max_length=10, null=False, choices=(("JobGiver", "JG"), ("JobSeeker", "JS"))
    )
    users_state = models.CharField(max_length=255, null=True)
    users_dist = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.contact_no)


# to store previous work images if any .
class Images(models.Model):
    """Stores USer Uploaded Files"""
    connect = models.ForeignKey(Applications, on_delete=models.CASCADE, null=True)
    image = models.FileField(null=True)  # file field will store in media folder.


class WorkType(models.Model):
    """Type Of Work and photo to display on main screen home screen"""
    TypeOfWork = models.CharField(max_length=50, null=False)
    photo = models.FileField(null=True)

    def __str__(self):
        return str(self.TypeOfWork)


class Work(models.Model):
    """Details About Work"""
    work_id = models.ForeignKey(
        WorkType, null=False, on_delete=models.CASCADE
    )  # one to many relation
    Hours = models.IntegerField(default=0)
    Description = models.CharField(max_length=200, null=False)
    Wages = models.IntegerField(default=0)
    Count = models.IntegerField(default=0)  # number of applications.
    city = models.CharField(max_length=255)  # extend .
    state = models.CharField(max_length=255, null=True)  # state
    district = models.CharField(max_length=255, null=True)  # district
    approved = models.BooleanField(default=False)


class ManyToManyRelation(models.Model):
    """Relation Between User And Work"""
    userid = models.ForeignKey(Applications, null=True, on_delete=models.SET_NULL)
    workid = models.ForeignKey(Work, null=True, on_delete=models.SET_NULL)
