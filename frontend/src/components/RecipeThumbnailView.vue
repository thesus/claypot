<template>
  <div>
    <div
      class="recipes"
      :class="{small}"
    >
      <div
        v-for="recipe in $props.recipes"
        :key="recipe.id"
        class="recipe-container"
      >
        <slot
          name="overlay"
          :recipe="recipe"
        />
        <router-link
          :to="to(recipe.id)"
        >
          <div class="recipe">
            <div class="info">
              {{ recipe.title }}
            </div>
            <div class="image">
              <img
                v-if="recipe.thumbnail"
                :src="recipe.thumbnail"
              >
              <span v-else>{{ $t('thumbnail.empty') }}</span>
            </div>
          </div>
        </router-link>
      </div>
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
    },
    small: {
      type: Boolean,
      default: false,
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
  justify-content: center;
  position: relative;
  grid-gap: 15px;

  &.small {
    grid-template-columns: repeat(auto-fill, 220px);
  }
}


.recipe-container {
  position: relative;

  & > a {
    display: block;
  }
}

.recipe {
  padding: 5px;
  border: solid 1px #ccc;

  .info {
    width: 100%;
    margin-bottom: 3px;
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

.recipes.small .recipe .image {
  /* 220px is the original height.T
  The original width of 330px was reduced to 220px.
  This results in the same ratio. */
  height: calc(220px*220/330);
}
</style>
