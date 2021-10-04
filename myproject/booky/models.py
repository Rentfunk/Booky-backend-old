from django.db import models
import datetime


class Grade(models.Model):
    name = models.CharField(max_length=11)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=30)
    authors = models.CharField(max_length=70)
    forGrades = models.ManyToManyField(Grade, related_name='books')

    @property
    def given(self):
        teachers = self.teacherInfo.all()
        students = self.classInfo.all()
        givenToTeacher = sum([t.booksOwned for t in teachers])
        givenToStudent = sum([s.booksOwned for s in students])

        return {'TEACHERS': givenToTeacher, 'STUDENTS': givenToStudent}

    @property
    def returned(self):
        teachers = self.teacherInfo.all()
        students = self.classInfo.all()
        returnedFromTeacher = sum([t.booksReturned for t in teachers])
        returnedFromStudent = sum([s.booksReturned for s in students])

        return {'TEACHERS': returnedFromTeacher,
                'STUDENTS': returnedFromStudent}

    @property
    def amountInTotal(self):
        bookOrders = self.orders.all()
        return (sum([order.amount for order in bookOrders]))

    @property
    def amountInStock(self):
        return (self.amountInTotal
                - sum(self.given.values())
                + sum(self.returned.values()))

    @property
    def amountLost(self):
        bookOrders = self.orders.all()
        return sum([order.booksLost for order in bookOrders])

    @property
    def gradesStr(self):
        """
        Converts names of MtM relationship map to string
        ex: [Obj1,Obj2,Obj3] -> "1,2,3"
        """
        names = ""
        for grade in self.forGrades.all():
            names += grade.name + ", "
        return names[:-2]

    def __str__(self):
        return self.title


class Teacher(models.Model):
    books = models.ManyToManyField(Book,
                                   through='OwnedByTeacher',
                                   related_name='teachers')

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class OwnedByTeacher(models.Model):
    teacher = models.ForeignKey(Teacher,
                                on_delete=models.CASCADE,
                                related_name='bookInfo')
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name='teacherInfo')

    booksOwned = models.PositiveSmallIntegerField(default=0)
    booksReturned = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.book.title + " owned by " + self.teacher.name


class Classroom(models.Model):
    grade = models.ForeignKey(Grade,
                              on_delete=models.CASCADE,
                              related_name="classrooms")
    books = models.ManyToManyField(Book,
                                   through='OwnedByClass',
                                   related_name="classrooms")

    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class OwnedByClass(models.Model):
    classroom = models.ForeignKey(Classroom,
                                  on_delete=models.CASCADE,
                                  related_name='bookInfo')
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name='classInfo')

    booksOwned = models.PositiveSmallIntegerField(default=0)
    booksReturned = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.book.title + " owned by " + self.classroom.name


class Order(models.Model):
    forBook = models.ForeignKey(Book,
                                on_delete=models.CASCADE,
                                related_name="orders")

    code = models.CharField(max_length=15, blank=True, null=True)
    isbn = models.CharField(max_length=17, blank=True, null=True)
    publicationYear = models.PositiveSmallIntegerField()
    registryNumber = models.CharField(max_length=15, blank=True, null=True)
    billingNumber = models.CharField(max_length=20, blank=True, null=True)
    amountOrdered = models.PositiveSmallIntegerField(default=0)
    pricePerBook = models.DecimalField(max_digits=6, decimal_places=2)
    dateOrdered = models.DateField(default=datetime.date.today)
    booksLost = models.PositiveSmallIntegerField(default=0)

    @property
    def totalPrice(self):
        return self.pricePerBook * self.amountOrdered

    @property
    def amount(self):
        return self.amountOrdered - self.booksLost

    def __str__(self):
        return self.forBook.title
