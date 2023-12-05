from django.shortcuts import redirect, render
from django.views import generic

from ..forms.sign_up_form import SignUpForm

__all__ = (
    'UserSignUpView',
)


class UserSignUpView(generic.View):
    template_name = 'templates/user/signup.html'
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class
        message = ''

        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

        else:
            form = self.form_class()

        message = 'Sign up failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})
