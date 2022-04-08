from msilib.schema import ListView
from multiprocessing import get_context
from django.shortcuts import render, get_object_or_404, redirect
from .models import Phase, SetGroup, Workout, Movement, Set, User
from .forms import SetForm, WorkoutForm, MovementForm, SetGroupForm, SetForm, PhaseForm, SetGroup, UserForm
from django.views.generic import ListView
from django.views import View
from django.urls import reverse


# Create your views here.

class StartingPageView(View):
    def get(self, request):
        context = {
        }
        return render(request, "workouts/index.html", context)

class WorkoutsView(View):

    @staticmethod
    def get_context():
        context = {
            "workout_form": WorkoutForm,
            "workouts": Workout.objects.all
        }
        return context

    def get(self, request):
        context = self.get_context()
        return render(request, "workouts/workouts.html", context)
    
    def post(self,request):
        workout_form = WorkoutForm(request.POST)

        if workout_form.is_valid():
            workout_form.save()

        context = self.get_context()
        return render(request, "workouts/workouts.html", context)

class MovementsView(View):
    def get(self, request):
        context = self.get_context()
        return render(request, "workouts/movements.html", context)

    def get_context(self):
        context = {
            "movement_form": MovementForm,
            "movements": Movement.objects.all
        }
        return context
    def post(self,request):
        movement_form = MovementForm(request.POST)

        if movement_form.is_valid():
            movement_form.save()
        context = self.get_context()
        return render(request, "workouts/movements.html", context)

class WorkoutDetailView(View):
    def get_context(self, id):
        workout = Workout.objects.get(pk=id)
        setgroup_form = SetGroupForm
        phase_form = PhaseForm
        phases = workout.phases.all().order_by("order")
        context = {
            "workout": workout,
            "setgroup_form": setgroup_form,
            "set_form": SetForm,
            "phase_form": phase_form,
            "phases": phases
        }
        return context
    
    def get(self, request, id):
        context = self.get_context(id)
        return render(request, "workouts/workout-detail.html", context)

    def new_phase(request, id):
        workout = get_object_or_404(Workout, pk=id)
        setgroup = SetGroup()
        setgroup.save()
        phase_form = PhaseForm(request.POST)
        if phase_form.is_valid():
            phase = phase_form.save(commit=False)
            phase.setgroup = setgroup
            phase.workout = workout
            phase.save()
        return redirect(reverse('workout-detail', args=[id]))


class PhaseDetailView(View):
    def get(self, request, id, phase_id):
        phase = Phase.objects.get(pk=phase_id)
        setgroup = phase.setgroup
        context = {
            "workout": Workout.objects.get(pk=id),
            "phase": phase,
            "setform": SetForm,
            "setgroup": setgroup,
            "sets": setgroup.sets.all()
        }
        return render(request, "workouts/phase-detail.html", context)
    
    def new_set(request, id, phase_id, setgroup_id):
        if request.method == 'POST':
            setgroup = get_object_or_404(SetGroup, pk=setgroup_id)
            set_form = SetForm(request.POST)
            if set_form.is_valid():
                set = set_form.save(commit=False)
                set.set_group = setgroup
                set.save()
        return redirect(reverse('phase-detail', args=[id, phase_id]))
                

        

class MovementDetailView(View):
    def get_context(self, id):
        movement = Movement.objects.get(pk=id)
        context = {
            "movement": movement,
            "workouts": movement.workouts.all()
        }
        return context

    def get(self, request, id):
        context = self.get_context(id)
        return render(request, "workouts/movement-detail.html", context)

def movement_delete(request, id):
    movement = get_object_or_404(Movement, pk=id)
    
    if request.method == 'POST':
        movement.delete()

    return render(request, 'workouts/workout-detail.html', {'id': id})

def workout_delete(request, id):
    workout = get_object_or_404(Workout, pk=id)

    if request.method == 'POST':
        workout.delete()
        return redirect(reverse('workouts'))

    return render(request, 'workouts/workout-detail.html', {'id': id})


def set_delete(request, id):
    set = get_object_or_404(Set, pk=id)
    if request.method == 'POST':
        set.delete()
    return redirect(set.set_group.phase.get_absolute_url())

def phase_delete(request, id):
    phase = get_object_or_404(Phase, pk=id)
    if request.method == 'POST':
        phase.delete()
    return redirect(phase.workout.get_absolute_url())

def phase_move(request, id, amount):
    phase = get_object_or_404(Phase, pk=id)
    if request.method == 'POST':
        phase.move(amount)
    return redirect(phase.workout.get_absolute_url())


class UsersView(View):
    
    def get_context(self):
        context = {
            "users": User.objects.all,
            "user_form": UserForm
        }
        return context
    def get(self, request):
        context = self.get_context()
        return render(request, "workouts/users.html", context)

    def post(self, request):
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user_form.save()

        context = self.get_context()
        return render(request, "workouts/users.html", context)
