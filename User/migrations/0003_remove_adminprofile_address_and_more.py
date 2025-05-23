# Generated by Django 5.2 on 2025-05-03 15:28

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_rename_student_id_studentprofile_roll_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminprofile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='adminprofile',
            name='designation',
        ),
        migrations.RemoveField(
            model_name='adminprofile',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='gender',
        ),
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='admin_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='admin_students', to='User.adminprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adminprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='roll_no',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_classes', to='User.adminprofile')),
            ],
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='student_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='User.schoolclass'),
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=20, unique=True)),
                ('specialization', models.CharField(max_length=100)),
                ('hire_date', models.DateField(default=datetime.datetime.now)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_teachers', to='User.adminprofile')),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_classes', to='User.schoolclass')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='TecherProfile',
        ),
    ]
