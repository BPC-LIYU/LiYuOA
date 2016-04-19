#coding=utf-8
from django.shortcuts import render

# Create your views here.
from liyu_organization.models import Organization

query_set = Organization.objects.filter()

l = []
