<template>
  <ApolloQuery
    :query="require('../graphql/RecipeList.gql')"
  >
    <template slot-scope="{ result: { loading, error, data } }">
      <div v-if="loading">Loading</div>
      <ul v-else-if="data && data">
        <li v-for="item in data.recipes.edges" :key="item.node.id">
          <recipe-link :recipe="item.node"/>
        </li>
      </ul>
    </template>
  </ApolloQuery>
</template>

<script>
import RecipeLink from '@/components/RecipeLink'

export default {
  name: 'home',
  components: {
    RecipeLink
  }
}
</script>
