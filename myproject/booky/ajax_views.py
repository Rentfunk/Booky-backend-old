from django.db.models import Sum
from django.http import QueryDict, JsonResponse

from .filters import OrderFilter, BookFilter
from .models import Order, Book

import json


def OrderFilterView(request):
    orders = Order.objects.annotate(sum_grades=Sum("forBook__forGrades__name")).order_by("sum_grades", "forBook__title")

    data = json.loads(request.body)
    qdData = QueryDict("", mutable=True)
    qdData.update(data)

    orderFilter = OrderFilter(qdData, queryset=orders)
    orders = orderFilter.qs

    filteredOrderPks = [order.pk for order in orders]

    return JsonResponse(filteredOrderPks, safe=False)


def BookFilterView(request):
    books = Book.objects.annotate(sum_grades=Sum("forGrades__name")).order_by("sum_grades", "title")

    data = json.loads(request.body)
    qdData = QueryDict("", mutable=True)
    qdData.update(data)

    bookFilter = BookFilter(qdData, queryset=books)
    books = bookFilter.qs

    filteredBookPks = [book.pk for book in books]

    return JsonResponse(filteredBookPks, safe=False)
