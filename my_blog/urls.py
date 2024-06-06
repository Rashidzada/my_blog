
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static, settings
admin.site.site_header = 'Bloging Web App'
admin.site.site_title = 'Bloging Web App'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls'))
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
