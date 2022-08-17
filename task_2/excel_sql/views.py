import xlrd
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import *
from .models import *
import numpy as np


def handle_uploaded_file(f):
    file_name = f.name  # getting name of file
    with open(f'excel_sql/media/excel_sql/{file_name}', 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    sheet = xlrd.open_workbook(f'excel_sql/media/excel_sql/{str(f)}').sheet_by_index(0)

    header = ""  # getting name of report
    accounts, balances, turnovers = [], [], []
    try:
        op_type = BalanceType.objects.get(name="Opening balance")
        cl_type = BalanceType.objects.get(name="Closing balance")
    except BalanceType.DoesNotExist:
        op_type = BalanceType(name="Opening balance")
        op_type.save()
        cl_type = BalanceType(name="Closing balance")
        cl_type.save()
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
            balances.append(Balance(account=account, assets=row[1].value, liability=row[2].value, type=op_type))
            turnovers.append(Turnover(account=account, debit=row[3].value, credit=row[4].value))
            balances.append(Balance(account=account, assets=row[5].value, liability=row[6].value, type=cl_type))

    BalanceAccount.objects.bulk_create(accounts)
    Balance.objects.bulk_create(balances)
    Turnover.objects.bulk_create(turnovers)


def upload_file(request):
    try:
        uploaded_files = UploadedFile.objects.all()
        uploaded_files = [file.name for file in uploaded_files]
    except UploadedFile.DoesNotExist:
        uploaded_files = []
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('main'))
    else:
        form = UploadFile()

    context = {'form': form, "files": uploaded_files}
    return render(request, 'excel_sql/main.html', context)


def display_file(request, file_name):
    file = UploadedFile.objects.get(name=file_name)
    classes = Class.objects.all().order_by("id")
    op_type = BalanceType.objects.get(name="Opening balance")
    cl_type = BalanceType.objects.get(name="Closing balance")
    rows = []
    all_sums = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
    for cls in classes:
        cls_sums = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        rows.append(f"КЛАСС  {cls.id}  {cls.name}")
        subclasses = Subclass.objects.filter(cls=cls)
        for subcls in subclasses:
            subcls_sums = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
            accounts = BalanceAccount.objects.filter(subcls=subcls, file=file)
            for acc in accounts:
                op_bal = Balance.objects.get(account=acc, type=op_type)
                turnover = Turnover.objects.get(account=acc)
                cl_bal = Balance.objects.get(account=acc, type=cl_type)
                row = (acc.account_num, op_bal.assets, op_bal.liability, turnover.debit,
                       turnover.credit, cl_bal.assets, cl_bal.liability)
                rows.append(row)
                cls_sums += np.array(row[1:], dtype=np.float64)
                subcls_sums += np.array(row[1:], dtype=np.float64)
                all_sums += np.array(row[1:], dtype=np.float64)
            rows.append([subcls.id] + list(subcls_sums))
        rows.append(["ПО КЛАССУ"] + list(cls_sums))
    rows.append(["БАЛАНС"] + list(all_sums))


    context = {"file": file,
               "rows": rows}
    return render(request, 'excel_sql/display_file.html', context)
