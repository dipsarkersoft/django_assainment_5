from django.contrib import admin
from .models import Books_Model ,BooksCate,TransactionModel,BorrowModel,Reviews

# Register your models here.
class BooksCateAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ['name', 'slug']


admin.site.register(BooksCate,BooksCateAdmin)
admin.site.register(Books_Model)
admin.site.register(BorrowModel)
admin.site.register(Reviews)
admin.site.register(TransactionModel)


    