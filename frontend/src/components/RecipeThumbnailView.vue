<template>
  <div class="recipes">
    <div
      v-for="recipe in $props.recipes"
      :key="recipe.id"
      class="recipe"
      >
      <div class="info">
        <recipe-link :recipe="recipe" />
      </div>
      <div class="image" v-if="recipe.thumbnail">
        <img :src="recipe.thumbnail">
      </div>
    </div>
  </div>
</template>

<script>
import RecipeLink from '@/components/RecipeLink'

export default {
  name: 'RecipeThumbnailView',
  components: {
    RecipeLink
  },
  props: {
    recipes: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style lang="scss" scoped>
.recipes {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.recipe {
  padding: 5px;
  margin: 5px;

  border: solid 1px #ccc;

  .info {
    width: 100%;
    margin-bottom: 3px;

    background-color: white;
  }

  .image {
    width: 300px;
    height: 200px;

    img {
      height: 100%;
      width: 100%;

      object-fit: cover;
    }
  }
}
</style>
