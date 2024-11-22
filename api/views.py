from django.http import JsonResponse
from django.core import serializers
from core.models import Citizen

def get_citizens(request):
    citizens = Citizen.objects.all()
    serialized_citizens = serializers.serialize('json', citizens)
    return JsonResponse(serialized_citizens, safe=False)