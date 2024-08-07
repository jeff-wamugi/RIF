# Generated by Django 5.0.6 on 2024-07-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0004_alter_answers_prob_happen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='prob_happen',
            field=models.FloatField(null=True, verbose_name='Probability of Happening'),
        ),
        migrations.AlterField(
            model_name='answers',
            name='prob_nothappen',
            field=models.FloatField(null=True, verbose_name='Probability of Not Happening'),
        ),
    ]
