<template>
  <div class="recipes">
    <div
        v-for="recipe in $props.recipes"
        :key="recipe.id"
        class="recipe-container"
    >
      <div class="toolbelt">
        <slot name="toolbelt">
          <button class="btn">-</button>
        </slot>
      </div>
      <router-link
        :to="to(recipe.id)"
      >
        <div class="recipe">
          <div class="info">
            {{ recipe.title }}
          </div>
          <div class="image">
            <img v-if="recipe.thumbnail" :src="recipe.thumbnail">
            <span v-else>{{ $t('thumbnail.empty') }}</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecipeThumbnailView',
  props: {
    recipes: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    to (id) {
      return {
        name: 'recipe-detail',
        params: {
          id: id
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/variables.scss';
@import '@/modules/inputs.scss';

a {
  text-decoration: none;
  color: $font_color;
}

.recipes {
  display: grid;
  grid-template-columns: repeat(auto-fill, 330px);
  justify-content: space-around;
}

.recipe-container {
  position: relative;
}

.toolbelt {
  display: inline;
  position: absolute;
  right: 8px;
  top: 8px;
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
    width: 100%;
    height: 220px;
    overflow: hidden;

    img {
      height: 100%;
      width: 100%;

      object-fit: cover;
    }

    span {
      padding-top: 70px;
      text-decoration: none !important;
      display: block;
    }
  }
}
</style>
