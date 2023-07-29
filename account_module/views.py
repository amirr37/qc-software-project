from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from account_module.forms import LoginForm


# Create your views here.

# Login with django auth
# class LoginView(View):
#     def get(self, request):
#         context = {'login_form': LoginForm()}
#         return render(request, 'account_module/login.html', context)
#
#     def post(self, request):
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             username = login_form.cleaned_data['username']
#             password = login_form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('index_page')
#             else:
#                 login_form.add_error('password', 'Invalid username or password.')
#
#         context = {'login_form': login_form}
#         return render(request, 'account_module/login.html', context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


class LoginView(APIView):
    def get(self, request: Request):
        # todo : fix if statement
        if request.user.is_authenticated:
            return redirect('index_page')
        context = {'login_form': LoginForm()}
        return render(request, 'account_module/login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index_page')

        login_form = LoginForm(request.data)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return redirect('index_page')
                # return Response({'access_token': access_token})
            else:
                login_form.add_error('username', 'invalid username or password')
                return render(request, 'account_module/login.html',
                              {'login_form': login_form, })
        else:
            login_form.add_error('username', 'invalid username or password')
            return render(request, 'account_module/login.html', {'login_form': login_form})
