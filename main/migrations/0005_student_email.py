# Generated by Django 5.1.1 on 2024-11-04 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_student_is_active_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='email'),
        ),
    ]