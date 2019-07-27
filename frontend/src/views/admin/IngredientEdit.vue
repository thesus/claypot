<template>
  <div>
    <IngredientSynonymInput
      v-if="ingredient.synonyms"
      v-model="ingredient.synonyms"
      :errors="errors.synonyms"
    />
    <table v-if="ingredient.tags && ingredient.tags.length > 0">
      <thead>
        <tr>
          <th>{{ $t('ingredient.name') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(value, index) in ingredient.tags"
          :key="index"
        >
          <td>{{ value }}</td>
        </tr>
      </tbody>
    </table>
    <button
      class="btn right save"
      @click="submit()"
    >
      {{ $t('generic.save') }}
    </button>
  </div>
</template>

<script>
import { api, endpoints } from '@/api'

import IngredientSynonymInput from '@/components/ingredient-edit/IngredientSynonymInput'

export default {
  components: {
    IngredientSynonymInput,
  },
  data () {
    return {
      ingredient: {
        name: '',
        synonyms: [],
        tags: []
      },
      locked: false,
      errors: {
        synonyms: {}
      }
    }
  },
  computed: {
    ingredientId () {
      return this.$route.params.id
    }
  },
  watch: {
    ingredientId() {
      this.get()
    }
  },
  mounted () {
    this.get()
  },
  methods: {
    async get() {
      try {
        this.loading = true
        const r = await api(endpoints.fetch_ingredient(this.ingredientId))
        this.loading = false

        if (r.ok) {
          this.ingredient = await r.json()
        } else {
          throw new Error("")
        }
      } catch (err) {
        console.log(err)
        this.error = true
      }
    },
    async submit() {
      try {
        this.locked = true
        const r = await api(
          endpoints.fetch_ingredient(this.ingredientId),
          {
            tags: this.ingredient.tags || [],
            synonyms: this.ingredient.synonyms || []
          },
          {
            method: 'PUT'
          }
        )

        const data = await r.json()
        if (r.ok) {
          this.ingredient = data
          this.$router.push({
            name: 'ingredient-list'
          })
        } else {
          this.$set(this, 'errors', data)
        }
      } catch (err) {
        console.log(err)
      } finally {
        this.locked = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/table.scss';

</style>
