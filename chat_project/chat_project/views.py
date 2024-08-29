from django.http import JsonResponse


def server_status(request):
    return JsonResponse({"status": "Server is running"})
