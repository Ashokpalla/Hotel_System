from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_employer:
            return redirect('employers:room_change_list')
        else:
            return redirect('customers:room_list')
    return render(request, 'hotel/home.html')
