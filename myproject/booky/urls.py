from django.urls import path
from . import views
from . import ajax_views

urlpatterns = [
    # Index
    path("", views.index, name="index"),

    # Lists
    path('books/', views.BooksListView, name="books-list"),
    path('teachers/', views.TeachersListView.as_view(), name="teachers-list"),
    # path('grades/', GradesListView.as_view(), name="grades-list"),
    path('orders/', views.OrdersListView, name="orders-list"),
    path('grades/<int:pk>/', views.ClassroomsView, name="classroom-list"),

    # Add forms
    # Linting this will be *fun*
    path('addOrderStep0/', views.addOrderStep0, name="add-order-step-0"),
    path('addOrderStep1/', views.addOrderStep1, name="add-order-step-1"),
    path('addNewBookForTeacher/<int:pk>/', views.addNewBookForTeacher, name="add-new-book-for-teacher"),
    path('addNewBookForGrade/<int:pk>/', views.addNewBookForGrade, name="add-new-book-for-grade"),
    path('addTeacher', views.addTeacher, name="add-teacher"),
    # Edit forms
    path('editTeacher/<int:pk>/', views.editTeacher, name="edit-teacher"),
    path('editClass/<int:pk>/', views.editClass, name="edit-class"),
    path('editOrder/<int:pk>/', views.editOrder, name="edit-order"),
    path('deleteOrder/<int:pk>', views.deleteOrder, name="delete-order"),
    path('deleteTeacherBook/<int:pk>', views.deleteTeacherBook, name="delete-teacher-book"),
    # Ajax
    path('orders/ajax/orderFilter', ajax_views.OrderFilterView),
    path('books/ajax/bookFilter', ajax_views.BookFilterView),
]
