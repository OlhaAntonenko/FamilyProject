# Generated by Django 3.1.7 on 2021-04-24 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('Person', '0011_auto_20210424_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserModel',
        ),
    ]
