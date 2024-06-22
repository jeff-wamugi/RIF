from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

# Create your views here.
from .forms import CreateUserForm, SinkForm, CollisionForm, ExplosionForm, GroundingForm


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
            squestion1 = data['question1']
            print(data['question2'])
            print(data['question3'])
            print(data['question4'])
            print(data['question5'])
            # Do something with the data
            return render(request, 'CheckedList.html', {'form_data': form_data, 'risk_type':risk_type})
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
            print(data['question1'])
            print(data['question2'])
            # Do something with the data
            return render(request, 'CheckedList.html', {'form_data': form_data, 'risk_type': risk_type})
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
            print(data['question1'])
            print(data['question2'])
            # Do something with the data
            return render(request, 'CheckedList.html', {'form_data': form_data, 'risk_type': risk_type})
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
            print(data['question1'])
            print(data['question2'])
            # Do something with the data
            return render(request, 'CheckedList.html', {'form_data': form_data, 'risk_type': risk_type})
    else:
        form = GroundingForm()
    return render(request, 'grounding_form.html', {'form': form})

def CheckedListPage(request):
    return render(request, 'CheckedList.html')


def ResultsPage(request):
    return render(request, 'Results.html')




