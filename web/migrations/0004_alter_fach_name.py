# Generated by Django 4.1.2 on 2022-10-16 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_alter_fach_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fach',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]