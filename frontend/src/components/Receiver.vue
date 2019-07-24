<template>
  <div>
    <span v-if="loading">{{ $t('generic.loading') }}</span>
    <span v-if="error">{{ error }}</span>

    <slot
      v-if="results"
      :data="results"
    />
    <span v-else-if="!working"><slot name="noData">{{ $t('generic.no_data') }}</slot></span>
  </div>
</template>


<script>
import { api } from '@/api'

import { Timer } from '@/utils'

export default {
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
    },
    transform: {
      type: Function,
      default: null,
    },
    reloadTrigger: {
      type: Number,
      default: 0,
    },
    forcePaginator: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      loading: false,
      working: false,
      error: null,
      results: null,

      next: null,
      previous: null,
      count: 0
    }
  },
  computed: {
    pagination () {
      return {
        count: this.count,
        next: this.next,
        previous: this.previous
      }
    }
  },
  watch: {
    filters: {
      handler () {
        this.get()
      },
      deep: true
    },
    reloadTrigger () {
      this.get()
    },
    pagination () {
      this.$emit('pagination', this.pagination)
    }
  },
  mounted () {
    this.get()
  },
  methods: {
    async get () {
      this.working = true
      const timer = new Timer(() => { this.loading = true }, 200)
      try {
        const page = this.isList ? { page: 1 } : {}

        const r = await api(
          this.endpoint,
          { ...page, ...this.filters },
          { method: 'GET' }
        )
        const data = await r.json()
        if (r.ok) {
          let relevantData
          if (this.isList) {
            relevantData = data.results.length > 0 ? data.results : null
          } else {
            relevantData = data
          }
          if (this.transform !== null) {
            relevantData = this.transform(relevantData)
          }
          this.$set(this, 'results', relevantData)

          if (this.isList && data) {
            this.$set(this, 'next', data.next)
            this.$set(this, 'previous', data.previous)
          }
        } else {
          throw new Error(data['detail'])
        }
      } catch (err) {
        this.error = err.message

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
