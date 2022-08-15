from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import *


def handle_uploaded_file(f):
    with open(f'excel_sql/media/excel_sql/{str(f)}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    with open(f'excel_sql/media/excel_sql/{str(f)}', 'r', encoding='utf-8') as file:
        pass


def upload_file(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('main'))
    else:
        form = UploadFile()
    return render(request, 'excel_sql/main.html', {'form': form})

