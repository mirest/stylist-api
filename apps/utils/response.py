from django.http import HttpResponse
import json


def Response(data):
    try:
        response = json.dumps(data)
        return HttpResponse(response, content_type="application/json")
    except:
        return HttpResponse(json.dumps({"error": "invalid json response"}), content_type="application/json")
