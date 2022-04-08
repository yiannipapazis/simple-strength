from django import forms


from .models import User, Workout, Movement, SetGroup, Set, Phase

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        exclude = []

class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        exclude = []

class SetGroupForm(forms.ModelForm):
    class Meta:
        model = SetGroup
        exclude = ['movement']

class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        exclude = ['set_group']

class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase
        exclude = ['workout', 'setgroup']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []