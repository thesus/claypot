<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error loading data</div>
  <article v-else-if="data && data.recipe">
    <header>
      <input v-model="title">
    </header>

    <table>
      <thead>
        <tr>
          <th>Amount</th>
          <th>Ingredient</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ingredient in recipeIngredients" :key="ingredient.name">
          <td><input v-model="ingredient.amountNumeric">&nbsp;<input v-model="ingredient.code"></td>
          <td><input v-model="ingredient.name"></td>
        </tr>
      </tbody>
    </table>
    <button @click.prevent="addIngredient">Add</button>

    <p><textarea v-model="instructions"></textarea></p>

    <footer>
      <p>posted by {{ user }}</p>
    </footer>

    <button @click.prevent="save">Save</button>
  </article>
  <div v-else>No result</div>
</template>

<script>
export default {
  data () {
    return {
      title: '',
      recipeIngredients: [],
      instructions: ''
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
  methods: {
    addIngredient () {
      this.recipeIngredients.push({name: '', amountNumeric: 0, code: ''})
    },
    save () {
      console.log('save')
    }
  }
}
</script>
