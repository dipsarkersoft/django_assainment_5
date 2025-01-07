from django.urls import path,include
from .views import home,details,borrow_book,return_book,all_Trans
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',home,name='homepage'),
  path('<slug:slug>',home,name='cateWise'),
  path('details/<int:id>',details,name='details'),
  path('transaction/',all_Trans,name='transaction'),
  path('borrow/<int:id>',borrow_book,name='borrow_book'),
  path('return_book/<int:id>',return_book,name='return_book'),
  
    
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)