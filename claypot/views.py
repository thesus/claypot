from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    View,
)

from .forms import (
    RecipeSetStarForm,
    RecipeUnsetStarForm,
    TOGGLE_FORM_SET,
    TOGGLE_FORM_UNSET,
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
        context['is_starred'] = context['recipe'].is_starred_by(
            self.request.user)
        context['tags'] = sorted(str(tag) for tag in context['recipe'].tags())
        context['AMOUNT_TYPE_APPROX'] = AMOUNT_TYPE_APPROX
        context['AMOUNT_TYPE_NONE'] = AMOUNT_TYPE_NONE
        context['AMOUNT_TYPE_NUMERIC'] = AMOUNT_TYPE_NUMERIC
        return context


class RecipeUpdateStarFormView(View, LoginRequiredMixin):
    form_class = None

    def post(self, request, pk):
        data = {
            'recipe': pk,
        }
        data.update(request.POST)
        form = self.form_class(data=data, user=request.user)
        if form.is_valid():
            recipe = form.cleaned_data['recipe']
            collection = recipe.starred_by
            if form.mode == TOGGLE_FORM_SET:
                collection.add(form.user.pk)
            elif form.mode == TOGGLE_FORM_UNSET:
                collection.remove(form.user.pk)
            else:
                # unreachable / programming error
                raise NotImplementedError('unknown toggle mode')
            return redirect('recipe-detail', pk=recipe.pk)
        else:
            return HttpResponseBadRequest()


class RecipeSetStarFormView(RecipeUpdateStarFormView):
    form_class = RecipeSetStarForm


class RecipeUnsetStarFormView(RecipeUpdateStarFormView):
    form_class = RecipeUnsetStarForm
