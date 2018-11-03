<template>
  <ApolloQuery
    :query="require('../graphql/Recipe.gql')"
    :variables="{ id: recipeId }"
  >
    <template slot-scope="{ result: { loading, error, data } }">
      <div v-if="loading">Loading...</div>
      <div v-else-if="error">Error loading data</div>
      <article v-else-if="data && data.recipe">
        <header>
          <h1>{{ data.recipe.title }}</h1>
        </header>

        <table>
          <thead>
            <tr>
              <th>Amount</th>
              <th>Ingredient</th>
            </tr>
          </thead>
          <tbody v-if="data.recipe && data.recipe.recipeIngredients">
            <tr v-for="ingredient in data.recipe.recipeIngredients.edges" :key="ingredient.node.ingredient.name">
              <td>{{ ingredient.node.amountNumeric }}&nbsp;{{ ingredient.node.unit.code }}</td>
              <td>{{ ingredient.node.ingredient.name }}</td>
            </tr>
          </tbody>
        </table>

        <p v-if="data.recipe">{{ data.recipe.instructions }}</p>

        <footer>
          <p>posted by {{ user }}</p>
        </footer>
      </article>
      <div v-else>No result</div>
    </template>
  </ApolloQuery>
</template>

<script>
export default {
  computed: {
    recipeId () {
      return this.$route.params.id
    },
    user () {
      return 'unknown'
    }
  }
}
</script>
