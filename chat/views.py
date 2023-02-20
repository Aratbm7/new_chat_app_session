from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from  django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.utils import timezone

# class SignUp(CreateView):
#     queryset = User.objects.all()
#     form_class = UserRegisterForm
#     success_url = reverse_lazy('login')
#     template_name = 'chat/register.html'
    
    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')

            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chat:index')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'chat/register.html', {'form': form})

# @login_required
def index(request):
    # request.session['created_at'] = 'hello'
    # member_session_date = request.session['created_at'] 
    # request.session.modified()
    # print(request.session.custom_session_set.created_at)  
    return render(request, 'chat/index.html', { 'session_key': request.session.session_key})
    