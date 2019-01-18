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
        <tr v-for="ingredient in recipe.recipe_ingredients" :key="ingredient.ingredient.name">
          <td><input v-model="ingredient.amount_numeric">&nbsp;<input v-model="ingredient.unit.code"></td>
          <td><input v-model="ingredient.ingredient.name"></td>
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
      this.recipeIngredients.push({name: '', amountNumeric: 0, code: ''})
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
    save () {
      console.log('save')
    }
  }
}
</script>
