from django.db import models

class Wallet(models.Model):
    seq_wallet_balance = models.AutoField(primary_key = True)
    email              = models.CharField(max_length=60, null = False)
    walletID           = models.CharField(max_length=65, null = True)
    wallet_balance     = models.TextField(null = True)
    created_at         = models.DateTimeField(auto_now_add =True, null = True)
    edited_at          = models.DateTimeField(auto_now =True, null = True)
    
    class Meta:
        db_table = "wallets"