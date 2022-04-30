from django.db import models
# Create your models here.
from django.contrib.auth.models import User

# basic details of job giver and job seeker.
class Applications(models.Model):
    #username password FirstName from User model.
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # one to one with user model
    contact_no = models.IntegerField(default=0)
    type = models.CharField(max_length=10, null=False, choices=(("JobGiver", "JG"), ("JobSeeker", "JS")))

    def __str__(self):
        return str(self.contact_no)

# to store previous work images if any .
class Images(models.Model):
    connect = models.ForeignKey(Applications, on_delete=models.CASCADE, null=True)
    image = models.FileField(null=True) # file field will store in media folder.


#Type Of Work and photo to display on main screen home screen.
class WorkType(models.Model):
    TypeOfWork = models.CharField(max_length=50, null=False)
    photo = models.FileField(null=True)
    def __str__(self):
        return self.TypeOfWork

class Work(models.Model):
    work_id = models.ForeignKey(WorkType, null=False, on_delete=models.CASCADE) # one to many relation
    Hours = models.IntegerField(default=0)
    Description = models.CharField(max_length=200, null= False)
    Wages = models.IntegerField(default=0)
    Count = models.IntegerField(default=0) # number of applications.
    city = models.CharField(max_length=255) # extend .
    approved = models.BooleanField(default=False)
    # userid = models.ForeignKey(Applications, null=True, on_delete=models.SET_NULL)  # to detect who applied for job.


class ManyToManyRelation(models.Model):
    userid = models.ForeignKey(Applications, null=True, on_delete=models.SET_NULL)
    workid = models.ForeignKey(Work, null=True, on_delete=models.SET_NULL)


