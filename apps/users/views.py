import json

import urllib3
from django.http import HttpResponse
from django.views.generic import CreateView, View

from apps.utils.response import Response


class GoogleLoginSignupView(View):

    def post(self, request, *args, **kwargs):
        data=json.loads(request.body)
        user_token=data.get('google_token')
        url = f'https://oauth2.googleapis.com/tokeninfo?id_token={user_token}'
        http = urllib3.PoolManager()
        response = http.request("GET", url,headers={'Content-Type': 'application/json'})
        if response.status==200:
            user_data=json.loads(response.data)
            return Response(user_data)

        return Response({"message": "invalid id token", "status_code": response.status})
