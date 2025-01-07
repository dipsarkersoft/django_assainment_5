from django.db import models
from django.contrib.auth.models import User
from profiles.models import UserAccount
from .constant import TRANSACTION_TYPE



class BooksCate(models.Model):
    name=models.CharField(max_length=30)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Books_Model(models.Model):
    name=models.CharField(max_length=30)
    description=models.CharField(max_length=200)
    price=models.IntegerField()
    quantity=models.IntegerField()
    category=models.ForeignKey(BooksCate,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='book/media/uploads/', blank = True, null = True)
    
    def __str__(self):
        return self.name



class BorrowModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    books=models.ForeignKey(Books_Model,on_delete=models.CASCADE)
    total_price = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    rturn_date = models.DateField(null=True, blank=True)
    isReturn=models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.books.name} by {self.user.username}"




class TransactionModel(models.Model):
    profile = models.ForeignKey(UserAccount, related_name = 'pr_transactions', on_delete = models.CASCADE)  
    book = models.ForeignKey(Books_Model,related_name='booksr',on_delete=models.CASCADE,null=True, blank=True)
    balance = models.IntegerField()
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)
    timestamp = models.DateTimeField(auto_now_add=True) 

    



class Reviews(models.Model):
    books = models.ForeignKey(Books_Model, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reviews by {self.name}"