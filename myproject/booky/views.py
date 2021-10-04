from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from .models import Grade, Book, Order, Classroom, Teacher, OwnedByClass, OwnedByTeacher
from .forms import PreBookForm, BookForm, OrderForm, OwnedByTeacherForm, OwnedByTeacherFormSet, OwnedByClassForm, \
    OwnedByClassFormSet, TeacherForm
from .filters import BookFilter, OrderFilter

from django.forms import modelformset_factory

from django.db.models import Sum


# Index
def index(request):
    return render(request, "booky/index.html")


# Lists

def BooksListView(request):
    books = Book.objects.annotate(sum_grades=Sum("forGrades__name")).order_by("sum_grades", "title")

    myFilter = BookFilter()

    context = {"books": books, "myFilter": myFilter}
    return render(request, "booky/books.html", context)


def OrdersListView(request):
    orders = Order.objects.annotate(sum_grades=Sum("forBook__forGrades__name")).order_by("sum_grades", "forBook__title")

    myFilter = OrderFilter()

    context = {"orders": orders, "myFilter": myFilter}
    return render(request, "booky/orders.html", context)


def GradesListView(request):
    grades = Grade.objects.order_by("name")

    context = {"grades": grades}
    return render(request, "booky/base.html", context)


def ClassroomsView(request, pk):
    grade = Grade.objects.get(pk=pk)
    classrooms = Classroom.objects.filter(grade__pk=pk)
    booksInClass = OwnedByClass.objects.filter(classroom__grade__pk=pk)
    gradeBooksPKs = booksInClass.values_list("book", flat="True").distinct()

    classroomInfo = {}

    for distinctBookPK in gradeBooksPKs:
        title = Book.objects.get(pk=distinctBookPK).title
        classroomInfo[title] = booksInClass.filter(book__pk=distinctBookPK)

    context = {"classroomInfo": classroomInfo,
               "classrooms": classrooms,
               "grade": grade}

    return render(request, "booky/classrooms.html", context)


class TeachersListView(ListView):
    template_name = "booky/teachers.html"
    context_object_name = "teachers"

    def get_queryset(self):
        return Teacher.objects.order_by('name')


# Add forms
def addOrderStep0(request):
    preBookForm = PreBookForm(request.POST or None)

    if request.method == "POST":
        if preBookForm.is_valid():
            request.session["typeOfOrder"] = request.POST["typeOfOrder"]
            return redirect("add-order-step-1")

    context = {"preBookForm": preBookForm}

    return render(request, "booky/add_order_step_0.html", context)


def addOrderStep1(request):
    if request.session.get("typeOfOrder") == "nb":
        bookForm = BookForm(request.POST or None)
    else:
        bookForm = BookForm(request.POST or None, queryset=Book.objects.order_by("title"))

    orderForm = OrderForm(request.POST or None)

    if request.method == "POST":
        if bookForm.is_valid() and orderForm.is_valid():

            if request.session.get("typeOfOrder") == "nb":
                newBook = bookForm.save()
                newOrder = orderForm.save(commit=False)

                newOrder.forBook = newBook
                newOrder.save()
            else:
                newOrder = orderForm.save(commit=False)
                newOrder.forBook = Book.objects.get(pk=bookForm.data.get("book"))
                newOrder.save()

            if "save" in request.POST:
                return redirect("orders-list")
            else:
                return redirect("add-order-step-0")

    context = {"bookForm": bookForm,
               "orderForm": orderForm,
               "newBook": request.session.get("typeOfOrder") == "nb"}

    return render(request, "booky/add_order_step_1.html", context)


def addTeacher(request):
    teacherForm = TeacherForm(request.POST or None)

    if request.method == "POST":
        if teacherForm.is_valid():
            teacherForm.save()
            return redirect("add-new-book-for-teacher", Teacher.objects.get(name=teacherForm.cleaned_data["name"]).pk)

    context = {"teacherForm": teacherForm}

    return render(request, "booky/add_teacher.html", context)


