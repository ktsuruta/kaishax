from django.db import models

# Create your models here.

class Company(models.Model):
    edinet_code = models.CharField(max_length=6, primary_key=True)
    company_name = models.CharField(max_length=200, default='', null=True)
    english_company_name = models.CharField(max_length=200, default='', null=True)
    security_code = models.CharField(max_length=5, default='', null=True)
    sector_code = models.CharField(max_length=3, default='', null=True)
    stock_market = models.CharField(max_length=45, default='', null=True)


class Report(models.Model):
    edinet_code = models.CharField(max_length=6)
    year = models.CharField(max_length=4)
    type_of_current_period = models.CharField(max_length=2)
    current_fiscal_year_start_date = models.DateField('fiscal year start date')
    current_fiscal_year_end_date = models.DateField('fiscal year end date')
    accounting_standard = models.CharField(max_length=15)
    per = models.DecimalField(max_digits=8, decimal_places=3)
    roe = models.DecimalField(max_digits=8, decimal_places=3)
    eps = models.DecimalField(max_digits=8, decimal_places=3)
    equity_to_asset_ratio = models.DecimalField(max_digits=8, decimal_places=3)
    pay_out_ratio = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    net_sales = models.IntegerField(default=0)
    net_assets = models.IntegerField(default=0)
    total_assets = models.IntegerField(default=0)
    liabilities = models.IntegerField(default=0)
    operating_revenue = models.IntegerField(default=0)
    ordinary_revenue = models.IntegerField(default=0)
    profit_before_tax = models.IntegerField(default=0)
    owners_equity_per_share = models.IntegerField(default=0)
    cash_and_cash_equivalents = models.IntegerField(default=0)
    cash_flow_from_operating = models.IntegerField(default=0)
    cash_flow_from_investing = models.IntegerField(default=0)
    cash_flow_from_financing = models.IntegerField(default=0)
    whether_consolidated_financial_statements = models.BooleanField(default=0)

    class Meta:
        unique_together = (("edinet_code", "year", "type_of_current_period"),)

    def __str__(self):
        return self.edinet_code



