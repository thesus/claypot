import django_filters
from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.db.models import Count, Q
from django.utils.translation import get_language, get_language_info

from claypot.models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ["name"]


class RecipeOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra["choices"] += [
            ("popularity", "Popularity"),
        ]

    def filter(self, qs, value):
        if value and any(v in ["popularity",] for v in value):
            return qs.annotate(popularity=Count("starred_by")).order_by("-popularity")

        return super().filter(qs, value)


class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    author_id = django_filters.ModelChoiceFilter(
        field_name="author", queryset=get_user_model().objects.all()
    )
    is_starred = django_filters.BooleanFilter(
        label="Is starred", method="filter_is_starred"
    )
    is_my_recipe = django_filters.BooleanFilter(
        label="Is my recipe", method="filter_is_my_recipe"
    )
    search = django_filters.CharFilter(label="Search", method="search_filter")
    exclude = django_filters.AllValuesMultipleFilter(
        field_name="pk", label="Exclude by id", method="filter_exclude_by_pk"
    )
    ordering = RecipeOrderingFilter(fields=(("published_on", "time"), "author"))

    def filter_exclude_by_pk(self, queryset, name, value):
        if value:
            return queryset.exclude(pk__in=value)
        return queryset

    def filter_is_starred(self, queryset, name, value):
        """Show recipes that are starred by the current user."""
        if value is True:
            if self.request.user.pk is not None:
                return queryset.filter(starred_by__id=self.request.user.pk)
            else:
                # anonymous
                return queryset.none()
        if value is False:
            if self.request.user.pk is not None:
                return queryset.exclude(starred_by__id=self.request.user.pk)
            else:
                # anonymous
                return queryset
        return queryset

    def filter_is_my_recipe(self, queryset, name, value):
        """Show recipes that are created by the current user."""
        if value is True:
            if self.request.user.pk is not None:
                return queryset.filter(author=self.request.user)
            else:
                # anonymous
                return queryset.none()
        if value is False:
            if self.request.user.pk is not None:
                return queryset.exclude(author=self.request.user)
            else:
                # anonymous
                return queryset
        return queryset

    def search_filter(self, queryset, name, value):
        """Search recipes by various fields and relations.

        The search is conducted on the following fields:
        - title
        - instructions
        - ingredients (group/non group)
        """

        if value:
            # Build the search vector
            vector = (
                SearchVector("title", weight="A")
                + SearchVector(
                    StringAgg("instructions__text", delimiter=" "), weight="C"
                )
                + SearchVector(
                    StringAgg(
                        "ingredients__ingredients__ingredient__name", delimiter=" ",
                    ),
                    weight="B",
                )
            )

            # extract language in lowercase for postgres tsquery
            lang = get_language_info(get_language())["name"].lower()
            query = SearchQuery(value, config=lang)

            # Query based on vector search and trigram similarity
            queryset = (
                queryset.annotate(
                    rank=SearchRank(vector, query),
                    similarity=TrigramSimilarity("title", value),
                )
                .filter(Q(rank__gte=0.1) | Q(similarity__gt=0.1))
                .order_by("-rank")
            )
            return queryset
        else:
            return queryset

    class Meta:
        model = Recipe
        fields = ["title"]
