from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
)

from .models import (
    AMOUNT_TYPE_APPROX,
    AMOUNT_TYPE_NONE,
    AMOUNT_TYPE_NUMERIC,
    Recipe,
)


class HomeView(TemplateView):
    template_name = 'claypot/home.html'


class RecipeListView(ListView):
    # template_name = 'claypot/recipe_list.html'
    context_object_name = 'recipes'
    queryset = Recipe.objects.all()
    ordering = '-published_on'


class RecipeDetailView(DetailView):
    # template_name = 'claypot/recipe_detail.html'
    model = Recipe
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = (
            context['recipe'].recipe_ingredients.
            all().
            order_by('ingredient__name').
            select_related('ingredient', 'unit')
        )
        context['AMOUNT_TYPE_APPROX'] = AMOUNT_TYPE_APPROX
        context['AMOUNT_TYPE_NONE'] = AMOUNT_TYPE_NONE
        context['AMOUNT_TYPE_NUMERIC'] = AMOUNT_TYPE_NUMERIC
        return context
