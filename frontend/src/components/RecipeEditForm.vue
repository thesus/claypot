<template>
  <article>
    <header>
      <div><input v-model="recipe_dirty.title" :disabled="saving" :class="{'form-error': !!errors.title.length}"></div>
      <form-field-validation-error :errors="errors.title" />
    </header>

    <table>
      <thead>
        <tr>
          <th>{{ $t('recipe_edit.amount') }}</th>
          <th>{{ $t('recipe_edit.unit') }}</th>
          <th>{{ $t('recipe_edit.ingredient') }}</th>
          <th>{{ $t('recipe_edit.ingredient_extra') }}</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(ingredient, i) in recipe_dirty.recipe_ingredients" :key="i">
          <td>
            <div><input v-model="ingredient.amount_numeric" :class="{'form-error': !!recipeIngredientError(i).amount_numeric.length}"></div>
            <form-field-validation-error :errors="recipeIngredientError(i).amount_numeric" />
          </td>
          <td>
            <div><input v-model="ingredient.unit" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).unit.length}"></div>
            <form-field-validation-error :errors="recipeIngredientError(i).unit" />
          </td>
          <td>
            <div><input v-model="ingredient.ingredient" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).ingredient.length}"></div>
            <form-field-validation-error :errors="recipeIngredientError(i).ingredient" />
          </td>
          <td>
            <input v-model="ingredient.ingredient_extra" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).ingredient_extra.length}">
            <form-field-validation-error :errors="recipeIngredientError(i).ingredient_extra" />
          </td>
          <td><button :disabled="saving" @click="recipe_dirty.recipe_ingredients.splice(i)">{{ $t('recipe_edit.remove') }}</button></td>
        </tr>
      </tbody>
    </table>
    <button @click.prevent="addIngredient" :disabled="saving">{{ $t('recipe_edit.add') }}</button>

    <div>
      <div><textarea v-model="recipe_dirty.instructions" :disabled="saving"></textarea></div>
      <form-field-validation-error :errors="errors.instructions" />
    </div>

    <footer>
      <p>{{ $t('recipe_edit.posted_by',  {user: user}) }}</p>
    </footer>

    <div><button @click.prevent="save" :disabled="saving">{{ $t('recipe_edit.save') }}</button></div>
    <div v-if="errors.client_side">{{ errors.client_side }}</div>
  </article>
</template>

<script>
import {api, endpoints} from '@/api'
import FormFieldValidationError from '@/components/FormFieldValidationError'

const amount_types = {
  none: 1,
  numeric: 2,
  approx: 3,
}

export default {
  name: 'recipe-edit-form',
  components: {
    FormFieldValidationError,
  },
  props: {
    recipe: Object,
  },
  data () {
    return {
      recipe_dirty: {},
      saving: false,
      errors: {
        title: [],
        recipe_ingredients: [],
        instructions: [],
        client_side: '',
      },
    }
  },
  computed: {
    user () {
      return this.$t('recipe_edit.unknown_user')
    },
    recipeIngredientError () {
      return i => {
        const e = this.errors.recipe_ingredients
        const r = e.length > i ? e[i] : {}
        for (let p of ['ingredient', 'ingredient_extra', 'amount_numeric', 'unit']) {
          r[p] = r[p] || []
        }
        return r
      }
    },
  },
  methods: {
    addIngredient () {
      this.recipe_dirty.recipe_ingredients.push({ingredient: '', ingredient_extra: '', amount_numeric: 0, unit: ''})
    },
    async save () {
      this.saving = true
      const ri = this.recipe_dirty.recipe_ingredients.map(i => {
        return {
          ingredient: i.ingredient,
          ingredient_extra: '',
          optional: false,
          amount_type: amount_types.numeric,
          amount_numeric: Number(i.amount_numeric),
          amount_approx: '',
          unit: i.unit,
        }
      })
      const d = {
        title: this.recipe_dirty.title,
        instructions: this.recipe_dirty.instructions,
        recipe_ingredients: ri,
      }
      try {
        const r = await api(endpoints.post_recipe(this.recipe.id), d, {method:'put'})
        if (r.ok) {
          this.errors.client_side = ''
          this.recipe_dirty = await r.json()
          // TODO: Notify user about success.
          this.$emit('input', this.recipe_dirty)
        } else {
          // TODO: Notify user about broken fields?
          const errors = await r.json()
          this.errors.title = errors.title || []
          this.errors.recipe_ingredients = errors.recipe_ingredients || []
          this.errors.instructions = errors.instructions || []
        }
      } catch (err) {
        this.errors.client_side = err.message
      }
      this.saving = false
    },
  },
  watch: {
    recipe () {
      const r = this.recipe
      this.recipe_dirty = {
        title: r.title,
        recipe_ingredients: [],
        instructions: r.instructions,
      }
      for (let ri of r.recipe_ingredients) {
        this.recipe_dirty.recipe_ingredients.push({
          amount_numeric: ri.amount_numeric,
          amount_approx: ri.amount_approx,
          amount_type: ri.amount_type,
          ingredient: ri.ingredient,
          ingredient_extra: ri.ingredient_extra,
          unit: ri.unit,
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

table {
  width: 100%;
}
</style>
