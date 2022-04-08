from tkinter import CASCADE
from unicodedata import name
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    email_address = models.EmailField()
    username = models.CharField(max_length=50)
    #gym
    #country
    #birth date


class Block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocks")


class Movement(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class BlockMovement(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE)
    # weight = models.FloatField('weight')


"""

class Session(models.Model):
    pass
"""



class Workout(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    movement = models.ForeignKey(
        Movement, on_delete=models.CASCADE, related_name="workouts")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("workout-detail", kwargs={"id": self.pk})
    
    def save(self, *args, **kwargs):
        phases = self.phases.all().order_by("order")

        i = 0
        for phase in phases:
            phase.order = i
            phase.save()
            i += 2 # increment in two to make reordering easy
        
        super().save(*args, **kwargs)
    
# Group of sets
class SetGroup(models.Model):
    pass

class Set(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    set_group = models.ForeignKey(
        SetGroup, on_delete=models.CASCADE, related_name="sets")
    
    RPE = 'RPE'
    PERCENTAGE = 'PER'
    INTENSITY_CHOICES = [
        (RPE, 'RPE'),
        (PERCENTAGE, 'Percentage'),
    ]

    intensity_type = models.CharField(
        max_length=3, choices=INTENSITY_CHOICES, default=PERCENTAGE)

    percentage = models.DecimalField(max_digits=3, decimal_places=0, default=70, validators=PERCENTAGE_VALIDATOR)
    rpe = models.IntegerField('RPE', null=True, default=80)
    sets = models.IntegerField('Sets', null=True, default=4)
    reps = models.IntegerField('Reps', null=True, default=5) 

class Phase(models.Model):
    name = models.CharField(max_length=100, blank=True)
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="phases")
    setgroup = models.OneToOneField(SetGroup, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, blank=False, null=False)

    def get_absolute_url(self):
        return reverse("phase-detail", kwargs={"id": self.workout.id, 
                                               "phase_id": self.pk})
    
    def __str__(self):
        order = int((self.order/2)+1)
        name = f"Phase {order}"
        if len(self.name)>0:
            name += f" - {self.name}"

        return name
    
    def move(self, amount):
        self.order += amount*3
        self.save()
        self.workout.save()

