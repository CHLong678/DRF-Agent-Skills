from django.urls import path
from fixtureapp.views import OrderListView

urlpatterns = [
    path("orders/", OrderListView.as_view()),
]
