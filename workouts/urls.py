from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name="starting-page"),
    path('movements', views.MovementsView.as_view(), name="movements"),
    path('movements/<int:id>', views.MovementDetailView.as_view(), name="movement-detail"),
    path('movements/<int:id>/delete', views.movement_delete, name="movement-delete"),
    path('workouts', views.WorkoutsView.as_view(), name="workouts"),
    path('workouts/<int:id>', views.WorkoutDetailView.as_view(),
         name="workout-detail"),
    path('workouts/<int:id>/phase/<int:phase_id>', views.PhaseDetailView.as_view(),
         name="phase-detail"),
    path('workouts/<int:id>/phase/<int:phase_id>/<int:setgroup_id>/newset', views.PhaseDetailView.new_set,
         name="phase-detail-newset"),
    path('workouts/<int:id>/newphase', views.WorkoutDetailView.new_phase,
         name="workout-newphase"),
    path('workouts/<int:id>/delete', views.workout_delete, name="workout-delete"),
    path('set/<int:id>/delete', views.set_delete, name="set-delete"),
    path('phase<int:id>/delete', views.phase_delete, name="phase-delete"),
    path('phase<int:id>/move<int:amount>', views.phase_move, name="phase-move"),
    path('users/', views.UsersView.as_view(), name="users"),
]

