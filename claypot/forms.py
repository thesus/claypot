from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext

from .models import (
    AMOUNT_TYPE_APPROX,
    AMOUNT_TYPE_NONE,
    AMOUNT_TYPE_NUMERIC,
    Recipe,
    RecipeIngredient,
)


TOGGLE_FORM_SET = 'set'
TOGGLE_FORM_UNSET = 'unset'


class NaiveSerializerMixin:
    def serialize(self, exclude=None):
        return {
            field_name: self.data.get(field_name, field.initial)
            for field_name, field in self.fields.items()
            if exclude is None or field_name not in exclude
        }


class RecipeCreateForm(forms.ModelForm, NaiveSerializerMixin):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'instructions',
        )


class RecipeIngredientCreateForm(forms.ModelForm, NaiveSerializerMixin):
    def clean(self):
        cd = super().clean()
        errors = []
        if cd['amount_type'] == AMOUNT_TYPE_NONE:
            if cd['amount_numeric'] is not None:
                errors.append(
                    ValidationError(
                        ugettext(
                            'Numeric amount given although amount type is '
                            '"unspecified"'),
                        code='numeric-amount-given',
                    )
                )
            if cd['amount_approx'] is not None:
                errors.append(
                    ValidationError(
                        ugettext(
                            'Approximated amount given although amount type '
                            'is "unspecified"'),
                        code='approximated-amount-given',
                    )
                )
            if cd['unit'] is not None:
                errors.append(
                    ValidationError(
                        ugettext(
                            'Unit given although amount type is '
                            '"unspecified"'),
                        code='unit-given',
                    )
                )
        elif cd['amount_type'] == AMOUNT_TYPE_NUMERIC:
            if cd['amount_numeric'] is None:
                errors.append(
                    ValidationError(
                        ugettext(
                            'Numeric amount missing'),
                        code='numeric-amount-missing',
                    )
                )
            if cd['amount_approx'] is not None:
                errors.append(
                    ValidationError(
                        ugettext(
                            'Approximated amount given although amount type '
                            'is "numeric"'),
                        code='approximated-amount-given',
                    )
                )
            if cd['unit'] is None:
                errors.append(
                    ValidationError(
                        ugettext('Unit missing'),
                        code='unit-missing',
                    )
                )
        elif cd['amount_type'] == AMOUNT_TYPE_APPROX:
            if cd['amount_numeric'] is not None:
                errors.append(
                    ValidationError(
                        ugettext(
                            'Numeric amount given although amount type is '
                            '"approximated"'),
                        code='numeric-amount-given',
                    )
                )
            if cd['amount_approx'] is None:
                errors.append(
                    ValidationError(
                        ugettext('Approximated amount missing'),
                        code='approximated-amount-missing',
                    )
                )
            if cd['unit'] is not None:
                errors.append(
                    ValidationError(
                        ugettext(
                            'Unit given although amount type is '
                            '"approximated"'),
                        code='unit-given',
                    )
                )

        if len(errors) > 0:
            raise ValidationError(errors)
        return cd

    def serialize(self, *args, **kwargs):
        result = super().serialize(*args, **kwargs)
        if self.instance and self.instance.ingredient_id:
            result['ingredient_name'] = str(self.instance.ingredient)
        else:
            result['ingredient_name'] = ''
        return result

    class Meta:
        model = RecipeIngredient
        fields = (
            'recipe',
            'ingredient',
            'ingredient_extra',
            'optional',
            'amount_type',
            'amount_numeric',
            'amount_approx',
            'unit',
        )


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
