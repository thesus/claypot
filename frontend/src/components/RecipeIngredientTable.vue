<template>
  <table class="ingredients">
    <caption v-if="caption">{{ caption }}</caption>
    <thead>
      <tr>
        <th class="amount">{{ $t('recipe_detail.amount') }}</th>
        <th class="ingredient">{{ $t('recipe_detail.ingredient') }}</th>
      </tr>
    </thead>
    <tbody v-if="ingredients">
      <tr
        v-for="ingredient in ingredients"
        :key="ingredient.ingredient">
        <td class="amount">{{ ingredient.amount_numeric }}&nbsp;{{ ingredient.unit }}</td>
        <td class="ingredient">{{ ingredient.ingredient }}<span v-if="ingredient.ingredient_extra">, {{ ingredient.ingredient_extra }}</span></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'RecipeIngredientTable',
  props: {
    caption: {
      type: String,
      default: '',
    },
    ingredients: {
      type: Array,
      default: () => [],
    },
  },
}
</script>
