from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

# Create your views here.
from .forms import *
from .models import *


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('hello')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
            return redirect('login')

        context = {'form':form}
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('hello')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('hello')
            else:
                messages.info(request, 'Username or Password is Incorrect')

        context = {}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def say_hello(request):
    # Pull data from db
    # Transform
    # Send email
    return render(request, 'hello.html')

def FramesetFormPage(request):
    return render(request, 'FramesetForm.html')

def QuestionnairePage(request):
    return render(request, 'questionnaire.html')

def sink_form_view(request):
    if request.method == 'POST':
        form = SinkForm(request.POST)
        if form.is_valid():
            form_data = form.get_labels_and_data()
            risk_type = 'Sinking'
            # Process form data
            data = form.cleaned_data
            # Access individual inputs
            # Define the probabilities for each question
            probabilities = {
                'question1': 0.25,
                'question2': 0.15,
                'question3': 0.1,
                'question4': 0.2,
                'question5': 0.3
            }

            # Calculate the sum of probabilities for each "yes" answer
            total_probability = 0
            for question, prob in probabilities.items():
                answer = data[question]
                if question == 'question3':
                    if answer == 'no':
                        total_probability += prob
                    else:
                        total_probability -= 0.0  # Assign 0.1 for any choice other than 'yes' for question 3
                else:
                    if answer == 'yes':
                        total_probability += prob


            # Cap the total_probability to 1.0
            total_probability = min(total_probability, 1.0)
            # The overall probability of sinking happening
            like_prob = int(total_probability * 100)
            # The probability of sinking not happening
            unlike_prob = int(100 - like_prob)

            # Save responses to the database
            risk_instance, created = Risks.objects.get_or_create(risk_type=risk_type)
            for field_name, answer in data.items():
                question_instance, created = Questions.objects.get_or_create(risks=risk_instance,
                                                                             question_text=form.fields[
                                                                                 field_name].label)
                answer_instance, created = Answers.objects.get_or_create(questions=question_instance,
                                                                         answer_text=answer,
                                                                         prob_happen=like_prob,
                                                                         prob_nothappen=unlike_prob)

            UserResponses.objects.create(questions=question_instance, answers=answer_instance)

            messages.success(request, 'Database updated! ')
            return render(request, 'CheckedList.html', {
                'form_data': form_data,
                'risk_type': risk_type,
                'like_prob': like_prob,
                'unlike_prob': unlike_prob
            })
    else:
        form = SinkForm()
    return render(request, 'sink_form.html', {'form': form})

def collision_form_view(request):
    if request.method == 'POST':
        form = CollisionForm(request.POST)
        if form.is_valid():
            form_data = form.get_labels_and_data()
            risk_type = 'Collision'
            data = form.cleaned_data
            # Access individual inputs
            # Define the probabilities for each question
            probabilities = {
                'question1': 0.2,
                'question2': 0.15,
                'question3': 0.1,
                'question4': 0.2,
                'question5': 0.15
            }

            # Calculate the sum of probabilities for each "yes" answer
            total_probability = 0
            for question, prob in probabilities.items():
                answer = data[question]
                if (question == 'question1') or (question == 'question2') or (question == 'question5'):
                    if answer == 'no':
                        total_probability += prob
                    else:
                        total_probability -= 0.0  # Assign 0.1 for any choice other than 'yes' for question 3
                else:
                    if answer == 'yes':
                        total_probability += prob

            # The overall probability of sinking happening
            like_prob = int((total_probability/0.8) * 100)
            # The probability of sinking not happening
            unlike_prob = int(100 - like_prob)

            # Save responses to the database
            risk_instance, created = Risks.objects.get_or_create(risk_type=risk_type)
            for field_name, answer in data.items():
                question_instance, created = Questions.objects.get_or_create(risks=risk_instance,
                                                                             question_text=form.fields[
                                                                                 field_name].label)
                answer_instance, created = Answers.objects.get_or_create(questions=question_instance,
                                                                         answer_text=answer,
                                                                         prob_happen=like_prob,
                                                                         prob_nothappen=unlike_prob)
                UserResponses.objects.create(questions=question_instance, answers=answer_instance)

            messages.success(request, 'Database updated! ')

            return render(request, 'CheckedList.html', {
                'form_data': form_data,
                'risk_type': risk_type,
                'like_prob': like_prob,
                'unlike_prob': unlike_prob
            })
    else:
        form = CollisionForm()
    return render(request, 'collision_form.html', {'form': form})

