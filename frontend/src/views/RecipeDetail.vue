<template>
  <article>
    <header>
      <h1>{{ title }}</h1>
    </header>

    <table>
      <thead>
        <tr>
          <th>Amount</th>
          <th>Ingredient</th>
        </tr>
      </thead>
      <tbody v-if="recipe && recipe.recipeIngredients">
        <tr v-for="ingredient in recipe.recipeIngredients.edges">
          <td>{{ ingredient.node.amountNumeric }}&nbsp;{{ ingredient.node.unit.code }}</td>
          <td>{{ ingredient.node.ingredient.name }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="recipe">{{ recipe.instructions }}</p>

    <footer>
      <p>posted by {{ user }}</p>
    </footer>
  </article>
</template>

<script>
import gql from 'graphql-tag'

export default {
  apollo: {
    recipe: {
      query: gql`query recipe($id: ID!) {
          recipe: recipe(id: $id) {
            title
            instructions
            publishedOn
            recipeIngredients {
              edges {
                node {
                  ingredient {name}
                  amountType
                  amountApprox
                  amountNumeric
                  unit {
                    code
                  }
                }
              }
            }
          }
        }`,
      variables() {
        return {
          id: this.$route.params.id
        }
      },
      skip () {
        return !this.$route.params.id
      }
    }
  },
  computed: {
    title () {
      return this.recipe && this.recipe.title
    },
    user () {
      return 'unknown'
    }
  }
}
</script>
