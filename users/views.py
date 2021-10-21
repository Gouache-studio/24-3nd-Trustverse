import json, requests, math
from django.http import JsonResponse
from django.views import View

from django.db.models import Q
from .models import User

from core.utils import authentication



#예외처리까지 생각할 것!! 
class UserListView(View):
    @authentication
    #토큰 발급하는 것까지 로직 만들것 
    def get(self, request):
        try:
            search_keyword = request.GET.get("keyword", None)
            ordering = request.GET.get("ordering",'id_trv_user')
            page = int(request.GET.get("page", 1))

            q = Q()

            #필터링 내용작성 =============================
            # if id_trv_user:
            #     q.add(Q(fit__in = fit_id), Q.AND)

            if search_keyword:
                q &= Q(name__icontains=search_keyword)
            #==========================================
            
            users = User.objects.filter(q).order_by(ordering) 
            
            limit = 7
            offset = (page-1)*limit
            page_count = math.ceil(len(users)/limit)
            
            result= []
            
            result = {
                "page": page,
                "page_count": page_count,
                "total_count": len(users),
                "trv_user": [],
            }

            users = users[offset : offset + limit]
            
            for user in users:
                result["trv_user"].append(
                    {
                        "id_trv_user"       : user.id_trv_user,
                        "email"             : user.email,
                        "f_name"            : user.f_name,
                        "l_name"            : user.l_name,
                        "password"          : user.password,
                        "phone_no"          : user.phone_no,
                        "country"           : user.country,
                        "appname"           : user.appname,
                        "register_datetime" : user.register_datetime,
                        "refer_code"        : user.refer_code,
                        "social_type"       : user.social_type,
                        "social_uuid"       : user.social_uuid,
                        "inactive_user"     : user.inctive_user,
                        "pwd_edited_date"   : user.password_edited_at
                    }
                )
            return JsonResponse({"results": result}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "Page Does Not Exists"}, status=404)

        # #토큰 가져오기 
        # access_token = request.headers.get("Authorization")
        # #https://trv-users.trustverse.io/api/v1/web/users
        # response = requests.get('https://tams-develop.trustverse.io/api/v2/auth/login',headers=({"Authorization": f'Bearer {access_token}',"X-API-KEY": f'{x_api_key}'})).json()
        # print(access_token)

        
        
        
        # # response = requests.get('https://tams-develop.trustverse.io/api/v1/users/login', headers=({"X-API-KEY" : f'Bearer {access_token}'})).json()
        
        # # response = requests.get('https://tams-develop.trustverse.io/api/v1/users/data/get', headers=({"Authorization" : f'Bearer {access_token}'})).json()
        # print("=========================")
        # print(response)
        # print("=========================")
        # result = response
        # return JsonResponse({"result" : result}, status= 200)
        # #
        
        #  result = []
        # for report in reports:
        #     cover_filename = report["titlepicture"].split("/")[4].split("?")[0]
        #     contente_filename = report["pdfurl"].split("/")[4].split("?")[0]

        #     result.append(
        #         {
        #             "report_id"    : report["report_id"],
        #             "title"        : report["title"],
        #             "brief"        : report["brief"],
        #             "cover"        : cover_filename,
        #             "content"      : contente_filename, 
        #             "cover_link"   : report["titlepicture"],
        #             "content_link" : report["pdfurl"]
        #         }
        #     )

        # return JsonResponse({"result" : result},status = 200)

