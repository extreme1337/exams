# Generated by Django 3.2.5 on 2021-07-20 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0003_alter_exam_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to=settings.AUTH_USER_MODEL),
        ),
    ]
