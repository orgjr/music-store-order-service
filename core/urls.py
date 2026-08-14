from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("health/", views.health, name="health"),
    path("", include("order.urls")),
    path("", include("order_item.urls")),
]
