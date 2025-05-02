from .periodic import periodic
from django.http import JsonResponse
# test endpoint


def test_endpoint(request):
    periodic()
   
    return JsonResponse({"msg": "Done"})



