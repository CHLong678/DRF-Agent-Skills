from django.urls import path
from fixtureapp.views import CustomerListView
urlpatterns = [path("customers/", CustomerListView.as_view())]
