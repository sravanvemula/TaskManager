# Generated by Django 2.2.7 on 2019-12-20 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagement', '0004_auto_20191219_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drafts',
            fields=[
                ('tasks_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TaskManagement.Tasks')),
            ],
            bases=('TaskManagement.tasks',),
        ),
    ]
