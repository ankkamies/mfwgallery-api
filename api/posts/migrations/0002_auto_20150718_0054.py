# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='url',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='file',
            field=models.ImageField(upload_to='images', null=True),
        ),
    ]
