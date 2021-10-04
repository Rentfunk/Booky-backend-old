from .models import Grade


def add_var_to_context(request):
    return {
        "grades": Grade.objects.order_by("name"),
    }
