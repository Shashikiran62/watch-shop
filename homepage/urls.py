from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from homepage import views  # Update this to match your app's name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('upload', views.upload, name="upload_images"),
    path('login', views.login_page, name="login"),
    path('signup', views.signup_user, name="signup"),
    path('logout', views.logout_user, name="logout"),
    path('product/<int:id>', views.show_product, name="product"),
    path('addtowish/<int:id>', views.addtowish, name="addtowish"),
    path('addtocart/<int:id>', views.addtocart, name="addtocart"),
    path('wishlist', views.show_wishlist, name="show_wishlist"),
    path('removewish/<int:id>', views.removewish, name="removewish"),
    path('removeCart/<int:id>', views.removeCart, name="removeCart"),
    path('show_cartlist', views.show_cartlist, name="show_cartlist"),
]

# Serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
