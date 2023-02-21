from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import FormFileCost


def home_page(request):
    return render(request, 'home_page.html')

def upload_app(request):
    return render(request, 'upload_file.html')

def upload_file(request):
    if request.method == 'POST':
        form = FormFileCost(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('success/url/')
        else:
            form = FormFileCost()
            return render(request, 'upload_file,html', {'form': form})
