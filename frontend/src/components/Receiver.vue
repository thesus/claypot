<template>
  <div>
    <span v-if="loading">{{ $t('generic.loading') }}</span>
    <span v-if="error">{{ error }}</span>

    <slot
      v-if="results"
      :data="results"
    />
    <span v-else-if="!working">{{ $t('generic.no_data') }}</span>

    <Pagination
      v-if="isList && results"
      :next="next"
      :previous="previous"
      @input="updateLink"
    />
  </div>
</template>


<script>
import { api } from '@/api'

import { Timer } from '@/utils'

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
      loading: false,
      working: false,
      error: null,
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
    filters: {
      handler () {
        this.get()
      },
      deep: true
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
      this.working = true
      const timer = new Timer(() => { this.loading = true }, 200)
      try {
        const r = await api(
          this.endpoint,
          { ...this.filters, page: this.page },
          { method: 'GET' }
        )
        const data = await r.json()
        if (r.ok) {
          if (this.isList) {
            this.$set(this, 'results', data.results.length > 0 ? data.results : null)

            this.$set(this, 'next', data['next'])
            this.$set(this, 'previous', data['previous'])
          } else {
            this.$set(this, 'results', data)
          }
        } else {
          throw new Error(data['detail'])
        }
      } catch (err) {
        this.err = err.message

        this.results = null
      } finally {
        timer.clear()
        this.working = false
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
