from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.base, name="base"),
    path(r'quote/', views.quote, name="quote"),
    path(r'show_all/', views.show_all, name="show_all"),
    path(r'about/', views.about, name="about"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)