def explosion_form_view(request):
    if request.method == 'POST':
        form = ExplosionForm(request.POST)
        if form.is_valid():
            form_data = form.get_labels_and_data()
            risk_type = 'Explosion'
            data = form.cleaned_data
            # Access individual inputs
            # Define the probabilities for each question
            probabilities = {
                'question1': 0.2,
                'question2': 0.15,
                'question3': 0.1,
                'question4': 0.15,
                'question5': 0.2
            }

            # Calculate the sum of probabilities for each "yes" answer
            total_probability = 0
            for question, prob in probabilities.items():
                answer = data[question]
                if (question == 'question1') or (question == 'question2'):
                    if answer == 'no':
                        total_probability += prob
                    else:
                        total_probability -= 0.0  # Assign 0.1 for any choice other than 'yes' for question 3
                else:
                    if answer == 'yes':
                        total_probability += prob

            # The overall probability of sinking happening
            like_prob = int((total_probability/0.8) * 100)
            # The probability of sinking not happening
            unlike_prob = int(100 - like_prob)

            # Save responses to the database
            risk_instance, created = Risks.objects.get_or_create(risk_type=risk_type)
            for field_name, answer in data.items():
                question_instance, created = Questions.objects.get_or_create(risks=risk_instance,
                                                                             question_text=form.fields[
                                                                                 field_name].label)
                answer_instance, created = Answers.objects.get_or_create(questions=question_instance,
                                                                         answer_text=answer,
                                                                         prob_happen=like_prob,
                                                                         prob_nothappen=unlike_prob)
                UserResponses.objects.create(questions=question_instance, answers=answer_instance)

            messages.success(request, 'Database updated! ')

            return render(request, 'CheckedList.html', {
                'form_data': form_data,
                'risk_type': risk_type,
                'like_prob': like_prob,
                'unlike_prob': unlike_prob
            })
    else:
        form = ExplosionForm()
    return render(request, 'explosion_form.html', {'form': form})

def grounding_form_view(request):
    if request.method == 'POST':
        form = GroundingForm(request.POST)
        if form.is_valid():
            form_data = form.get_labels_and_data()
            risk_type = 'Grounding'
            data = form.cleaned_data
            # Access individual inputs
            # Define the probabilities for each question
            probabilities = {
                'question1': 0.2,
                'question2': 0.15,
                'question3': 0.1,
                'question4': 0.2,
                'question5': 0.15
            }

            # Calculate the sum of probabilities for each "yes" answer
            total_probability = 0
            for question, prob in probabilities.items():
                answer = data[question]
                if (question == 'question1') or (question == 'question5'):
                    if answer == 'no':
                        total_probability += prob
                    else:
                        total_probability -= 0.0  # Assign 0.1 for any choice other than 'yes' for question 3
                else:
                    if answer == 'yes':
                        total_probability += prob

            # The overall probability of sinking happening
            like_prob = int((total_probability/0.8) * 100)
            # The probability of sinking not happening
            unlike_prob = int(100 - like_prob)

            # Save responses to the database
            risk_instance, created = Risks.objects.get_or_create(risk_type=risk_type)
            for field_name, answer in data.items():
                question_instance, created = Questions.objects.get_or_create(risks=risk_instance,
                                                                             question_text=form.fields[
                                                                                 field_name].label)
                answer_instance, created = Answers.objects.get_or_create(questions=question_instance,
                                                                         answer_text=answer,
                                                                         prob_happen=like_prob,
                                                                         prob_nothappen=unlike_prob)
                UserResponses.objects.create(questions=question_instance, answers=answer_instance)

            messages.success(request, 'Database updated! ')

            return render(request, 'CheckedList.html', {
                'form_data': form_data,
                'risk_type': risk_type,
                'like_prob': like_prob,
                'unlike_prob': unlike_prob
            })
    else:
        form = GroundingForm()
    return render(request, 'grounding_form.html', {'form': form})

def CheckedListPage(request):
    return render(request, 'CheckedList.html')


def ResultsPage(request):
    return render(request, 'Results.html')