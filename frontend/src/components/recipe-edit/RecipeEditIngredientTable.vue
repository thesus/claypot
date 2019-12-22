<template>
  <div
    :class="{group: dirty.is_group}"
    class="table"
  >
    <input
      v-if="dirty.is_group"
      v-model="dirty.title"
      placeholder="Ingredient group title"
      class="title"
    >
    <div
      v-show="dirty.ingredients.length > 0"
    >
      <div class="header">
        <span>{{ $t('recipe_edit.amount') }}</span>
        <span>{{ $t('recipe_edit.unit') }}</span>
        <span>{{ $t('recipe_edit.ingredient') }}</span>
        <span>{{ $t('recipe_edit.ingredient_extra') }}</span>
        <span>{{ $t('recipe_edit.optional') }}</span>
        <span>{{ $t('recipe_edit.action') }}</span>
      </div>
      <div
        v-for="(ingredient, i) in dirty.ingredients"
        ref="ingredientsNode"
        :key="i"
        class="ingredient"
      >
        <div class="input amount">
          <input
            :value="displayAmount(ingredient)"
            :disabled="saving"
            :class="{'form-error': !!recipeIngredientError(i).amount_numeric.length || !!recipeIngredientError(i).amount_numeric.length}"
            @input="updateAmount(ingredient, $event)"
          >
          <FormFieldValidationError :errors="recipeIngredientError(i).amount_numeric" />
          <FormFieldValidationError :errors="recipeIngredientError(i).amount_approx" />
        </div>
        <div class="input unit">
          <input
            v-model="ingredient.unit"
            :disabled="saving || ingredient.amount_type !== AMOUNT_TYPE_NUMERIC"
            :class="{'form-error': !!recipeIngredientError(i).unit.length}"
            :placeholder="$t('recipe_edit.unit')"
          >
          <FormFieldValidationError :errors="recipeIngredientError(i).unit" />
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
        <div class="optional">
          <span>{{ $t('recipe_edit.optional') }}</span>
          <input
            v-model="ingredient.optional"
            type="checkbox"
            :disabled="saving"
          >
        </div>
        <!--
          It is fine to only show the remove button, if the form is not empty.
          Only if anything is in group, it makes any sense to offer the user such a button.
        -->
        <button
          v-if="!isEmpty"
          :disabled="saving"
          tabindex="-1"
          class="btn"
          @click="dirty.ingredients.splice(i, 1)"
        >
          {{ $t('recipe_edit.remove') }}
        </button>
      </div>
    </div>
    <button
      :disabled="saving"
      class="btn right"
      @click.prevent="addIngredient"
    >
      {{ $t('recipe_edit.add_ingredient') }}
    </button>
    <!--
      We will only show the button that allows removal of the whole group,
      if the group is already empty. This helps to prevent users from removing
      a group in error.
    -->
    <button
      v-if="isEmpty"
      :disabled="saving"
      class="btn right"
      @click.prevent="removeGroup"
    >
      {{ $t('recipe_edit.remove_group') }}
    </button>
    <div style="clear:both" />
  </div>
</template>

<script>
import IngredientInput from '@/components/utils/IngredientInput'
import FormFieldValidationError from '@/components/utils/FormFieldValidationError'

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
            // There is always the literal string entered by the user in
            // "amount_approx". To handle cases like when the user entered
            // "0.", we prefer displaying "amount_approx", because
            // "amount_numeric" is "0", although the user just entered a dot.
            if (
                (typeof ingredient.amount_approx !== "undefined")
                && (ingredient.amount_approx !== ""))
            {
              return ingredient.amount_approx
            } else {
              return String(ingredient.amount_numeric)
            }
          case this.AMOUNT_TYPE_APPROX:
            if (typeof ingredient.amount_approx === "string") {
              return ingredient.amount_approx
            } else if (ingredient.amount_approx === null) {
              return ""
            } else {
              return String(ingredient.amount_approx)
            }
          default:
            return 'broken'
        }
      }
    },
    isEmpty () {
      // either there is no ingredient or there is exactly one, that matches the empty object in every respect
      return this.dirty.ingredients.length === 0 ||
        (this.dirty.ingredients.length === 1 && Object.entries(this.createEmptyIngredient()).every((([k, v]) => this.dirty.ingredients[0][k] == v)))
    },
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
          this.$refs.ingredientsNode[pos].children[0].children[0].focus()
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
      const numberRegex = /(\d*),(\d*)/
      let valueForNumber = value
      if (numberRegex.test(valueForNumber)) {
        valueForNumber = valueForNumber.replace(numberRegex, "$1.$2")
      }
      const num = Number(valueForNumber)
      if ((value !== "") && !Number.isNaN(num)) {
        ingredient.amount_type = this.AMOUNT_TYPE_NUMERIC
        ingredient.amount_numeric = num
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

.table {
  background: rgba(184, 203, 214, 0.4);
  padding: 5px;
  margin: 10px 0 10px 0;
}

/* Description if this is a group */
.title {
  margin: 0 0 10px 0;
}

/* On desktops make grid layouts for header and ingredients */
.header, .ingredient {
  display: grid;
  grid-template-columns:  2fr 1fr 3fr 3fr 1fr 1fr;
  grid-gap: 2px;

  width: 100%;
  margin: 0 0 2px 0;
}


@media screen and (max-width: 500px) {
   /* Don't display description at the top of the ingredient table on desktops */
    span {
      display: none;
    }
}

.ingredient {
  .optional {
    /* Hide description of optional button on table view */
    span {
      display: none;
    }
  }

  /* Buttons have the same height as inputs */
  .btn {
    margin: 0;
    height: 30px;
  }

  /* Collapse view on smartphones */
  @media screen and (max-width: 500px) {
    display: flex;
    flex-wrap: wrap;
    margin: 0 0 10px 0;
    border-bottom: solid 1px #97A7B0;
    padding-bottom: 5px;

    /* Button goes beside optional div */
    button {
      width: calc(50% - 1px);
      margin: 1px 0 auto 0 !important;
    }

    .input {
      margin: 1px auto 1px auto;

      /* Fill one row with unit and amount */
      &.unit, &.amount {
        width: calc(50% - 1px);
      }

      &.unit {
        margin-right: 0;
      }

      &.amount {
        margin-left: 0;
      }
    }

    /* Optional's label and button are a flexbox themselve. */
    .optional {
      display: flex;
      justify-content: center;
      width: calc(50% - 1px);

      /* Show label on collapsed view */
      span {
        display: initial;
      }

      span, input {
        margin: auto 2px auto 2px;
      }
    }
  }
}

/* Always fill boxes, since layout is defined as flex or grid */
.input {
  width: 100%;
}

/* Checkboxes are not centered otherwise */
input[type=checkbox] {
  width: 14px;
  height: 14px;
}
</style>
