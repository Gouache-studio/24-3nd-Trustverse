import json
import requests

from django.http import JsonResponse
from django.core.files import File

from django.views import View
from requests.api import head

from core.utils import authentication
from .models import Report


class ReportListView(View):
    # @authentication
    def get(self, request):
        try:  
            response = requests.get('https://jupiterapiserver-dev.azurewebsites.net/main/reports').json()
            reports = response["reports"]
            
            result = []
            
            for report in reports:
               
                cover_link = report["titlepicture"]
                content_link = report["pdfurl"]
                cover_filename = cover_link.split("/")[4].split("?")[0]
                contente_filename = content_link.split("/")[4].split("?")[0]

                result.append(
                    {
                        "report_id"    : report["report_id"],
                        "title"        : report["title"],
                        "brief"        : report["brief"],
                        "cover"        : cover_filename,
                        "content"      : contente_filename, 
                        "cover_link"   : cover_link,
                        "content_link" : content_link
                    }
                )
            
            return JsonResponse({"reports" : result},status = 200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)


class ReportEditView(View): 
    # @authentication
    def put(self, request):
        try: 
            data = json.loads(request.body)
            print("==========")
            print(request.body)
            print("==========")

            report_id = data["report_id"]
            title = data["title"]
            brief = data["brief"]

            url = "https://jupiterapiserver-dev.azurewebsites.net/main/reports"
            
            payload=f'report_id={report_id}&title={title}&brief={brief}'
            headers = {
                'Content-Type' : 'application/x-www-form-urlencoded',
                "Accept"       : "application/json"
                }
            response = requests.request("PUT", url, headers=headers, data=payload).json()
            print("======")
            print(response)
            print("======")
            
            if response == {}:
                return JsonResponse({"result" : "EDIT SUCCESS!"}, status =200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)
        
class ReportDeleteView(View):
    # @authentication
    def delete(self, request):
        try:
            data = json.loads(request.body)
            print("==========")
            print(request.body)
            print("==========")

            report_id = data["report_id"]

            url = "https://jupiterapiserver-dev.azurewebsites.net/main/reports"
            headers = {"report_id" : f'{report_id}'}
            response = requests.request("DELETE", url, headers=headers).json()
            print("==========")        
            print(response)
            print("==========")
            if response == {}:
                return JsonResponse({"DELETE REPORT_ID" : report_id}, status = 200)
            
            elif response != {}:
                return JsonResponse({"MESSAGE", "INTERNAL SERVER"}, status =500, safe=False)
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)
 
