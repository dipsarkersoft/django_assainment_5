from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserAccount

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','password1','password2','email']

    def __str__(self):
        return self.first_name
    
    def save(self, commit=True):
        our_user = super().save(commit=False) 
        if commit == True:
            our_user.save()   
            UserAccount.objects.create(
                user = our_user,
                balance=0              
            )
        return our_user
     
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-2 px-3 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            }) 



class ChangeUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-2 px-3 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })     



class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=100, required=True)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 100:
            raise forms.ValidationError('You need to deposit at least 100 TK')
        return amount

