# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-19 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20170816_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithm',
            name='auto_add',
            field=models.BooleanField(default=True, help_text='Omogućiti kako bi se novi registrirani korisnici automatski dodali u listu korisnika s pristupom.', verbose_name='automatski pristup korisnicima'),
        ),
        migrations.AlterField(
            model_name='algorithm',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Neaktivan algoritam se neće prikazivati kao opcija korisnicima.', verbose_name='aktivno'),
        ),
    ]