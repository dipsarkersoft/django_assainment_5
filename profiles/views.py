from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.contrib.auth import login,logout
from .forms import UserRegistrationForm,ChangeUserForm,DepositForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from book.models import BorrowModel
from .models import UserAccount
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from profiles.models import UserAccount
from book.constant import Deposit
from book.models import TransactionModel


def send_transaction_email(user, amount, subject, template):
       
       
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class UserRegistrationView(FormView):
    template_name='registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('profile'))
        return super().dispatch(request, *args, **kwargs)
    

    def  form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name='login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('profile'))
        return super().dispatch(request, *args, **kwargs)
   
    def get_success_url(self):
        return reverse_lazy('profile')


@method_decorator(login_required, name='dispatch')
class AllOrderView(ListView):
    model = BorrowModel
    template_name = 'allborrow.html'  
    context_object_name = 'data'
     

    def get_queryset(self):
         
        return BorrowModel.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('register')     
    
@login_required
def editProfile(request):
    if request.method == 'POST':
        profile_form =ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    
    else:
        profile_form =ChangeUserForm(instance = request.user)
    return render(request, 'profile.html', {'form' : profile_form})




@method_decorator(login_required, name='dispatch')
class DepositMoneyView(FormView):
    form_class = DepositForm
    template_name = 'deposit.html' 

    def form_valid(self, form):
      
        amount = form.cleaned_data['amount']       
        user_account, created = UserAccount.objects.get_or_create(user=self.request.user)
        user_account.balance += amount
        user_account.save(update_fields=['balance'])

        inst_user=self.request.user.account
        TransactionModel.objects.create(
            profile=inst_user,          
            balance=amount,
            balance_after_transaction=inst_user.balance,
            transaction_type=Deposit, 
         )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(amount)}BDT was deposited to your account successfully'
        )
       # print(self.request.user.account.balance)

        send_transaction_email(self.request.user, amount, "Deposite Message", "depositEm.html")

        return redirect('profile') 

    