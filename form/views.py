from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

# Create your views here.
from .forms import *
from .models import *
from django.db.models import F


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
    # Query to get userresponses_id, response_time, and risk_type for all records, sorted by response_date in descending order
    queryset = UserResponses.objects.select_related('questions__risks').values(
        'id', 'response_date', 'questions__risks__risk_type'
    ).annotate(
        userresponses_id=F('id'),
        response_time=F('response_date'),
        risk_type=F('questions__risks__risk_type')
    ).values('userresponses_id', 'response_time', 'risk_type').order_by('-response_time')

    # Pagination
    paginator = Paginator(queryset, 5)  # Show 5 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'hello.html', {'risk_records': page_obj})

@login_required(login_url='login')
def ResultsPage(request, pk):
    # Get the UserResponse instance
    user_response = get_object_or_404(UserResponses, id=pk)

    # Get all the related questions and answers
    responses = UserResponses.objects.filter(id=pk).select_related('questions', 'answers')

    # Collect detailed information for each response
    records = []
    for response in responses:
        records.append({
            'question': response.questions.question_text,
            'answer': response.answers.answer_text,
            'prob_happen': response.answers.prob_happen,
            'prob_nothappen': response.answers.prob_nothappen,
        })

    context = {
        'user_response': user_response,
        'records': records,
    }
    return render(request, 'Results.html', context)

def delete_response(request, pk):
    response = get_object_or_404(UserResponses, id=pk)
    response.delete()
    messages.success(request, 'Record deleted successfully!')
    return redirect('hello')

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

            messages.success(request, 'Success: Data submitted to a Safety Engineer! ')
            return render(request, 'CheckedList.html', {
                'form_data': form_data,
                'risk_type': risk_type,
                'like_prob': like_prob,
                'unlike_prob': unlike_prob,
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

            messages.success(request, 'Success: Data submitted to a Safety Engineer! ')

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

            messages.success(request, 'Success: Data submitted to a Safety Engineer! ')

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

            messages.success(request, 'Success: Data submitted to a Safety Engineer! ')

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