def addNewBookForTeacher(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    bookChoices = Book.objects.exclude(pk__in=teacher.bookInfo.all()
                                       .values_list("book", flat="True"))
    ownedByTeacherForm = OwnedByTeacherForm(bookChoices, request.POST or None)

    if request.method == "POST":
        if ownedByTeacherForm.is_valid():

            newObj = OwnedByTeacher(book=Book.objects.get(pk=request.POST["book"]),
                                    booksOwned=request.POST["booksOwned"],
                                    booksReturned=request.POST["booksReturned"],
                                    teacher=teacher)
            newObj.save()
            if "save" in request.POST:
                return redirect("teachers-list")
            else:
                return redirect("add-new-book-for-teacher", pk)

    context = {"form": ownedByTeacherForm, "teacher": teacher.name}

    return render(request, "booky/add_new_book_for_teacher.html", context)


def addNewBookForGrade(request, pk):
    grade = Grade.objects.get(pk=pk)
    classrooms = Classroom.objects.filter(grade=grade)
    bookChoices = Book.objects.exclude(pk__in=classrooms[0].bookInfo.all()
                                       .values_list("book", flat="True"))
    ownedByClassForm = OwnedByClassForm(bookChoices, classrooms, request.POST or None)

    if request.method == "POST":
        print(request.POST)
        if ownedByClassForm.is_valid():

            for classroom in classrooms:
                newObj = OwnedByClass(book=Book.objects.get(pk=request.POST["book"]),
                                      booksOwned=request.POST["booksOwned_{}".format(classroom.name)],
                                      booksReturned=request.POST["booksReturned_{}".format(classroom.name)],
                                      classroom=classroom)
                newObj.save()
            if "save" in request.POST:
                return redirect("classroom-list", pk)
            else:
                return redirect("add-new-book-for-grade", pk)

    context = {"form": ownedByClassForm}

    return render(request, "booky/add_new_book_for_grade.html", context)


# Edit forms
def editClass(request, pk):
    classroom = Classroom.objects.get(pk=pk)
    books = classroom.bookInfo.all()
    gradePK = classroom.grade.pk
    OwnedByClassFormset = modelformset_factory(OwnedByClass,
                                               form=OwnedByClassFormSet,
                                               extra=0,
                                               labels={"booksOwned": "Priradené", "booksReturned": "Vrátené"})

    ownedByClassFormset = OwnedByClassFormset(queryset=books)

    if request.method == "POST":
        editedClass = OwnedByClassFormset(request.POST)
        if editedClass.is_valid():
            editedClass.save()
            return redirect("classroom-list", gradePK)

    context = {"formset": ownedByClassFormset, "classroom": classroom}

    return render(request, "booky/edit_grade.html", context)


def editTeacher(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    bookChoices = Book.objects.exclude(pk__in=teacher.bookInfo.all()
                                       .values_list("book", flat="True"))
    books = teacher.bookInfo.all()

    OwnedByTeacherFormset = modelformset_factory(OwnedByTeacher,
                                                 form=OwnedByTeacherFormSet,
                                                 fields=("booksOwned", "booksReturned"),
                                                 extra=0,
                                                 labels={"booksOwned": "Priradené", "booksReturned": "Vrátené"})
    ownedByTeacherFormset = OwnedByTeacherFormset(request.POST or None, queryset=books)

    if request.method == "POST":
        if ownedByTeacherFormset.is_valid():
            ownedByTeacherFormset.save()
            return redirect("teachers-list")

    context = {"formset": ownedByTeacherFormset, "pk": pk, "newBooks": len(bookChoices), "teacher": teacher}

    return render(request, "booky/edit_teacher.html", context)


def editOrder(request, pk):
    order = Order.objects.get(pk=pk)

    orderForm = OrderForm(request.POST or None, instance=order)

    if request.method == "POST":
        if orderForm.is_valid():
            orderForm.save()
            return redirect("orders-list")

    context = {"orderForm": orderForm}

    return render(request, "booky/edit_order.html", context)


# Delete forms

def deleteOrder(request, pk):
    order = Order.objects.get(pk=pk)

    orderForm = OrderForm(request.POST or None, instance=order)

    if request.method == "POST":
        if orderForm.is_valid():
            if "save" in request.POST:
                if Order.objects.filter(forBook=Book.objects.get(pk=order.forBook_id)).count() == 1:
                    Book.objects.get(pk=order.forBook_id).delete()
                order.delete()
            return redirect("orders-list")

    context = {"orderForm": orderForm}

    return render(request, "booky/delete_order.html", context)


def deleteTeacherBook(request, pk):
    ownedByTeacherBook = OwnedByTeacher.objects.get(pk=pk)
    teacher = ownedByTeacherBook.teacher
    book = Book.objects.get(pk=ownedByTeacherBook.book_id)

    if request.method == "POST":
        if "save" in request.POST:
            ownedByTeacherBook.delete()
        return redirect("edit-teacher", teacher.pk)

    context = {"ownedByTeacherBook": ownedByTeacherBook, "book": book}

    return render(request, "booky/delete_teacher_book.html", context)
