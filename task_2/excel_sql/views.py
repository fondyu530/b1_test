import xlrd
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import *
from .models import *


def handle_uploaded_file(f):
    file_name = f.name  # getting name of file
    with open(f'excel_sql/media/excel_sql/{file_name}', 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    sheet = xlrd.open_workbook(f'excel_sql/media/excel_sql/{str(f)}').sheet_by_index(0)

    header = ""  # getting name of report
    accounts, balances, turnovers = [], [], []
    for i in range(1, sheet.nrows - 2):
        row = sheet.row(i)
        if 1 <= i <= 3:
            header += f" {row[0].value}"
            header = header.strip()
            if i == 3:
                file = UploadedFile(name=file_name, header=header)
                file.save()
        elif (row[-1].value == '') and ("КЛАСС " in row[0].value):
            class_id, class_name = row[0].value.split("  ")[1:]
            try:
                Class.objects.get(id=int(class_id))
            except Class.DoesNotExist:
                cls = Class(id=int(class_id), name=class_name)
                cls.save()
        elif (len(str(row[0].value)) == 4) and (isinstance(row[0].value, str)) and (row[-1].value != ''):
            acc_num = int(row[0].value)
            subclass_id = int(row[0].value[:2])
            try:
                subcls_db = Subclass.objects.get(id=subclass_id)
            except Subclass.DoesNotExist:
                class_id_fk = int(row[0].value[0])
                cls = Class.objects.get(id=class_id_fk)
                subcls_db = Subclass(id=subclass_id, cls=cls)
                subcls_db.save()

            file_db = UploadedFile.objects.get(name=file_name)
            account = BalanceAccount(account_num=acc_num, subcls=subcls_db, file=file_db)
            accounts.append(account)
            balances.append(OpeningBalance(account=account, assets=row[1].value, liability=row[2].value))
            turnovers.append(Turnover(account=account, debit=row[3].value, credit=row[4].value))

    BalanceAccount.objects.bulk_create(accounts)
    OpeningBalance.objects.bulk_create(balances)
    Turnover.objects.bulk_create(turnovers)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('main'))
    else:
        form = UploadFile()
    return render(request, 'excel_sql/main.html', {'form': form})

