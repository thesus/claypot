<template>
  <div class="ingredients-group">
    <div
      v-if="caption"
      class="caption"
    >
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
            <span v-if="ingredient.amount_type === AMOUNT_TYPE_NUMERIC && ingredient.unit != ''">
              {{ formatter.format(ingredient.amount_numeric * scaling) }}&nbsp;{{ ingredient.unit }}
            </span>
            <span v-else-if="ingredient.amount_type === AMOUNT_TYPE_NUMERIC && ingredient.amount_numeric != null">
              {{ formatter.format(ingredient.amount_numeric * scaling) }}
            </span>
            <span v-else-if="ingredient.amount_type === AMOUNT_TYPE_APPROX">

              {{ ingredient.amount_approx }}
            </span>
          </td>
          <td class="ingredient">
            {{ ingredient.ingredient }}{{ ingredient.ingredient_extra ? ', ' + ingredient.ingredient_extra : '' }}
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
    scaling: {
      type: Number,
      default: 1.0,
    }
  },
  data () {
    return {
      AMOUNT_TYPE_NONE: 1,
      AMOUNT_TYPE_NUMERIC: 2,
      AMOUNT_TYPE_APPROX: 3,
      formatter: new Intl.NumberFormat(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 2}),
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
