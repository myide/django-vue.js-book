# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,Group

class Book(models.Model):
    name = models.CharField(max_length = 64)
    price = models.IntegerField()
    note = models.TextField()
    user = models.ManyToManyField(User, null=True, blank=True)
    group = models.ManyToManyField(Group, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-id']

