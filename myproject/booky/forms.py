from django import forms
from .models import Grade, Order, Book, OwnedByTeacher, OwnedByClass, Teacher


class PreBookForm(forms.Form):
    CHOICES = [
        ("nb", "Nová kniha"),
        ("eb", "Existujúca kniha")
    ]

    typeOfOrder = forms.ChoiceField(
        choices=CHOICES,
        label="Nová/existujúca kniha",
        widget=forms.RadioSelect(attrs={"class": "list-style-none"}))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ("forBook", "booksLost")
        labels = {
            "code": "Kód",
            "isbn": "ISBN",
            "publicationYear": "Rok vydania",
            "registryNumber": "Evidenčné číslo",
            "billingNumber": "Fakturačné číslo",
            "amountOrdered": "Počet kusov",
            "pricePerBook": "Cena za kus",
            "dateOrdered": "Dátum zaevidovania"
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({
                "class": "input-style"
            })


class BookForm(forms.ModelForm):
    forGrades = forms.ModelMultipleChoiceField(
        required=False,
        label="Ročníky",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "list-style-none"}),
        queryset=Grade.objects.all())

    class Meta:
        model = Book

        fields = ("forGrades", "title", "authors")
        labels = {
            "title": "Názov učebnice",
            "authors": "Autori"
        }
        help_texts = {
            "authors": "Odďeľujte mená autorov čirakou."
        }

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset", None)
        super(BookForm, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({
                "class": "input-style"
            })

        self.fields["forGrades"].widget.attrs = {key: value for key, value in
                                                 self.fields["forGrades"].widget.attrs.items() if
                                                 value != "input-style"}

        if self.queryset:
            self.fields.clear()

            self.fields["book"] = forms.ModelChoiceField(queryset=self.queryset, label="Kniha")
            self.fields["book"].widget.attrs.update({
                "class": "input-style"
            })


class OwnedByTeacherForm(forms.ModelForm):
    bookChoices = None
    book = forms.ModelChoiceField(queryset=bookChoices, label="Kniha")

    class Meta:
        model = OwnedByTeacher
        fields = ("book", "booksOwned", "booksReturned")
        exclude = ("teacher",)
        labels = {
            "book": "Kniha",
            "booksOwned": "Priradené",
            "booksReturned": "Odovzdané"
        }

    def __init__(self, bookChoices, *args, **kwargs):
        self.bookChoices = bookChoices
        super(OwnedByTeacherForm, self).__init__(*args, **kwargs)
        self.fields["book"].queryset = self.bookChoices

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({
                "class": "input-style"
            })


class OwnedByTeacherFormSet(forms.ModelForm):
    class Meta:
        model: OwnedByTeacher

    def __init__(self, *args, **kwargs):
        super(OwnedByTeacherFormSet, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({
                "class": "input-style"
            })


class OwnedByClassForm(forms.Form):
    bookChoices = None
    book = forms.ModelChoiceField(queryset=bookChoices, label="Kniha")

    def __init__(self, bookChoices, classrooms, *args, **kwargs):

        self.bookChoices = bookChoices
        super(OwnedByClassForm, self).__init__(*args, **kwargs)
        self.fields["book"].queryset = self.bookChoices

        for classroom in classrooms:
            hiddenInput = "hiddenInput_" + classroom.name
            booksOwned = "booksOwned_" + classroom.name
            booksReturned = "booksReturned_" + classroom.name
            '''self.fields[hiddenInput] = forms.CharField()
            self.fields[hiddenInput].label = classroom.name
            self.fields[hiddenInput].required = False'''
            self.fields[booksOwned] = forms.IntegerField(label=("Priradené {}".format(classroom.name)))
            self.fields[booksOwned].initial = "0"
            self.fields[booksReturned] = forms.IntegerField(label=("Vrátené {}".format(classroom.name)))
            self.fields[booksReturned].initial = "0"

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({
                "class": "input-style"
            })


class OwnedByClassFormSet(forms.ModelForm):
    class Meta:
        model: OwnedByClass
        fields = ("booksOwned", "booksReturned")

    def __init__(self, *args, **kwargs):
        super(OwnedByClassFormSet, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({
                "class": "input-style"
            })

        print(self.fields)


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-style"})
        }
        labels = {
            "name": "Meno učiteľa"
        }
