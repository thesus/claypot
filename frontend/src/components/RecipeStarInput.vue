<template>
  <div v-if="value">
    <span>{{ $t('recipes.starred') }}</span>
    <button class="btn" @click="doUnstar" :disabled="saving">{{ $t('recipes.unstar') }}</button>
  </div>
  <button v-else class="btn" @click="doStar" :disabled="saving">{{ $t('recipes.star') }}</button>
</template>

<script>
import {api, endpoints} from '@/api'

export default {
  name: 'recipe-star-input',
  props: {
    recipeId: String,
    value: Boolean,
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
@import '@/modules/inputs.scss';
</style>
