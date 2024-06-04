from django.urls import path
from .views import CurrencyRateList

urlpatterns = [
    path('currency-rates/', CurrencyRateList.as_view(), name='currency-rate-list-create'),
]