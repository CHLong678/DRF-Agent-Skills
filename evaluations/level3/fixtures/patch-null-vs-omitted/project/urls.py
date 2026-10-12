from django.urls import path
from fixtureapp.views import CustomerDetailView

urlpatterns = [
    path("customers/<int:pk>/", CustomerDetailView.as_view()),
]
