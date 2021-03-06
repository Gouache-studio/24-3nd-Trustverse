import json, re, requests, bcrypt, jwt

from django.views import View
from django.http import JsonResponse
from datetime import datetime, timedelta

from my_settings import SECRET_KEY, ALGORITHM
from admincustom.models import Admincustom

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        REGEX_PASSWORD = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$") 

        password = data["password"]

        print('=====================')
        print(data["name"])
        print('=====================')
        if Admincustom.objects.filter(name = data["name"]).exists():
            return JsonResponse({"MESSAGE" : "DUPLICATED ADMIN NAME"}, status = 400)
        
        print('=====================')
        print(data["password"])
        if not REGEX_PASSWORD.match(data["password"]):
            return JsonResponse({"MESSAGE" : "PASSWORD_ERROR"}, status = 400)
        
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        decoded_password = hashed_password.decode("utf-8")

        # query = f'SELECT walletID FROM wallet_balance WHERE email = "{current_user}" and walletID = "{walletID}"'

        Admincustom.objects.create(
            name = data["name"],
            password = decoded_password
        )

        return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
  
        try:
            if not Admincustom.objects.filter(name = data["name"]).exists():
                return JsonResponse({"MESSAGE": "INVALID_ADMIN"}, status = 401)

            admin = Admincustom.objects.get(name = data["name"])

            if not bcrypt.checkpw(data["password"].encode("utf-8"), admin.password.encode("utf-8")):
                return JsonResponse({"MESSAGE": "INVALID_PASSWORD"}, status = 401)
            
            access_token = jwt.encode({"id": admin.id, 'exp': datetime.utcnow() + timedelta(days=1)}, SECRET_KEY, algorithm= ALGORITHM)
            return JsonResponse({"MESSAGE": "SUCCESS", 'token' : access_token, "admin_name" : admin.name}, status = 200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

