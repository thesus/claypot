<template>
  <div
    :class="{group: dirty.is_group}"
    class="table"
  >
    <input
      v-if="dirty.is_group"
      v-model="dirty.title"
      placeholder="Ingredient group title"
    >

    <div v-show="dirty.ingredients.length > 0">
      <div
        v-for="(ingredient, i) in dirty.ingredients"
        ref="ingredientsNode"
        :key="i"
        class="ingredient"
      >
      <div class="input amount">
          <div class="number">
            <input
              :value="displayAmount(ingredient)"
              :disabled="saving"
              :class="{'form-error': !!recipeIngredientError(i).amount_numeric.length || !!recipeIngredientError(i).amount_numeric.length}"
              :placeholder="$t('recipe_edit.amount')"
              @input="updateAmount(ingredient, $event)"
            >
            <FormFieldValidationError :errors="recipeIngredientError(i).amount_numeric" />
            <FormFieldValidationError :errors="recipeIngredientError(i).amount_approx" />
          </div>
          <div class="unit">
            <input
              v-model="ingredient.unit"
              :disabled="saving || ingredient.amount_type !== AMOUNT_TYPE_NUMERIC"
              :class="{'form-error': !!recipeIngredientError(i).unit.length}"
              :placeholder="$t('recipe_edit.unit')"

            >
            <FormFieldValidationError :errors="recipeIngredientError(i).unit" />
          </div>
        </div>
        <div class="input">
          <IngredientInput
            v-model="ingredient.ingredient"
            :disabled="saving"
            :error="!!recipeIngredientError(i).ingredient.length"
          />
          <FormFieldValidationError :errors="recipeIngredientError(i).ingredient" />
        </div>
        <div class="input">
          <input
            v-model="ingredient.ingredient_extra"
            :disabled="saving"
            :class="{'form-error': !!recipeIngredientError(i).ingredient_extra.length}"
            :placeholder="$t('recipe_edit.ingredient_extra')"
          >
          <FormFieldValidationError :errors="recipeIngredientError(i).ingredient_extra" />
        </div>
        <div class="input button">
          <div class="optional">
            <label>
              {{ $t('recipe_edit.optional') }}
            </label>
            <input
              v-model="ingredient.optional"
              type="checkbox"
              :disabled="saving"
              :class="{'form-error': !!recipeIngredientError(i).optional.length}"
            >
            <FormFieldValidationError :errors="recipeIngredientError(i).optional" />
          </div>
          <button
            :disabled="saving"
            tabindex="-1"
            class="btn btn-right remove"
            @click="dirty.ingredients.splice(i, 1)"
          >
            {{ $t('recipe_edit.remove') }}
          </button>
        </div>
      </div>
    </div>
    <button
      :disabled="saving"
      class="btn btn-right submit"
      @click.prevent="addIngredient"
    >
      {{ $t('recipe_edit.add_ingredient') }}
    </button>
    <button
      :disabled="saving"
      class="btn btn-right submit"
      @click.prevent="removeGroup"
    >
      {{ $t('recipe_edit.remove_group') }}
    </button>
  </div>
</template>

<script>
import IngredientInput from '@/components/IngredientInput'
import FormFieldValidationError from '@/components/FormFieldValidationError'

