# Generated by Django 4.0.1 on 2022-03-18 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0005_block_rename_email_address_user_email_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='rpe',
            field=models.IntegerField(default=80, null=True, verbose_name='RPE'),
        ),
    ]
