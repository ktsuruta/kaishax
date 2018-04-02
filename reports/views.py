from django.http import HttpResponse
from django.shortcuts import render

from .models import Report, Company

# Create your views here.

def index(request):
    reports = Report.objects.filter(type_of_current_period='FY')[:100]
    return render(request, 'reports/index.html', {'reports':reports})

def detail(request, edinet_code):
    company = Company.objects.get(edinet_code=edinet_code)
    latest_report = Report.objects.filter(edinet_code=edinet_code, type_of_current_period='FY').order_by('-year')[0]
    reports = Report.objects.filter(edinet_code=edinet_code, type_of_current_period='FY')
    return render(request,'reports/detail.html', {'company': company, 'reports':reports, 'latest_report':latest_report })

