# Generated by Django 3.1.7 on 2021-04-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Person', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personmodel',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='personmodel',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'NotKnown')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='personmodel',
            name='last_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='personmodel',
            name='patronymic_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='personmodel',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='personmodel',
            name='place_of_death',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
