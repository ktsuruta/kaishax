from django.http import HttpResponse
from django.shortcuts import render

from .models import Report, Company

# Create your views here.

def index(request):
    reports = Report.objects.filter(type_of_current_period='FY')
    return render(request, 'reports/index.html', {'reports':reports})

def detail(request, edinet_code):
    company = Company.objects.get(edinet_code=edinet_code)
    reports = Report.objects.filter(edinet_code=edinet_code)
    return render(request,'reports/detail.html', {'company': company, 'reports':reports})

