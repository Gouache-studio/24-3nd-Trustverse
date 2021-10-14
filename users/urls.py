from django.urls import path
from users.views import UserDataView

urlpatterns = [
    path('/data', UserDataView.as_view()),
    # path('/getWallet', WalletView.as_view()),
]