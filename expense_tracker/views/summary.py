from uuid import UUID
from django.shortcuts import render,redirect
from expense_tracker.models import Transaction,Mode,Category,ImportHistory
from django.db.models import Sum, Case, When, F,DecimalField
from django.db import connection,transaction
import pandas as pd
from django.utils import timezone
from django.core.files.base import ContentFile
from datetime import datetime
import calendar
def calculateIncomeExpenseByMonthAnnual(year, start_date_of_the_month, end_date_of_the_month):
    sql = f"""
    select
        sum(case when t.date>='{start_date_of_the_month}' and t.date<='{end_date_of_the_month}' and t.type='income' then t.amount else 0 end) as income_month,
        sum(case when t.date>='{start_date_of_the_month}' and t.date<='{end_date_of_the_month}' and t.type='expense' then t.amount else 0 end) as expense_month,
        sum(case when t.date>='{year}-01-01' and t.date<='{year}-12-31' and t.type='income' then t.amount else 0 end) as income_annual,
        sum(case when t.date>='{year}-01-01' and t.date<='{year}-12-31' and t.type='expense' then t.amount else 0 end) as expense_annual
    from expense_tracker_transaction as t
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


def getReportByType (request):
        current_date = datetime.now()
        current_year = current_date.year
        first_day_of_month = current_date.replace(day=1)
        last_day_num=str(calendar.monthrange(current_date.year, current_date.month)[1])
        last_day_of_month = f"{current_date.year}-{current_date.month}-"+str(calendar.monthrange(current_date.year, current_date.month)[1])

        start = request.GET.get("start")
        end = request.GET.get("end")

        if start is None:
            start = f"{current_year}-01-01"
        if end is None:
            end = f"{current_year}-12-{last_day_num}"
        print(start)
        print(end)

        resultIncomeExpenseByMonthAnnual=calculateIncomeExpenseByMonthAnnual(current_year,first_day_of_month,last_day_of_month)

        result = Transaction.objects.filter(date__range=(start, end)).aggregate(
        sum_income=Sum(Case(When(type='income', then=F('amount')), output_field=DecimalField(), default=0)),
        sum_expense=Sum(Case(When(type='expense', then=F('amount')), output_field=DecimalField(), default=0))
    )
        sqlChartByMode = """
    SELECT m.id, m.name, COALESCE(SUM(t.amount), 0)
    FROM expense_tracker_mode AS m
    LEFT JOIN expense_tracker_transaction AS t ON m.id = t.mode_id
    WHERE t.date >= %s AND t.date <= %s
    GROUP BY m.name, m.id
    ORDER BY m.name
"""
        with connection.cursor() as cursor:
            cursor.execute(sqlChartByMode , [start, end])
            resultChartByMode = cursor.fetchall()

        sqlReportByIncomeByMonth="SELECT EXTRACT(year  FROM date) AS year,EXTRACT(MONTH FROM date) AS month,SUM(amount) AS total_amount FROM expense_tracker_transaction where type='income' and date>=%s and date<=%s GROUP BY year,month ORDER BY year,month asc "
        with connection.cursor() as cursor:
            cursor.execute(sqlReportByIncomeByMonth, [start, end])
            resultReportByIncomeByMonth = cursor.fetchall()

        sqlReportByExpenseByMonth="SELECT EXTRACT(year  FROM date) AS year,EXTRACT(MONTH FROM date) AS month,SUM(amount) AS total_amount FROM expense_tracker_transaction where type='expense' and date>=%s and date<=%s GROUP BY year,month ORDER BY year,month asc "
        with connection.cursor() as cursor:
            cursor.execute(sqlReportByExpenseByMonth , [start, end])
            resultReportByExpenseByMonth = cursor.fetchall()

        sqlReportByCategory = '''
    SELECT c."name",
           COALESCE(SUM(CASE WHEN t."type" = 'income' THEN t.amount ELSE 0 END), 0) AS total_income,
           COALESCE(SUM(CASE WHEN t."type" = 'expense' THEN t.amount ELSE 0 END), 0) AS total_expense
    FROM expense_tracker_category AS c
    LEFT JOIN expense_tracker_transaction AS t ON c.id = t.category_id where  t.date>=%s and t.date<=%s
    GROUP BY c."name" order by c."name"
'''
        with connection.cursor() as cursor:
            cursor.execute(sqlReportByCategory , [start, end])
            resultReportByCategory = cursor.fetchall()




        return render(request, 'index.html', {'chartbytype': result,'chartbymode':resultChartByMode,'reportbyincomebymonth':resultReportByIncomeByMonth,'reportbyexpensebymonth':resultReportByExpenseByMonth,'reportbycategory':resultReportByCategory,'current_year':current_year,'resultIncomeExpenseByMonthAnnual':resultIncomeExpenseByMonthAnnual})


def importTransaction (request):
    data=ImportHistory.objects.all()
    data=data.order_by('-datetime')
    return render (request,'import-transaction.html',{'data':data})

def processImportTransaction (request):
    if request.method == 'POST' and request.FILES.get('excel_file'):

        excel_file = request.FILES['excel_file']

        df = pd.read_excel(excel_file)
        num_rows, num_columns = df.shape

        mode_cache = {}
        category_cache = []

        with transaction.atomic():
            transactions_to_create = []

            for x in range(num_rows):
                mode_name = df.iloc[x, 0]
                category_name = df.iloc[x, 1]

                date = df.iloc[x, 2]

                type = df.iloc[x, 3]
                amount = df.iloc[x, 4]
                note = df.iloc[x, 5]

                if mode_name not in mode_cache:
                    mode, _ = Mode.objects.get_or_create(name=mode_name)
                    mode_cache[mode_name] = mode

                else:
                    mode = mode_cache[mode_name]


                if category_name not in category_cache:
                    category, _ = Category.objects.get_or_create(name=category_name)
                    category_cache.append(category_name)

                else:
                    category = category_cache[category_name]
                transactions_to_create.append(
                    Transaction(
                        type=type,
                        amount=float(amount),
                        note=note,
                        date=date,
                        category=category,
                        mode=mode,
                    )
                )

            Transaction.objects.bulk_create(transactions_to_create)
        ImportHistory.objects.create(datetime=timezone.now(), file=excel_file)

    return render (request,'show-import-alert.html',)
