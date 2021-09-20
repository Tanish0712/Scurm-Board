# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Project, ScurmBoard


"""
    Hooks up the models to view them at admin panel.
"""
admin.site.register(Project)
admin.site.register(ScurmBoard)


