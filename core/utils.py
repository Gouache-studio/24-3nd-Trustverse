from jwt import exceptions, decode

from django.http import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from django.contrib.auth.models import User
# 인증
def authentication(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            if not access_token:
                return JsonResponse( {'MESSAGE' : 'NO TOKEN'}, status = 403)

            #JWT payload는 유저id 값을 가지는 것
            payload = decode(access_token, SECRET_KEY, ALGORITHM)
            admin_id = payload['id']

            admin = User.objects.get(id = admin_id)
            request.admin = admin.id

        except exceptions.DecodeError:
            return JsonResponse( {'MESSAGE' : 'INVALID TOKEN'}, status = 403)

        except User.DoesNotExist:
            return JsonResponse( {'MESSAGE' : 'INVALID USER'}, status = 403)

        except exceptions.ExpiredSignatureError:
            return JsonResponse( {'MESSAGE' : 'TOKEN EXPIRED'}, status = 400)

        return func(self, request, *args, **kwargs)

    return wrapper
