from django.urls import path
from . import views

app_name = "diary"

urlpatterns = [
    path("", views.entry_list, name="entry_list"),
    path("signup/", views.signup, name="signup"),
    path("new/", views.entry_create, name="entry_create"),
    path("<int:pk>/", views.entry_detail, name="entry_detail"),
    path("<int:pk>/edit/", views.entry_update, name="entry_update"),
    path("<int:pk>/delete/", views.entry_delete, name="entry_delete"),
]
