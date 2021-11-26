# Generated by Django 3.1.5 on 2021-10-09 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('A', 'Await'), ('ACC', 'Accepted'), ('REJ', 'Rejected'), ('END', 'End')], default='A', max_length=3),
        ),
    ]