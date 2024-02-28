# Generated by Django 4.2.2 on 2023-07-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_availablecolors_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availablecolors',
            old_name='name',
            new_name='name_EN',
        ),
        migrations.RemoveField(
            model_name='availablecolors',
            name='color',
        ),
        migrations.AddField(
            model_name='availablecolors',
            name='hexcolor',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]
