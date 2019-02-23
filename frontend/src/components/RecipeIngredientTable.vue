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
            <span v-if="ingredient.amount_type === AMOUNT_TYPE_NUMERIC">
              {{ ingredient.amount_numeric }}&nbsp;{{ ingredient.unit }}
            </span>
            <span v-else-if="ingredient.amount_type === AMOUNT_TYPE_APPROX">
              {{ ingredient.amount_approx }}
            </span>
          </td>
          <td class="ingredient">
            {{ ingredient.ingredient }}<span v-if="ingredient.ingredient_extra">, {{ ingredient.ingredient_extra }}</span>
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
  data () {
    return {
      AMOUNT_TYPE_NONE: 1,
      AMOUNT_TYPE_NUMERIC: 2,
      AMOUNT_TYPE_APPROX: 3,
    }
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
