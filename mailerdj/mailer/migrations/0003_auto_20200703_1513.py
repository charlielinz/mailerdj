# Generated by Django 3.0.8 on 2020-07-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0002_emailcontent_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcontent',
            name='body',
            field=models.TextField(max_length=200),
        ),
    ]
