<template>
  <div>
    <h1>{{ ingredient.name }}</h1>
    <IngredientSynonymInput
      v-if="ingredient.synonyms"
      v-model="ingredient.synonyms"
    />

    <table>
      <thead>
        <tr>
          <th>Name</th>
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
      class="btn right"
      @click="submit()"
    >
      Save
    </button>
  </div>
</template>

<script>
import { api, endpoints } from '@/api'

import IngredientSynonymInput from '@/components/IngredientSynonymInput'

export default {
  components: {
    IngredientSynonymInput,
  },
  data () {
    return {
      ingredient: {}
    }
  },
  computed: {
    getId () {
      return this.$route.params.id
    }
  },
  watch: {
    getId() {
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
        const r = await api(endpoints.fetch_ingredient(this.getId))
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
          endpoints.fetch_ingredient(this.getId),
          {
            tags: this.ingredient.tags,
            synonyms: this.ingredient.synonyms
          },
          {
            method: 'PUT'
          }
        )

        if (r.ok) {
          this.ingredient = await r.json()
        }
      } catch (err) {
        console.log(err)
      }
    }
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/table.scss';
</style>
