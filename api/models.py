from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class RegisterUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.first_name
        


#model for the todo task
class Tasks(models.Model):
    todo = models.TextField()
    completed = models.BooleanField(default=True)

    def __str__(self):
        return self.todo