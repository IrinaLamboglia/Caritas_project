from django.contrib.auth import logout
from django.shortcuts import render, redirect

def exit(request):
    if request.method == 'POST':
        logout(request)
        print()
        return redirect('login')
   # return render(request, 'core/base.html')

