# Generated by Django 3.2.5 on 2021-07-29 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_student_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='student', serialize=False, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
