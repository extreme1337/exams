# Generated by Django 3.2.5 on 2021-07-19 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_alter_question_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='school.exam'),
        ),
    ]
