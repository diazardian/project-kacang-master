# Generated by Django 3.2.5 on 2021-08-04 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kacang', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmember_discord',
            name='id_discord',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
