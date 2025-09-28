from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # inclui as rotas de accounts
    path('', include('dashboard.urls')),  # dashboard na raiz
    path('documents/', include('documents.urls')),
    path('printing/', include('printing.urls')),
]

# Servir arquivos de mídia em modo debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
