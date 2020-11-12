from django.urls import path
from django.conf.urls.static import static
from shop import settings
from .views import *

app_name = 'store'
urlpatterns = [
    path('', home_view, name='home_view'),
    path('info/', info_view, name='info_view'),
    path('add_product/', create_view, name='create_view'),
    path('products/<int:id>/', product_view, name='product_view'),
    path('<category>/', home_view, name='home_view'),
    path('account', account_info_view, name='account_info')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
