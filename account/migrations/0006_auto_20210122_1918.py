# Generated by Django 3.1.5 on 2021-01-22 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20210122_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='confirmationcode',
            name='exp_date',
            field=models.BooleanField(default=False),
        ),
    ]
