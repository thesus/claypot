<template>
  <ul v-if="recipes">
    <li>
      <recipe-link :recipe="item.node" v-for="item in recipes.edges" :key="item.node.id"/>
    </li>
  </ul>
</template>

<script>
import gql from 'graphql-tag'
import RecipeLink from '@/components/RecipeLink'

export default {
  name: 'home',
  components: {
    RecipeLink
  },
  apollo: {
    recipes: gql`query {
          recipes {
            edges {
              node {
                id
                title
                instructions
                recipeIngredients {
                  edges {
                    node {
                      id
                      ingredient {
                        name
                      }
                      amountType
                      amountNumeric
                      amountApprox
                      unit {
                        id
                        name
                        code
                        namePlural
                      }
                    }
                  }
                }
              }
            }
          }
        }`
  }
}
</script>
