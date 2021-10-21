from django.urls import path
from wallets.views import WalletBalanceView

#API 따라서 만들기!!! 
urlpatterns = [
    path('', WalletBalanceView.as_view()),
]