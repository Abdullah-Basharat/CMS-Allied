# Generated by Django 5.2 on 2025-05-03 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_remove_adminprofile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherprofile',
            name='class_assiging_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='class_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_classes', to='User.schoolclass'),
        ),
    ]
