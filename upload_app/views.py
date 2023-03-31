from django.shortcuts import render
from django.http import HttpResponseRedirect

from upload_app.models import ModelFileCost
from .forms import FormFileCost
from django.core.files.storage import FileSystemStorage


def home_page(request):
    return render(request, 'home_page.html')

def upload_app(request):
    if request.method == 'POST':
        form = FormFileCost(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('./')
    else:
        form = FormFileCost()
    return render(request, 'upload_app.html', {'form': form})