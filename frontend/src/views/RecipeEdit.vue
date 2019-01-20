<template>
  <div v-if="loading">{{ $t('recipe_edit.loading') }}</div>
  <div v-else-if="error">{{ $t('recipe_edit.loading_error') }}</div>
  <article v-else-if="recipe">
    <header>
      <div><input v-model="recipe.title" :disabled="saving" :class="{'form-error': !!errors.title.length}"></div>
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
        <tr v-for="(ingredient, i) in recipe.recipe_ingredients" :key="i">
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
          <td><button :disabled="saving" @click="recipe.recipe_ingredients.splice(i)">{{ $t('recipe_edit.remove') }}</button></td>
        </tr>
      </tbody>
    </table>
    <button @click.prevent="addIngredient" :disabled="saving">{{ $t('recipe_edit.add') }}</button>

    <div>
      <div><textarea v-model="recipe.instructions" :disabled="saving"></textarea></div>
      <form-field-validation-error :errors="errors.instructions" />
    </div>

    <footer>
      <p>{{ $t('recipe_edit.posted_by',  {user: user}) }}</p>
    </footer>

    <div><button @click.prevent="save" :disabled="saving">{{ $t('recipe_edit.save') }}</button></div>
    <div v-if="errors.client_side">{{ errors.client_side }}</div>
  </article>
  <div v-else>{{ $t('recipe_edit.no_data') }}</div>
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
  components: {
    FormFieldValidationError,
  },
  data () {
    return {
      loading: false,
      error: false,
      errors: {
        title: [],
        recipe_ingredients: [],
        instructions: [],
        client_side: '',
      },
      saving: false,
      recipe: {},
    }
  },
  mounted () {
    this.update()
  },
  computed: {
    recipeId () {
      return this.$route.params.id
    },
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
    }
  },
  methods: {
    addIngredient () {
      this.recipe.recipe_ingredients.push({ingredient: '', ingredient_extra: '', amount_numeric: 0, unit: ''})
    },
    async update () {
      if (!this.recipeId) {
        return
      }
      try {
        this.loading = true
        const r = await api(endpoints.fetch_recipe(this.recipeId))
        this.loading = false
        if (r.ok) {
          this.recipe = await r.json()
        } else {
          throw new Error("Display some kind of error")
        }
      } catch (err) {
        // TODO: Display some kind of error
        this.error = true
      }
    },
    async save () {
      this.saving = true
      const ri = this.recipe.recipe_ingredients.map(i => {
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
        title: this.recipe.title,
        instructions: this.recipe.instructions,
        recipe_ingredients: ri,
      }
      try {
        const r = await api(endpoints.post_recipe(this.recipeId), d, {method:'put'})
        if (r.ok) {
          this.errors.client_side = ''
          this.recipe = await r.json()
          // TODO: Notify user about success.
          this.$router.push({
            name: 'recipe-detail',
            params: {
              id: this.$route.params.id,
            },
          })
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
