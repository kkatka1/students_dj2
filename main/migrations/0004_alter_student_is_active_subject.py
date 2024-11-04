# Generated by Django 5.1.1 on 2024-11-01 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_student_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='учится'),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student', verbose_name='студент')),
            ],
            options={
                'verbose_name': 'предмет',
                'verbose_name_plural': 'предметы',
            },
        ),
    ]
