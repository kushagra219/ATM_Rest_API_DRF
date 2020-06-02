from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "transaction"

urlpatterns = [
    path('card/register/', views.registerCardAPI.as_view(), name="card-register"),
    path('card/authenticate/', views.authenticateCardAPI.as_view(), name="card-authenticate"),
    path('card/deposit/', views.depositMoneyAPI.as_view(), name="card-deposit"),
    path('card/withdraw/', views.withdrawMoneyAPI.as_view(), name="card-withdraw"),
]