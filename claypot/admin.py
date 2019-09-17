from django.contrib import admin

from . import models


admin.site.register(models.Ingredient)
admin.site.register(models.IngredientTag)
admin.site.register(models.Recipe)
admin.site.register(models.RecipeIngredient)
admin.site.register(models.RecipeRelation)
admin.site.register(models.RecipeDraft)
admin.site.register(models.Unit)
