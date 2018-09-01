from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/<int:pk>/set-star', views.RecipeSetStarFormView.as_view(), name='recipe-set-star'),
    path('recipes/<int:pk>/unset-star', views.RecipeUnsetStarFormView.as_view(), name='recipe-unset-star'),
]