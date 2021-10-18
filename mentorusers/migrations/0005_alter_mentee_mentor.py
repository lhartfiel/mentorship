# Generated by Django 3.2.7 on 2021-10-18 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentorusers', '0004_alter_mentor_mentor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentee',
            name='mentor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mentors', to='mentorusers.mentor'),
        ),
    ]
