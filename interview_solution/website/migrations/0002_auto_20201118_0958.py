# Generated by Django 3.0.3 on 2020-11-18 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='student',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='report',
            name='share',
            field=models.BooleanField(default=False, verbose_name='공유'),
        ),
    ]
