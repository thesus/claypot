<template>
  <div
    class="table group"
  >
    <input
      v-if="!single"
      v-model="group.title"
      placeholder="Ingredient group title"
      class="title"
    >
    <div
      v-show="group.ingredients.length > 0"
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
        v-for="(ingredient, i) in group.ingredients"
        ref="ingredientsNode"
        :key="i"
        class="ingredient"
      >
        <div class="input amount">
          <input
            :value="displayAmount(ingredient)"
            :class="{'form-error': !!recipeIngredientError(i).amount_numeric.length || !!recipeIngredientError(i).amount_numeric.length}"
            @input="updateAmount(ingredient, $event.target.value)"
          >
          <FormFieldValidationError :errors="recipeIngredientError(i).amount_numeric" />
          <FormFieldValidationError :errors="recipeIngredientError(i).amount_approx" />
        </div>
        <div class="input unit">
          <input
            v-model="ingredient.unit"
            :disabled="!isNumeric(ingredient.amount_type)"
            :class="formError(i, 'unit')"
            :placeholder="$t('recipe_edit.unit')"
          >
          <FormFieldValidationError :errors="recipeIngredientError(i).unit" />
        </div>
        <div class="input">
          <IngredientInput
            v-model="ingredient.ingredient"
            :class="formError(i, 'ingredient')"
          />
          <FormFieldValidationError :errors="recipeIngredientError(i).ingredient" />
        </div>
        <div class="input">
          <input
            v-model="ingredient.ingredient_extra"
            :class="formError(i, 'ingredient_extra')"
            :placeholder="$t('recipe_edit.ingredient_extra')"
          >
          <FormFieldValidationError :errors="recipeIngredientError(i).ingredient_extra" />
        </div>
        <div class="optional">
          <span>{{ $t('recipe_edit.optional') }}</span>
          <input
            v-model="ingredient.optional"
            type="checkbox"
          >
        </div>
        <!--
          It is fine to only show the remove button, if the form is not empty.
          Only if anything is in group, it makes any sense to offer the user such a button.
        -->
        <button
          tabindex="-1"
          class="btn"
          @click="group.ingredients.splice(i, 1)"
        >
          {{ $t('recipe_edit.remove') }}
        </button>
      </div>
    </div>
    <button
      class="btn right"
      @click.prevent="addIngredient"
    >
      {{ $t('recipe_edit.add_ingredient') }}
    </button>
    <div style="clear:both" />
  </div>
</template>

<script>
import IngredientInput from '@/components/utils/IngredientInput'
import FormFieldValidationError from '@/components/utils/FormFieldValidationError'
import { createEmptyIngredient, AMOUNT_TYPE_NUMERIC, AMOUNT_TYPE_APPROX } from '@/components/recipe-edit/utils'

export default {
  name: 'RecipeEditIngredientTable',
  components: {
    FormFieldValidationError,
    IngredientInput,
  },
  props: {
    group: {
      type: Object,
      required: true
    },
    single: {
      type: Boolean,
      default: false
    },
    recipeIngredientError: {
      type: Function,
      default: function () {
        return function () {}
      }
    }
  },
  computed: {
    displayAmount () {
      return ingredient => {
        switch (ingredient.amount_type) {
          case AMOUNT_TYPE_NUMERIC:
            return ingredient.amount_numeric
          case AMOUNT_TYPE_APPROX:
            return ingredient.amount_approx
          default:
            return 'broken'
        }
      }
    },
    isEmpty () {
      return !this.group.ingredients.length
    }
  },
  watch: {
    isEmpty () {
      // The group can't exist if there are no ingredients
      if (this.isEmpty) {
        this.$emit('remove')
      }
    }
  },
  methods: {
    isNumeric (amount_type) {
      return amount_type === AMOUNT_TYPE_NUMERIC
    },
    formError (index, key) {
      return {
        'form-error': !!this.recipeIngredientError(index)[key].length
      }
    },
    addIngredient () {
      this.group.ingredients.push(createEmptyIngredient())

      const pos = this.group.ingredients.length - 1
      // Select the first field in the input after it was created
      // And yeah. This is pretty dirty.
      this.$nextTick(() => {
        if (this.$refs.ingredientsNode) {
          this.$refs.ingredientsNode[pos].children[0].children[0].focus()
        }
      })
    },
    updateAmount (ingredient, value) {
      const numberRegex = /(\d*),(\d*)/
      let possibleNumber = value;

      if (numberRegex.test(possibleNumber)) {
        possibleNumber = possibleNumber.replace(numberRegex, "$1.$2")
      }

      const number = Number(possibleNumber)
      const isApprox = Number.isNaN(number)

      ingredient.amount_type = isApprox ? AMOUNT_TYPE_APPROX : AMOUNT_TYPE_NUMERIC
      ingredient.amount_approx = isApprox ? value : null
      ingredient.amount_numeric = isApprox ? null : number
    }
  }
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
