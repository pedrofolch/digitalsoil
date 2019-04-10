from django.http import JsonResponse


def analytics_view(request):
    context = {
        'views': 10
    }
    return JsonResponse(context)
