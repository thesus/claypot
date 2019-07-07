<template>
  <div>
    <slot
      v-show="results"
      :data="results"
    />
    <Pagination
      v-if="isList"
      :next="next"
      :previous="previous"
      @input="updateLink"
    />
  </div>
</template>


<script>
import { api } from '@/api'

import Pagination from '@/components/Pagination'

export default {
  components: {
    Pagination
  },
  props: {
    endpoint: {
      type: Object,
      required: true
    },
    filters: {
      type: Object,
      default: () => ({})
    },
    isList: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      page: 1,
      results: null,
      next: null,
      previous: null
    }
  },
  watch: {
    page () {
      this.get()
    },
    filters () {
      this.get()
    }
  },
  mounted () {
    this.get()
  },
  methods: {
    updateLink(urlString) {
      const url = new URL(urlString)
      let page = url.searchParams.get('page')
      this.page = page ? page : 1
    },
    async get () {
      try {
        this.loading = true

        const r = await api(
          this.endpoint,
          { ...this.filters, page: this.page },
          { method: 'GET' }
        )

        if (r.ok) {
          const data = await r.json()

          this.$set(this, 'results', data['results'])

          if (this.isList) {
            this.$set(this, 'next', data['next'])
            this.$set(this, 'previous', data['previous'])
          }
        } else {
          throw new Error('error occured')
        }
      } catch (err) {
        // this.error = err.message
        this.results.length = 0
      } finally {
        this.loading = false
      }
    }
  }
}

</script>

<style lang="scss" scoped>

</style>
