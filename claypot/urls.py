from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home'
    ),
    path(
        'recipes/',
        views.RecipeListView.as_view(),
        name='recipe-list'
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetailView.as_view(),
        name='recipe-detail'
    ),
    path(
        'recipes/<int:pk>/set-star',
        views.RecipeSetStarFormView.as_view(),
        name='recipe-set-star'
    ),
    path(
        'recipes/<int:pk>/unset-star',
        views.RecipeUnsetStarFormView.as_view(),
        name='recipe-unset-star'
    ),
    path(
        'recipes/<int:pk>/edit',
        views.RecipeEditFormView.as_view(),
        name='recipe-update'
    ),
    path(
        'recipes/create',
        views.RecipeEditFormView.as_view(),
        name='recipe-create'
    ),
    path(
        'ingredients/',
        views.IngredientListView.as_view(),
        name='ingredient-list'
    )
]
