# Generated by Django 3.0.3 on 2020-11-23 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='질문'),
        ),
    ]
