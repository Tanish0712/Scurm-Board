from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH


class Project(models.Model):
    Projectname = models.CharField(max_length=50, null=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='creator', null=True
    )
    code = models.CharField(max_length=6, null=False, default="passwd")
    user_profile = models.ManyToManyField(User)
    description = models.CharField(max_length= 50, null=True)


    def __str__(self):
        return self.Projectname


Status_CHOICES = (
    ('Todo','Todo'),
    ('In progress', 'In progress'),
    ('Done','Done'),
)
class ScurmBoard(models.Model):
    Task_name = models.CharField(max_length= 50)
    Task_Description = models.CharField(max_length = 500)
    Dead_line = models.DateField()
    status = models.CharField(max_length=20, choices= Status_CHOICES, default= 'Todo' )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)