export default {
  name: 'RecipeEditIngredientTable',
  components: {
    FormFieldValidationError,
    IngredientInput,
  },
  props: {
    value: {
      type: Object,
      default: function () {
        return {}
      },
    },
    recipeIngredientError: {
      type: Function,
      default: function () {
        return function () {}
      }
    },
    saving: {
      type: Boolean,
      default: false,
    },
  },
  data () {
    return {
      dirty: {
        is_group: false,
        title: '',
        ingredients: [],
      },
      AMOUNT_TYPE_NONE: 1,
      AMOUNT_TYPE_NUMERIC: 2,
      AMOUNT_TYPE_APPROX: 3,
    }
  },
  computed: {
    displayAmount () {
      return ingredient => {
        switch (ingredient.amount_type) {
          case this.AMOUNT_TYPE_NUMERIC:
            if (ingredient.amount_numeric !== null) {
              return ingredient.amount_numeric
            } else {
              return ingredient.amount_approx
            }
          case this.AMOUNT_TYPE_APPROX:
            return ingredient.amount_approx
          default:
            return 'broken'
        }
      }
    }
  },
  watch: {
    value () {
      this.updateDirty()
    },
    dirty: {
      handler () {
        const equalIngredients = function (i1, i2) {
          const fields = [
            'ingredient',
            'ingredient_extra',
            'optional',
            'amount_type',
            'amount_numeric',
            'amount_approx',
            'unit',
          ]
          return fields.map(name => (i1[name] === i2[name])).every(i => i)
        }

        const changed = (
          (this.dirty.is_group !== this.value.is_group) ||
          (this.dirty.title !== this.value.title) ||
          (this.dirty.ingredients.some((ingredient, i) => !equalIngredients(this.value.ingredients[i] || {}, ingredient))) ||
          (this.value.ingredients.some((ingredient, i) => !equalIngredients(this.dirty.ingredients[i] || {}, ingredient)))
        )
        if (changed) {
          this.$emit('input', {
            is_group: this.dirty.is_group,
            title: this.dirty.title,
            ingredients: this.dirty.ingredients.map(i => Object.assign({}, i)),
          })
        }
      },
      deep: true,
    },
  },
  mounted () {
    this.updateDirty()
  },
  methods: {
    createEmptyIngredient () {
      return {
        ingredient: '',
        ingredient_extra: '',
        optional: false,
        amount_type: this.AMOUNT_TYPE_NUMERIC,
        amount_approx: '',
        amount_numeric: 0,
        unit: '',
      }
    },
    addIngredient () {
      this.dirty.ingredients.push(this.createEmptyIngredient())

      const pos = this.dirty.ingredients.length - 1
      /* Select the first field in the input after it was created */
      /* And yeah. This is pretty dirty. */
      this.$nextTick(() => {
        if (this.$refs.ingredientsNode) {
          this.$refs.ingredientsNode[pos].children[0].children[0].children[0].focus()
        }
      })
    },
    updateDirty () {
      this.dirty.is_group = this.value.is_group
      this.dirty.title = this.value.title
      this.dirty.ingredients.splice(0)
      this.dirty.ingredients.push(...this.value.ingredients.map(i => Object.assign({}, i)))
      if (this.dirty.ingredients.length === 0) {
        this.addIngredient()
      }
    },
    removeGroup () {
      this.$emit('remove', {})
    },
    updateAmount (ingredient, event) {
      const value = event.target.value
      const num = Number(value)
      if ((value === '') || !Number.isNaN(num)) {
        ingredient.amount_type = this.AMOUNT_TYPE_NUMERIC
        if (value !== '') {
          ingredient.amount_numeric = num
        } else {
          ingredient.amount_numeric = null
        }
        ingredient.amount_approx = value
      } else {
        ingredient.amount_type = this.AMOUNT_TYPE_APPROX
        ingredient.amount_numeric = null
        ingredient.amount_approx = value
      }
    }
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.ingredient {
  display: flex;
  width: 100%;
  flex-direction: row;
  margin: 2px 0 2px 0;
}

.input {
  width: 100%;
  margin: 0px 2px 0px 2px;

  &.amount, &.button{
    div {
      margin: 0px 2px 0px 2px;
    }
    display: flex;
  }

  &.button {
    width: initial;
    .optional {
      display: inline-block;
      width: max-content;
      margin: auto 4px auto 2px;
      font-size: smaller;
    }
    input {
      width: inherit;
      height: inherit;
    }
  }

  &.amount {
    .unit {
      width: 50%;
    }

    .number {
      width: 100%;
    }
  }
}

.description {
  display: flex;
}

.description span {
  width: 100%;
}

.table {
  margin-top: 0.5em;
}
.table:first-child {
  margin-top: 0em;
}

.table.group {
  padding: 0.5em;
  border: solid 1px #ccc;
  width: 100%;
  display: inline-block;
  box-sizing: border-box;
}
</style>
