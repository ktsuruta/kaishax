from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django import template

from .models import Report, Company

# Create your views here.

def index(request):
    # Default sort key is -net_sales
    sort_key = request.GET.get('sort')
    if sort_key is None:
        sort_key = '-net_sales'

    # Innner_query helps to eliminate recordts which do not contain a security code.
    inner_query = Company.objects.exclude(security_code = '').exclude(sector_code = None)
    reports = Report.objects.filter(type_of_current_period='FY', edinet_code__in=inner_query).order_by('-year', sort_key)[:100]

    # Below lines provide company information.
    company_en_name_dict = {}
    company_name_dict = {}
    company_sector_dict = {}

    print(SECTOR_DICT)

    for row in inner_query:
        company_en_name_dict[row.edinet_code] = row.english_company_name
        company_name_dict[row.edinet_code] = row.company_name
        if len(row.sector_code) == 2:
            row.sector_code = '0' + row.sector_code
        company_sector_dict[row.edinet_code] = SECTOR_DICT[row.sector_code]

    return render(request, 'reports/index.html', {'reports':reports, 'company_en_name_dict':company_en_name_dict,'company_name_dict':company_name_dict, 'company_sector_dict':company_sector_dict})

def detail(request, edinet_code):
    company = Company.objects.get(edinet_code=edinet_code)
    company.security_code = company.security_code[:4]
    latest_fiscal_report = Report.objects.filter(edinet_code=edinet_code, type_of_current_period='FY').order_by('-year')[0]

    q1_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q1')
    q2_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q2')
    q3_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='Q3')
    fy_reports =  Report.objects.filter(edinet_code=edinet_code, type_of_current_period='FY')


    # Below is to find out the latest report to show in the upper part in the page
    if 0 in (len(fy_reports),len(q1_reports),len(q2_reports),len(q3_reports)):
        latest_report = Report.objects.filter(edinet_code=edinet_code).order_by('year', 'type_of_current_period')[0]
    else:
        print(len(q1_reports))
        print(len(q2_reports))
        print(len(q3_reports))
        print(len(fy_reports))
        if q2_reports[len(q2_reports)-1].year == q1_reports[len(q1_reports)-1].year:
            latest_report = q2_reports[len(q2_reports)-1]
        if q3_reports[len(q3_reports)-1].year == q2_reports[len(q2_reports)-1].year:
            latest_report = q3_reports[len(q3_reports)-1]
        if fy_reports[len(fy_reports)-1].year == q3_reports[len(q3_reports)-1].year:
            latest_report = latest_fiscal_report

    reports = {
        'q1':q1_reports,
        'q2':q2_reports,
        'q3':q3_reports,
        'fy':fy_reports
    }

    if company.sector_code is not None:
        if len(company.sector_code) == 2:
            company.sector_code = '0' + company.sector_code
        sector = SECTOR_DICT[company.sector_code]

    return render(request,'reports/detail.html', {'company': company,
                                                  'sector' : sector,
                                                  'q1_reports':q1_reports,
                                                  'q2_reports':q2_reports,
                                                  'q3_reports':q3_reports,
                                                  'fy_reports':fy_reports,
                                                  'latest_report':latest_report,
                                                  'latest_fiscal_report': latest_fiscal_report})


def search(request):
    '''

    :param request:
    :param query:
    :return:
    '''
    query = request.GET.get('query')
    companies = Company.objects.filter(english_company_name__icontains=query).exclude(sector_code=None)

    #companies = Company.objects.raw("SELECT * FROM reports_company where english_company_name LIKE " + "'%kaneko%'")

    return render(request, 'reports/search.html', {
        'companies': companies,
        'query': query,
    })



def _get_company_dicts(inner_query):
    '''
    :param inner_query: This is a result of taret records of reports_company.
    :return:
    '''
    # Below lines provide company information.
    company_en_name_dict = {}
    company_name_dict = {}
    company_sector_dict = {}

    print(SECTOR_DICT)

    for row in inner_query:
        company_en_name_dict[row.edinet_code] = row.english_company_name
        company_name_dict[row.edinet_code] = row.company_name
        if len(row.sector_code) == 2:
            row.sector_code = '0' + row.sector_code
        company_sector_dict[row.edinet_code] = SECTOR_DICT[row.sector_code]


SECTOR_DICT = {
    '011': 'Mining and energy development',
    '012': 'Electricity, Gas',
    '021': 'Textile fiber',
    '022': 'Paper and paper products',
    '023': 'Chemical, Chemical products',
    '024': 'Rubber, rubber products',
    '025': 'Ceramics, Sandstone products',
    '026': 'Steel and Metal Products',
    '027': 'Industrial materials',
    '031': 'Industrial equipment and heavy electric equipment',
    '032': 'Manufacturing machinery and electric machinery',
    '033': 'Business machinery',
    '034': 'Information equipment / communication equipment',
    '035': 'Household electrical equipment',
    '036': 'Semiconductor and electronic parts',
    '041': 'Car',
    '042': 'Car parts',
    '043': 'Shipbuilding',
    '044': 'Transportation machinery',
    '051': 'Food manufacturing',
    '052': 'Beverages, Tobacco, Loose goods',
    '061': 'Clothing items and accessories',
    '062': 'Daily necessities',
    '063': 'Hobbies, Entertainment goods',
    '071': 'Bio, Pharmaceutical related',
    '072': 'Medical, Health Care, Nursing Care',
    '081': 'Construction and civil engineering',
    '082': 'Construction materials / equipment',
    '083': 'Real estate · housing',
    '091': 'General trading company',
    '092': 'Textile / Chemical / Paper wholesale',
    '093': 'Construction materials · Electrical machinery · Metal wholesale',
    '094': 'Medicines · Medical wholesale',
    '095': 'Food unloading',
    '096': 'Daily life goods wholesale',
    '101': 'General retail, grocery retail',
    '102': 'Clothing and accessories retail',
    '103': 'Specialty store, Drugstore',
    '105': 'Home electronics retail',
    '106': 'Car retail',
    '107': 'Mail order',
    '111': 'Food Shop',
    '112': 'Bento / Delivery',
    '121': 'Bank',
    '122': 'Securities',
    '123': 'Insurance',
    '124': 'Consumer and business finance',
    '125': 'Lease, Rental',
    '126': 'Investment',
    '127': 'Real estate investment trust',
    '128': 'Exchange, Securities agency',
    '131': 'Warehouse and logistics',
    '132': 'Land transport',
    '133': 'Shipping',
    '134': 'Air transport',
    '141': 'Mass media',
    '142': 'Communication service',
    '143': 'Advertisement',
    '144': 'Content creation / delivery',
    '145': 'Internet site operation',
    '146': 'System software',
    '151': 'Leisure and leisure facilities',
    '152': 'Lifestyle related services',
    '153': 'Education',
    '154': 'Recruitment, temporary staffing',
    '155': 'Professional services for companies',
    '156': 'Travel, Hotel',
}