# Generated by Django 4.0.1 on 2023-03-06 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Код верификации'),
        ),
    ]
