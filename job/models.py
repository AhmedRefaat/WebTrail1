from django.db import models

JOB_TYPE = (
    ('FULL TIME', 'FULL TIME'),
    ('PART TIME', 'PART TIME'),
)

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=100)
    job_type = models.CharField(max_length=15, choices=JOB_TYPE)
    description = models.TextField(max_length=1000)
    published_at = models.DateTimeField(auto_now=True)
    Vacancy = models.IntegerField(default=1)
    salary = models.IntegerField(default=0)
    experience = models.IntegerField(default=1)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name