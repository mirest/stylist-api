import json

import urllib3
from django.http import HttpResponse
from django.views.generic import CreateView, View
from django.shortcuts import render
from django.template.loader import get_template



class GoogleLoginSignupView(View):

    def get(self, request, *args, **kwargs):
        t = get_template('google.html')
        html = t.render()
        return HttpResponse(html)
