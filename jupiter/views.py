import json, requests
from django.http import JsonResponse
from django.views import View

from core.utils import authentication
from .models import Report

#예외처리까지 생각할 것!! try except
class ReportListView(View):
    @authentication
    def get(self, request):
        try:         
            response = requests.get('https://jupiterapiserver.azurewebsites.net/main/reports').json()
            reports = response["reports"]
            
            result = []
            
            for report in reports:
                
                #report Object(1) (2) (3) (4) .... 
                #(1)
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
            for i in range(0, len(result)):

                report_id = result[i]["report_id"]
        
                #똑같은 report_id가 없으면 데이터 베이스에 추가하고 
                if not Report.objects.filter(report_id = report_id).exists():
                    title         = result[i]["title"]  
                    brief         = result[i]["brief"]
                    title_picture = result[i]["cover_link"]
                    pdf_url       = result[i]["content_link"]

                    Report.objects.create(
                        report_id = report_id,
                        title = title,
                        brief = brief,
                        titlepicture = title_picture,
                        pdfurl = pdf_url
                    )
                
                #똑같은 report_id가 있다면, pass해라 
                if Report.objects.filter(report_id = report_id).exists():
                    continue
            
            return JsonResponse({"reports" : result},status = 200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)



#=================================================================
# class ReportEditView(View): #title or description만 수정할 수 있음!! 
#     def post(self, request):
#         data = json.loads(request.body)

#         id = 
#==================================================================

class ReportDeleteView(View):
    @authentication
    def post(self, request):
        data = json.loads(request.body)

        id = data["report_id"]
        report = Report.objects.get(report_id = id)
        delete_report_id = report.report_id
        report.delete()

        return JsonResponse({"DELETE REPORT_ID" : delete_report_id}, status = 200)

