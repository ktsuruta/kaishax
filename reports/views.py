from django.http import HttpResponse
from django.shortcuts import render

from .models import Report, Company

# Create your views here.

def index(request):
    reports = Report.objects.filter(type_of_current_period='FY')[:100]
    return render(request, 'reports/index.html', {'reports':reports})

def detail(request, edinet_code):
    company = Company.objects.get(edinet_code=edinet_code)
    latest_fiscal_report = Report.objects.filter(edinet_code=edinet_code, type_of_current_period='FY').order_by('-year')[0]

    q1_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q1')
    q2_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q2')
    q3_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q3')
    fy_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='FY')



    if fy_reports[len(fy_reports)-1].year == q1_reports[len(q1_reports)-1].year:
        latest_report = latest_fiscal_report
    if q2_reports[len(q2_reports)-1].year == q1_reports[len(q1_reports)-1].year:
        latest_report = q2_reports[len(q2_reports)-1]
    if q3_reports[len(q3_reports)-1].year == q2_reports[len(q2_reports)-1].year:
        latest_report = q3_reports[len(q3_reports)-1]

    reports = {
        'q1':q1_reports,
        'q2':q2_reports,
        'q3':q3_reports,
        'fy':fy_reports
    }

    return render(request,'reports/detail.html', {'company': company,
                                                  'q1_reports':q1_reports,
                                                  'q2_reports':q2_reports,
                                                  'q3_reports':q3_reports,
                                                  'fy_reports':fy_reports,
                                                  'latest_report':latest_report,
                                                  'latest_fiscal_report': latest_fiscal_report})

