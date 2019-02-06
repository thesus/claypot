<template>
  <div class="table" :class="{group: dirty.isGroup}">
    <input v-if="dirty.isGroup" v-model="dirty.title" placeholder="Ingredient group title"/>
    <table v-show="dirty.ingredients.length > 0">
      <thead>
        <tr>
          <th>{{ $t('recipe_edit.amount') }}</th>
          <th>{{ $t('recipe_edit.unit') }}</th>
          <th>{{ $t('recipe_edit.ingredient') }}</th>
          <th>{{ $t('recipe_edit.ingredient_extra') }}</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(ingredient, i) in dirty.ingredients" :key="i" ref="ingredientsNode">
          <td>
            <div class="input">
              <input v-model="ingredient.amount_numeric" :class="{'form-error': !!recipeIngredientError(i).amount_numeric.length}">
            </div>
            <form-field-validation-error :errors="recipeIngredientError(i).amount_numeric" />
          </td>
          <td>
            <div class="input">
              <input v-model="ingredient.unit" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).unit.length}">
            </div>
            <form-field-validation-error :errors="recipeIngredientError(i).unit" />
          </td>
          <td>
            <div class="input">
              <ingredient-input v-model="ingredient.ingredient" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).ingredient.length}" />
            </div>
            <form-field-validation-error :errors="recipeIngredientError(i).ingredient" />
          </td>
          <td>
            <div class="input">
              <input v-model="ingredient.ingredient_extra" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).ingredient_extra.length}">
            </div>
            <form-field-validation-error :errors="recipeIngredientError(i).ingredient_extra" />
          </td>
          <td><button tabindex="-1" class="btn btn-right remove" :disabled="saving" @click="dirty.ingredients.splice(i, 1)">{{ $t('recipe_edit.remove') }}</button></td>
        </tr>
      </tbody>
    </table>
    <button class="btn btn-right submit" @click.prevent="addIngredient" :disabled="saving">{{ $t('recipe_edit.add') }}</button>
    <button class="btn btn-right submit" @click.prevent="removeGroup" :disabled="saving">{{ $t('recipe_edit.remove_group') }}</button>
  </div>
</template>

<script>
import IngredientInput from '@/components/IngredientInput'
import FormFieldValidationError from '@/components/FormFieldValidationError'

export default {
  name: 'recipe-edit-ingredient-table',
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
        isGroup: false,
        title: '',
        ingredients: [],
      },
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
          (this.dirty.isGroup !== this.value.isGroup) ||
          (this.dirty.title !== this.value.title) ||
          (this.dirty.ingredients.some((ingredient, i) => !equalIngredients(this.value.ingredients[i], ingredient)))
        )
        if (changed) {
          this.$emit('input', {
            isGroup: this.dirty.isGroup,
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
      return {ingredient: '', ingredient_extra: '', amount_numeric: 0, unit: ''}
    },
    addIngredient () {
      this.dirty.ingredients.push(this.createEmptyIngredient())

      const pos = this.dirty.ingredients.length - 1
      /* Select the first field in the input after it was created */
      /* And yeah. This is pretty dirty. */
      this.$nextTick(() => { this.$refs.ingredientsNode[pos].children[0].children[0].children[0].focus() })
    },
    updateDirty () {
      this.dirty.isGroup = this.value.isGroup
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
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.table {
  margin-top: 1em;
}
.table:first-child {
  margin-top: 0em;
}

.table.group {
  padding: 1em;
  margin-left: 1em;
  margin-right: 1em;
  border: solid 1px #ccc;
}
</style>
