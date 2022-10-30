from django.shortcuts import render


def home_page(request):
    return render(request, 'home_page.html')

def upload_sicro(request):
    return render(request, 'upload_sicro.html')