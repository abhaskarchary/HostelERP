from django.shortcuts import render

# Create your views here.

def inventory_logs(request):
    return render(request, 'logs.html')