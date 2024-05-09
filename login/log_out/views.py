from django.contrib.auth import logout
from django.shortcuts import render, redirect

def exit(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'logOut/confirmar_salida.html')

