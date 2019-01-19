<template>
  <div v-if="loading">{{ $t('recipe_edit.loading') }}</div>
  <div v-else-if="error">{{ $t('recipe_edit.loading_error') }}</div>
  <article v-else-if="recipe">
    <header>
      <input v-model="recipe.title" :disabled="saving">
    </header>

    <table>
      <thead>
        <tr>
          <th>{{ $t('recipe_edit.amount') }}</th>
          <th>{{ $t('recipe_edit.ingredient') }}</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(ingredient, i) in recipe.recipe_ingredients" :key="i">
          <td><input v-model="ingredient.amount_numeric">&nbsp;<input v-model="ingredient.unit"></td>
          <td><input v-model="ingredient.ingredient" :disabled="saving"></td>
          <td><button :disabled="saving" @click="recipe.recipe_ingredients.splice(i)">{{ $t('recipe_edit.remove') }}</button></td>
        </tr>
      </tbody>
    </table>
    <button @click.prevent="addIngredient" :disabled="saving">{{ $t('recipe_edit.add') }}</button>

    <p><textarea v-model="recipe.instructions" :disabled="saving"></textarea></p>

    <footer>
      <p>{{ $t('recipe_edit.posted_by',  {user: user}) }}</p>
    </footer>

    <button @click.prevent="save" :disabled="saving">{{ $t('recipe_edit.save') }}</button>
  </article>
  <div v-else>{{ $t('recipe_edit.no_data') }}</div>
</template>

<script>
import {api, endpoints} from '@/api'

const amount_types = {
  none: 1,
  numeric: 2,
  approx: 3,
}

export default {
  data () {
    return {
      loading: false,
      error: false,
      saving: false,
      recipe: {}
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
    }
  },
  methods: {
    addIngredient () {
      this.recipe.recipe_ingredients.push({ingredient: '', amount_numeric: 0, unit: ''})
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
        }
      } catch (err) {
        // TODO: Notify user about network error.
      }
      this.saving = false
    }
  }
}
</script>
