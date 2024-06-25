from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SinkForm(forms.Form):
    QUESTION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe'),
        ('skip', 'Skip')
    ]

    question1 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the vessel appear to be carrying more passengers or cargo than usual?"
    )
    question2 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the crew seem inexperienced or untrained in handling the vessel?"
    )
    question3 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Were the enough life-saving devices on the vessel?"
    )
    question4 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the vessel set sail despite bad weather conditions or overloading?"
    )
    question5 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the vessel appear unstable, especially in rough sea conditions?"
    )

    def get_labels_and_data(self):
        return {field.name: {'label': field.label, 'value': self.cleaned_data[field.name]} for field in self}

class CollisionForm(forms.Form):
    QUESTION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe'),
        ('skip', 'Skip')
    ]

    question1 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the vessel follow proper navigation rules (COLREGs)?"
    )
    question2 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the crew handle navigation confidently?"
    )
    question3 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Were there any communication issues between the vessel and others?"
    )
    question4 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Was the vessel moving at a high speed in a crowded area or low-invisibility conditions?"
    )
    question5 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Was there a proper lookout posted during the journey?"
    )
    def get_labels_and_data(self):
        return {field.name: {'label': field.label, 'value': self.cleaned_data[field.name]} for field in self}

class ExplosionForm(forms.Form):
    QUESTION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe'),
        ('skip', 'Skip')
    ]

    question1 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did you notice any fire extinguishers or fire suppression systems on board?"
    )
    question2 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the crew seem prepared to handle a fire emergency?"
    )
    question3 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Were there any visible signs of poor electrical maintenance, like exposed wires?"
    )
    question4 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did you notice any hazardous materials stored improperly? "
    )
    question5 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Were there any visible violations of safety regulations?"
    )
    def get_labels_and_data(self):
        return {field.name: {'label': field.label, 'value': self.cleaned_data[field.name]} for field in self}

class GroundingForm(forms.Form):
    QUESTION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe'),
        ('skip', 'Skip')
    ]

    question1 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the crew regularly check the depth and positioning?"
    )
    question2 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the vessel come very close to the shore or any underwater hazards?"
    )
    question3 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Was the vessel mostly on autopilot without much monitering?"
    )
    question4 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the vessel show any signs of propulsion or steering issues?"
    )
    question5 = forms.ChoiceField(
        choices=QUESTION_CHOICES,
        widget=forms.RadioSelect,
        label="Did the journey seem well planned and navigated according to charts?"
    )
    def get_labels_and_data(self):
        return {field.name: {'label': field.label, 'value': self.cleaned_data[field.name]} for field in self}






