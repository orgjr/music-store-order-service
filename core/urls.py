from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("health/", views.health, name="health"),
    path("order/", include("order.urls")),
]
