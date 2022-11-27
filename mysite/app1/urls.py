"""This Module Contain All the Urls Of APP1"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_page, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("work/<int:item_id>/", views.work, name="work"),
    path("create/", views.create, name="create"),
    path("addwork/<int:pk>/", views.addWork, name="addwork"),
    path("profile/", views.profile, name="profile"),
    path("apply/<int:pk>/<int:item_id>/", views.apply, name="apply"),
    path("worksearch/", views.worksearch, name="worksearch"),
    path("update_address", views.update_address, name="update_address"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
