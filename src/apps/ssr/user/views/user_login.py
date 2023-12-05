from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import generic

from ..forms.login_form import LoginForm

__all__ = (
    'UserLoginView',
)


class UserLoginView(generic.View):
    template_name = 'templates/user/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''

        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')

        message = 'Login failed!'

        return render(request, self.template_name, context={'form': form, 'message': message})
