# Generated by Django 2.2.7 on 2019-12-20 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagement', '0006_delete_drafts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drafts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskId', models.CharField(max_length=10)),
                ('taskName', models.CharField(max_length=70)),
                ('taskDescription', models.TextField()),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('createdBy', models.CharField(max_length=30)),
                ('assignedTo', models.CharField(max_length=30)),
                ('lastModifiedDate', models.DateTimeField(auto_now_add=True)),
                ('lastModifiedBy', models.CharField(max_length=30)),
                ('remarks', models.TextField()),
                ('status', models.ForeignKey(default=1, on_delete='', to='TaskManagement.Status')),
            ],
        ),
    ]