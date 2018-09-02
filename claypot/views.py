import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    View,
)
from django.utils.text import slugify
from rest_framework.parsers import JSONParser

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
    RecipeIngredient,
    Ingredient,
    Unit,
)
from .serializers import RecipeSerializer


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


class RecipeUpdateStarFormView(LoginRequiredMixin, View):
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


class SearchableListView(View):
    queryset = None
    search_field = 'name'
    serializer_class = None
    limit = 10

    def get_queryset(self, request):
        return self.queryset

    def get_filtered_queryset(self, request, search_term):
        qs = self.get_queryset(request)
        return qs.filter(**{self.search_field + '__icontains': search_term})

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', '')
        results = self.get_filtered_queryset(request, search)[:self.limit]

        return JsonResponse(
            {'search': [getattr(item, self.search_field) for item in results]},
            safe=False)


class IngredientListView(SearchableListView):
    queryset = Ingredient.objects.all()


class UnitListView(SearchableListView):
    queryset = Unit.objects.all()


class RecipeEditFormView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'pk' in kwargs:
                instance = get_object_or_404(Recipe, pk=kwargs['pk'])
            else:
                instance = None
            response = RecipeSerializer(instance)
            return JsonResponse(response.data, safe=False)
        else:
            return render(request, 'claypot/recipe_update.html')

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('Expecting AJAX request')
        data = JSONParser().parse(request)
        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            pk = kwargs.get('pk', None)
            vd = serializer.validated_data
            pk = self.apply_input_to_database(pk, vd)
            instance = get_object_or_404(Recipe, pk=pk)
            serializer = RecipeSerializer(instance)
            return JsonResponse(serializer.data, safe=False)
        else:
            response = JsonResponse({'errors': serializer.errors}, safe=False)
            response.status_code = 400
            return response

    def apply_input_to_database(self, pk, data):
        # Save recipe
        if pk is None:
            base_slug = slugify(data['title'])
            slug = base_slug
            while Recipe.objects.filter(slug=slug).exists():
                slug = base_slug + '-{:04x}'.format(random.randint(0, 1024))
            recipe = Recipe.objects.create(
                title=data['title'],
                slug=slug,
                instructions=data['instructions']
            )
            pk = recipe.pk
        else:
            recipe = Recipe.objects.get(pk=pk)

        # Save new ingredients so they're hashable
        for ri in data['recipe_ingredients']:
            if ri['ingredient'].pk is None:
                ri['ingredient'].save()

        # Save recipe ingredients
        existing = {
            ri.ingredient: ri
            for ri in recipe.recipe_ingredients.all()
        }
        new = {
            ri['ingredient']: ri
            for ri in data['recipe_ingredients']
        }
        created = set(new) - set(existing)
        updated = set(existing) & set(new)
        removed = set(existing) - set(new)

        # Create new RecipeIngredient objects
        for ri_key in created:
            ri = new[ri_key]
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ri['ingredient'],
                ingredient_extra=ri['ingredient_extra'],
                optional=ri['optional'],
                amount_type=ri['amount_type'],
                amount_numeric=ri['amount_numeric'],
                amount_approx=ri['amount_approx'],
                unit=ri['unit'],
            )

        # Update existing RecipeIngredient objects
        for ri_key in updated:
            ri = new[ri_key]
            obj = existing[ri_key]
            obj.ingredient_extra = ri['ingredient_extra']
            obj.optional = ri['optional']
            obj.amount_type = ri['amount_type']
            obj.amount_numeric = ri['amount_numeric']
            obj.amount_approx = ri['amount_approx']
            obj.unit = ri['unit']
            obj.save()

        # Remove unmentioned RecipeIngredient objects
        for ri in recipe.recipe_ingredients.filter(ingredient__name__in=removed):
            ri.delete()

        return pk
