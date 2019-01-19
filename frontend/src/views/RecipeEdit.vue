<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error loading data</div>
  <article v-else-if="recipe">
    <header>
      <input v-model="recipe.title">
    </header>

    <table>
      <thead>
        <tr>
          <th>Amount</th>
          <th>Ingredient</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ingredient in recipe.recipe_ingredients" :key="ingredient.ingredient">
          <td><input v-model="ingredient.amount_numeric">&nbsp;<input v-model="ingredient.unit"></td>
          <td><input v-model="ingredient.ingredient"></td>
        </tr>
      </tbody>
    </table>
    <button @click.prevent="addIngredient">Add</button>

    <p><textarea v-model="recipe.instructions"></textarea></p>

    <footer>
      <p>posted by {{ user }}</p>
    </footer>

    <button @click.prevent="save">Save</button>
  </article>
  <div v-else>No result</div>
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
      return 'unknown'
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
        const r = await api(endpoints.post_recipe(this.recipeId), d)
        if (r.ok) {
          this.recipe = await r.json()
          // TODO: Notify user about success.
        } else {
          // TODO: Notify user about broken fields?
        }
      } catch (err) {
        // TODO: Notify user about network error.
      }
    }
  }
}
</script>
