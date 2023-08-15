from django.contrib import admin
from django.urls import include, path  
from django.conf import settings
from django.conf.urls.static import static
from auction import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('auctions/', views.auction_art_pieces, name='auctions'),
    path('art_gallery/', views.art_gallery, name='art_gallery'),
    path('my_collection/', views.my_collection, name='my_collection'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact_us/', views.contact_us, name='contact_us'),
     path('contact/', views.contact, name='contact'),
    path('art_piece/<int:art_piece_id>/update/', views.update_art_piece, name='update_art_piece'),
    path('search/', views.search, name='search'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
