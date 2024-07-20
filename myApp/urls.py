from django.urls import path,include
from myApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',views.home,name="home"),
  path('register/',views.registrationView,name="register"),
  path('login/',views.loginView,name="login"),
  path('logout/',views.logoutView,name='logout'),
  path("reset/",views.password_reset,name="password_Reset"),
  path('password_reset/done/',views.password_reset_done,name='password_reset_done'),
  path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
  path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
  path("product_categories/",views.product_categories,name="product_categories"),
  path('create_product_category/',views.create_product_category,name="create_product_category"),
  path('update_product_category/<int:id>/',views.update_product_category,name="update_product_category"),
  path('confirm_delete_product_category/<int:id>/',views.delete_product_category,name="delete_product_category"),

]+static(settings.STATIC_URL,
          document_root=settings.STATIC_ROOT)
