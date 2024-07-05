from django.db import models

# Create your models here.

class Risks(models.Model):
    risk_type = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.risk_type

class Questions(models.Model):
    risks = models.ForeignKey(Risks, null=True, on_delete=models.SET_NULL)
    question_text = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.question_text

class Answers(models.Model):
    questions = models.ForeignKey(Questions, null=True, on_delete=models.SET_NULL)
    answer_text = models.CharField(max_length=200, null=True)
    prob_happen = models.FloatField(null=True, verbose_name="Probability of Happening")
    prob_nothappen = models.FloatField(null=True, verbose_name="Probability of Not Happening")

    def __str__(self):
        return self.answer_text

class UserResponses(models.Model):
    questions = models.ForeignKey(Questions, null=True, on_delete=models.SET_NULL)
    answers = models.ForeignKey(Answers, null=True, on_delete=models.SET_NULL)
    response_date = models.DateTimeField(auto_now_add=True, null=True)
    risks = models.ForeignKey(Risks,null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Response to {self.questions} - {self.answers}"


