# Generated by Django 3.0.8 on 2020-07-07 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0014_auto_20200707_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='book',
            field=models.FileField(upload_to='library'),
        ),
    ]
