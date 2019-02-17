<template>
  <div v-if="value">
    <div
      :disabled="saving"
      class="button starred"
      @click="doUnstar"
    >
      {{ $t('recipes.unstar') }}
    </div>
  </div>
  <div
    v-else
    :disabled="saving"
    class="button"
    @click="doStar"
  >
    {{ $t('recipes.star') }}
  </div>
</template>

<script>
import {api, endpoints} from '@/api'

export default {
  name: 'RecipeStarInput',
  props: {
    recipeId: {
      type: Number,
      required: true,
    },
    value: {
      type: Boolean,
      default: false,
    }
  },
  data () {
    return {
      saving: false,
    }
  },
  methods: {
    async doStar () {
      this.saving = true
      try {
        const response = await api(endpoints.recipe_star(this.recipeId), null, {method: 'post'})
        const result = await response.json()
        if (response.ok) {
          this.$emit('input', result)
        } else {
          // TODO: error handling
        }
      } finally {
        this.saving = false
      }
    },
    async doUnstar () {
      this.saving = true
      try {
        const response = await api(endpoints.recipe_unstar(this.recipeId), null, {method: 'post'})
        const result = await response.json()
        if (response.ok) {
          this.$emit('input', result)
        } else {
          // TODO: error handling
        }
      } finally {
        this.saving = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/variables.scss';

.button {
  cursor: pointer;
  display: inline-block;

  &:hover {
    background-color: $font_color;
    color: white;
  }
}
</style>
