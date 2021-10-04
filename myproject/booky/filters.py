import django_filters

from .models import Book, Order


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "authors": ["icontains"],
        }
        exclude = ("forGrades",)

    def __init__(self, *args, **kwargs):
        super(BookFilter, self).__init__(*args, **kwargs)
        self.filters["title__icontains"].label = "Názov"
        self.filters["authors__icontains"].label = "Autori"

        for key in self.filters.keys():
            self.filters[key].field.widget.attrs.update({"class": "input-style"})


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            "forBook__title": ["icontains"],
            "code": ["icontains"],
            "isbn": ["icontains"],
            "registryNumber": ["icontains"],
            "billingNumber": ["icontains"],
            "amountOrdered": ["gt", "lt"],
            "pricePerBook": ["gt", "lt"],
            "publicationYear": ["gte", "lt"],
            # "dateOrdered": ["contains"]
        }
        exclude = ("booksLost",)

    def __init__(self, *args, **kwargs):
        super(OrderFilter, self).__init__(*args, **kwargs)
        self.filters["forBook__title__icontains"].label = "Kniha"
        self.filters["code__icontains"].label = "Kód"
        self.filters["isbn__icontains"].label = "ISBN"
        self.filters["registryNumber__icontains"].label = "Evidenčné číslo"
        self.filters["billingNumber__icontains"].label = "Fakturačné číslo"
        self.filters["amountOrdered__gt"].label = "Počet kusov väčší ako"
        self.filters["amountOrdered__lt"].label = "Počet kusov menší ako"
        self.filters["pricePerBook__gt"].label = "Cena za kus väčšia ako"
        self.filters["pricePerBook__lt"].label = "Cena za kus menšia ako"
        self.filters["publicationYear__gte"].label = "Od roku"
        self.filters["publicationYear__lt"].label = "do roku"
        # self.filters["dateOrdered"].label = "Dátum prijatia"

        for key in self.filters.keys():
            self.filters[key].field.widget.attrs.update({"class": "input-style"})
