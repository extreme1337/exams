# Generated by Django 3.2.5 on 2021-07-21 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_alter_exam_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='nuber_of_questions',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]
