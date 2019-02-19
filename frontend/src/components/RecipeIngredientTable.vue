<template>
  <div class="ingredients-group">
    <div class="caption" v-if="caption">
      <caption>
        {{ caption }}
      </caption>
    </div>
    <table>
      <tbody v-if="ingredients">
        <tr
          v-for="ingredient in ingredients"
          :key="ingredient.ingredient"
        >
          <td class="amount">
            {{ ingredient.amount_numeric }}&nbsp;{{ ingredient.unit }}
          </td>
          <td class="ingredient">
            {{ ingredient.ingredient }}<span v-if="ingredient.ingredient_extra">
              , {{ ingredient.ingredient_extra }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
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

<style lang="scss" scoped>
.amount {
  text-align: right;
  width: 70px;
}

.ingredient {
  padding-left: 10px;
  text-align: left
}

.caption {
  font-weight: 600;
  height: 20px;
  width: 100%;
  caption {
    display: block;
  }
}
</style>
