from django.urls import path
from . import views

# URLConfig
urlpatterns = [
    path('', views.FramesetFormPage, name="frameset"),
    path('Results/<str:pk>/', views.ResultsPage, name="results"),
    path('CheckedList/', views.CheckedListPage, name="current_answers"),
    path('Questionnaire/', views.QuestionnairePage, name="questionnaire"),
    path('delete-response/<int:pk>/', views.delete_response, name='delete_response'),
    path('sink-form/', views.sink_form_view, name='sink_form'),
    path('collision-form/', views.collision_form_view, name='collision_form'),
    path('explosion-form/', views.explosion_form_view, name='explosion_form'),
    path('grounding-form/', views.grounding_form_view, name='grounding_form'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('hello/', views.say_hello, name="hello"),
]
