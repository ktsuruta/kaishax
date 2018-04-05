from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django import template

from .models import Report, Company

# Create your views here.

def index(request):
    sort_key = request.GET.get('sort')
    if sort_key is None:
        sort_key = '-net_sales'
    inner_query = Company.objects.exclude(security_code = '')
    reports = Report.objects.filter(type_of_current_period='FY', edinet_code__in=inner_query).order_by('-year', sort_key)[:100]

    for row in inner_query:
        pass
        #print(row.security_code)

    return render(request, 'reports/index.html', {'reports':reports})

def detail(request, edinet_code):
    company = Company.objects.get(edinet_code=edinet_code)
    company.security_code = company.security_code[:4]
    latest_fiscal_report = Report.objects.filter(edinet_code=edinet_code, type_of_current_period='FY').order_by('-year')[0]

    q1_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q1')
    q2_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q2')
    q3_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q3')
    fy_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='FY')


    if 0 in (len(fy_reports),len(q1_reports),len(q2_reports),len(q3_reports)):
        latest_report = Report.objects.filter(edinet_code=edinet_code).order_by('year', 'type_of_current_period')[0]
    else:
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

