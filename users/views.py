import json, requests, math
from django.http import JsonResponse
from django.views import View

from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Q

from .models import User
from core.utils import authentication

class DashboardView(View):
    # @authentication
    def get(self, request):
        try:
            #None 으로 할 경우 nonetype이라 공백처리된 데이터를 못 받음 따라서 "" 로 표시할 것 
            #폰넘버로 국가정할 수 있음 #82 -> KR #76 -> BY
            
            result = {
                "User_App" : [],
                "User_Appratio" : [],
                "User_Socialtype" : [],
                "Country" : [],
                "Monthly_New_User" : [],
                "Total" :  [],
            }

            #4. 누적 가입자 수 
            total_register_num = User.objects.count()
            total_withdrawn_num = User.objects.filter(inctive_user=1).count()
            cumulative_num = total_register_num + total_withdrawn_num
            result["Total"].append(
                {
                    "total_register_num"  : total_register_num,
                    "total_withdrawn_num" : total_withdrawn_num,
                    "cumulative_num"      : cumulative_num
                }
            )
            #=============================================
            # 쿼리셋으로 앱 개수별로 통신이 늘어남.
            # 효율적인 통신은 아님! 어떻게 효율적 통신을 할지 생각하자. 
            #=============================================
            
            #1. 앱별 가입자 수 #2. 앱별 가입자 비율
            apps = User.objects.values('appname').annotate(count_app=Count('appname'))
            
            for app in apps:
                appname = app['appname']
                #if canvas_appraisal가 없다면 추가해라 
                count_app = app['count_app']

                result["User_App"].append(
                    {
                        "appname" : appname,
                        "app_num" : count_app
                    }
                )
                user_ratio = round((count_app/total_register_num)*100)
                result["User_Appratio"].append(
                    {
                        "appname" : app,
                        "app_ratio" : user_ratio
                    }
                )
            
            
            # #3. 가입타입별 유저 수 
            types = User.objects.values('social_type').annotate(count_type=Count('social_type'))
            for type in types:
                social_type = type['social_type']
                if social_type == "":
                    social_type = "local"
                
                count_type = type['count_type']                
                
                result["User_Socialtype"].append(
                    {
                        "social_type" : social_type,
                        "social_type_num"  : count_type
                    }
                )
            
            
            #5. 월별 가입자 수 총 현재월일 부터 12개월 전 까지
            monthly_users = User.objects.annotate(month=TruncMonth('register_datetime')).values('month').annotate(count_monthly_users=Count('id_trv_user'))[:12]
            
            for monthly_user in monthly_users:
                year_month = str(monthly_user['month']).split('-')[:2]
                count_user = monthly_user['count_monthly_users']
                result["Monthly_New_User"].append(
                    {
                        "year_month" : year_month,
                        "mothly_num" : count_user
                    }
                )
            #    User.objects.filter(register_date = )
            #     result["대쉬보드"].append(
            #         {
            #             "id"        :  
            #             "month"     : type,
            #             "counting1" : type_count
            #             "counting2" : type_countsaa
            #         }
            #     )

            #6. 국가별 가입자 수 상위 4개
            topfour_country = User.objects.values('country').annotate(count_country=Count('country')).order_by('-count_country')[:4]
            
            for i in range(len(topfour_country)):
                country = topfour_country[i]['country']
                count_country = topfour_country[i]['count_country']
                            
                result["Country"].append(
                    {
                        "country"     : country,
                        "country_num" : count_country
                    }
                )
            
            country = User.objects.values('country').annot
            phone_query = User.objects.values('phone_no')
            for query in phone_query:
                if query['phone_no'][:2] == 82:
                    country = 'KR'
      
                        
            # for flag in country:
            #     country_num = User.objects.filter(country = flag)
            #     country_count = len(country_num)
            #     if flag == "":
            #         flag = "Undefined"

            #     result["Country"].append(
            #         {
            #             "country": flag,
            #             "country_count" : country_count
            #         }
            # )
            return JsonResponse({"result" : result}, status =200)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY ERROR"}, status=404)


#예외처리까지 생각할 것!! 
class UserListView(View):
    # @authentication
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

