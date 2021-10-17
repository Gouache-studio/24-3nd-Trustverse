import json, requests
from django.http import JsonResponse
from django.views import View

from core.utils import authentication
from .models import Report

#예외처리까지 생각할 것!! 
class ReportListView(View):
    #@authentication
    def get(self, request):

        response = requests.get('https://jupiterapiserver.azurewebsites.net/main/reports').json()
        reports = response["reports"]
        
        result = []
        for report in reports:
            cover_filename = report["titlepicture"].split("/")[4].split("?")[0]
            contente_filename = report["pdfurl"].split("/")[4].split("?")[0]

            result.append(
                {
                    "report_id"    : report["report_id"],
                    "title"        : report["title"],
                    "brief"        : report["brief"],
                    "cover"        : cover_filename,
                    "content"      : contente_filename, 
                    "cover_link"   : report["titlepicture"],
                    "content_link" : report["pdfurl"]
                }
            )

        return JsonResponse({"result" : result},status = 200)


class ReportDeleteView(View):
    # @authentication
    def post(self, request):
        data = json.loads(request.body)

        id = data["report_id"]
        reports = Report.objects.get(report_id = id)
        delete_report_id = reports.report_id
        reports.delete()

        return JsonResponse({"DELETE REPORT_ID" : delete_report_id}, status = 200)
