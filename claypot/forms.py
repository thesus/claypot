from django import forms

from .models import Recipe


TOGGLE_FORM_SET = 'set'
TOGGLE_FORM_UNSET = 'unset'


class RecipeUpdateStarForm(forms.Form):
    recipe = forms.ModelChoiceField(
        queryset=Recipe.objects.all(),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


class RecipeSetStarForm(RecipeUpdateStarForm):
    mode = TOGGLE_FORM_SET


class RecipeUnsetStarForm(RecipeUpdateStarForm):
    mode = TOGGLE_FORM_UNSET
