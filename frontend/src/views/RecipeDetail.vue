<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error loading data</div>
  <article v-else-if="recipe">
    <header>
      <h1>{{ recipe.title }}</h1>
    </header>

    <router-link :to="{name: 'recipe-edit', param: {id: recipeId}}">Edit</router-link>

    <table>
      <thead>
        <tr>
          <th>Amount</th>
          <th>Ingredient</th>
        </tr>
      </thead>
      <tbody v-if="recipe && recipe.recipe_ingredients">
        <tr v-for="ingredient in recipe.recipe_ingredients" :key="ingredient.ingredient">
          <td>{{ ingredient.amount_numeric }}&nbsp;{{ ingredient.unit.code }}</td>
          <td>{{ ingredient.ingredient.name }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="recipe">{{ recipe.instructions }}</p>

    <footer>
      <p>posted by {{ user }}</p>
    </footer>
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
      recipe: {
      }
    }
  },
  mounted () {
    this.update()
  },
  methods: {
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
    }
  },
  computed: {
    recipeId () {
      return this.$route.params.id
    },
    user () {
      return 'unknown'
    }
  },
  watch: {
    recipeId() {
      this.update()
    }
  }
}
</script>
