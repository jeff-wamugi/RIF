# Generated by Django 5.0.6 on 2024-07-05 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0005_alter_answers_prob_happen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponses',
            name='risks',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form.risks'),
        ),
    ]
