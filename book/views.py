from django.shortcuts import render,redirect
from .models import Books_Model,TransactionModel ,BooksCate,BorrowModel,Reviews
from .forms import ReviewsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
from profiles.models import UserAccount
from .constant import Borrow,Deposit,RETURN
from django.views.generic import ListView


def send_borrow_email(user, book, subject, template):
       
       
        message = render_to_string(template, {
            'user' : user,
            'book' : book,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()



def home(request,slug=None):
    
    allcate=BooksCate.objects.all()
    alp=Books_Model.objects.all()

    if slug is not None:
        mdl=BooksCate.objects.get(slug=slug)
        alp=Books_Model.objects.filter(category=mdl)
    #print(alp)  
    return render(request,'mainhero.html',{'data':allcate,'product':alp})



def details(request, id):

    single_book = Books_Model.objects.get(pk=id)
    Review = Reviews.objects.filter(books_id=id) 
    
    if request.user.is_authenticated:
        is_borrowed = BorrowModel.objects.filter(user=request.user, books=single_book).exists()

        if request.method == 'POST':
            form = ReviewsForm(request.POST)
            if not is_borrowed :
                messages.error(request,"Please Borrow This Book Than Review  ")
                return redirect('homepage')
            
            if form.is_valid():
                alreadyexist= Reviews.objects.filter(email=request.user.email,books=single_book)
                if alreadyexist:
                    messages.error(request,"You have already Reviews")
            
                else:
                    cmnt = form.save(commit=False) 
                    cmnt.email=request.user.email
                    cmnt.books = single_book 
                    cmnt.save()
                    return redirect('details', id=id)
        else:
            form = ReviewsForm()

        
        return render(request, 'details.html', {
            'data': single_book,
            'Reviews': Review,
            'form': form
        })
    else:
        return render(request, 'details.html', {
            'data': single_book,                    
            'Reviews': Review,
        })



@login_required
def borrow_book(request,id):
    
    abook=Books_Model.objects.get(pk=id)
    
    
    if request.user.account.balance < abook.price:
        messages.error(request, 'Please Deposit ,Not Enough Money')
        return redirect('deposit')  
    
    

    already_buy_not_ret=BorrowModel.objects.filter(user=request.user, books=abook,isReturn=False)
    if already_buy_not_ret:
        messages.error(request, 'You Already Borrowed This Book , Please Return Then Borrow')
        return redirect('allorder')


    request.user.account.balance-=abook.price
    request.user.account.save(update_fields=['balance'])
    
    BorrowModel.objects.create(
            user=request.user,
            books=abook,
            total_price=abook.price
        ).save()
    abook.save()
    inst_user=request.user.account
  
    TransactionModel.objects.create(
        profile=inst_user,
        book=abook,
        balance=abook.price,
        balance_after_transaction=inst_user.balance,
        transaction_type=Borrow, 
    )
    send_borrow_email(request.user, abook ,"Borrow Success Message", "borrowem.html")                  
    return redirect('allorder')

@login_required
def return_book(request,id):

    b_book=BorrowModel.objects.get(pk=id)
    this_book=Books_Model.objects.get(id=b_book.books_id)
    
    b_price=b_book.total_price
    

    if b_book: 
        request.user.account.balance+=b_price
        b_book.isReturn=True
        b_book.rturn_date = now().date()
        b_book.save()
        request.user.account.save(update_fields=['balance'])
        inst_user=request.user.account
        TransactionModel.objects.create(
            profile=inst_user,
            book=this_book,
            balance=b_price,
            balance_after_transaction=inst_user.balance,
            transaction_type=RETURN, 
        )
        messages.success(request,f"You have received { b_price } TK .")
        return redirect('allorder')
    

@login_required
def all_Trans(request):
    
    
    data=TransactionModel.objects.filter(profile_id=request.user.account.id)
    return render(request,'book_list.html',{'data':data} )


 

