import json, requests, math
from django.http import JsonResponse
from django.views import View
from ast import literal_eval
from django.db.models import Q
from .models import Wallet

from core.utils import authentication
 
class WalletBalanceView(View):
    @authentication
    def get(self, request):
        try:
            search_keyword = request.GET.get("keyword", None)
            ordering = request.GET.get("ordering",'seq_wallet_balance')
            page = int(request.GET.get("page", 1))
            
            q = Q()

            #필터링 내용작성 =========================
            # 오름차순 정렬 등등임 
            # if id_trv_user:
            #     q.add(Q(fit__in = fit_id), Q.AND)
            #=====================================


            if search_keyword:
                q &= Q(name__icontains=search_keyword)
             
            wallets = Wallet.objects.filter(q).order_by(ordering) 
            
            limit = 7
            offset = (page-1)*limit
            page_count = math.ceil(len(wallets)/limit)
            
            result = {
                "page": page,
                "page_count": page_count,
                "total_count": len(wallets),
                "wallets": [],
            }

            wallets = wallets[offset : offset + limit]
            
            for wallet in wallets:
            
                balance = wallet.wallet_balance
                print("===========")
                print(literal_eval(balance))
                print(type(balance))
                print("===========")
                
                if not balance == "None":
                    balance = eval(balance)
                    coin_list = list(balance.keys())
                    values = list(balance.values())
                    password = values[0][:1][0]
                    num = values[0][1:][0]
                
                    portfolio = []
                    for i in range(0,len(coin_list)):
                        portfolio.append(
                            {
                                "coin_name" : coin_list[i],
                                "password"  : password,
                                "num"       : num
                            }
                        )
                    print(portfolio)
                    
                if balance == "None":
                    balance = None
                    coin_list = [0]
                    values = None
                    password = 0
                    num = 0

                    portfolio = []
                    portfolio.append(
                            {
                                "coin_name" : coin_list,
                                "password"  : password,
                                "num"       : num
                            }
                        )
                    print(portfolio)

                
                result["wallets"].append(
                    {
                        "email"          : wallet.email,
                        "wallet_id"      : wallet.walletID,
                        "created_at"     : wallet.created_at, 
                        "edited_at"      : wallet.edited_at,
                        "coin_list"      : coin_list,
                        "wallet_balance" : portfolio
                    }
                )

            return JsonResponse({"results": result}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "Page Does Not Exists"}, status=404)
