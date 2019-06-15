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
      <div class="image">
        <img v-if="recipe.thumbnail" :src="recipe.thumbnail">
        <span v-else>{{ $t('thumbnail.empty') }}</span>
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

    span {
      padding-top: 70px;
      display: block;
    }
  }
}
</style>
