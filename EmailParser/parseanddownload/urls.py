from django.urls import path

from . import views
app_name='parseanddown'         
urlpatterns = [
  path('', views.show_the_db),
  path('makedb', views.upload_from_gmail),
  path('delete',views.clear_db),


]