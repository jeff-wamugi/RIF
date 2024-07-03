# Generated by Django 5.0.6 on 2024-07-03 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=200, null=True)),
                ('prob_happen', models.FloatField(null=True)),
                ('prob_nothappen', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]