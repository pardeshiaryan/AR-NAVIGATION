# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entryPage, name="entrypage"),
    path("search", views.search, name="search"),
    path("new", views.createEntry, name="newentry"),
    path("edit", views.editEntry, name="edit"),
    path("random", views.randomPage, name="random"),
    path("function", views.Function, name="function"),  # Update path and view name as needed
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
