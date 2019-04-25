from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template


class GoogleLoginSignupView(View):

    def get(self, request, *args, **kwargs):
        t = get_template('google.html')
        html = t.render()
        return HttpResponse(html)
