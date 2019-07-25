<template>
  <div>
    <span v-if="loading">{{ $t('generic.loading') }}</span>
    <span v-if="error">{{ error }}</span>

    <slot
      v-if="results"
      :data="results"
    />

    <span v-else-if="!working"><slot name="noData">{{ $t('generic.no_data') }}</slot></span>

    <Pagination
      v-if="hasPagination"
      :next="next"
      :previous="previous"
      @update="setPage"
    />
  </div>
</template>


<script>
import { api } from '@/api'

import { Timer } from '@/utils'

import Pagination from '@/components/Pagination'

export default {
  components: {Pagination},
  props: {
    endpoint: {
      type: Object,
      required: true
    },
    filters: {
      type: Object,
      default: () => ({})
    },
    /* Expect multiple results in a nested response */
    isList: {
      type: Boolean,
      default: true
    },
    /* Function that is applied to data before passing them to slots */
    transform: {
      type: Function,
      default: null,
    },
    reloadTrigger: {
      type: Number,
      default: 0,
    },
    /* Removes pagination completely */
    hasPagination: {
      type: Boolean,
      default: true
    },
    /* page is stored in url history */
    hasUrlPages: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      loading: false,
      working: false,
      error: null,
      results: null,

      next: null,
      previous: null,
      count: 0,
      simplePage: 0
    }
  },
  computed: {
    page: {
      get () {
        return (this.hasUrlPages ? this.$route.query.page : this.simplePage) || 1
      },
      set (value) {
        /* Store page in url otherwise in 'simplePage' data */
        if (this.hasUrlPages) {
          this.$router.push({
            name: this.$route.name,
            params: this.$route.params,
            query: { ...this.$route.query, page: value }
          })
        } else {
          this.simplePage = value
        }
      }
    },
    combinedFilters () {
      /* Merge page in filters if list mode is enabled */
      const d = this.isList ? { page: this.page } : { }

      return {
        ...this.filters,
        ...d
      }
    }
  },
  watch: {
    /* Reset the page to one if the filter changes */
    filters: {
      handler () {
        if (this.isList) {
          this.page = 1
        }
      },
      deep: true
    },
    /* Fetch data after page or filter change */
    combinedFilters: {
      handler () {
        this.get()
      },
      deep: true
    },
    reloadTrigger () {
      this.get()
    }
  },
  mounted () {
    this.get()
  },
  methods: {
    async get () {
      this.working = true
      /* Show loading indicator after 200ms */
      const timer = new Timer(() => { this.loading = true }, 200)
      try {

        const r = await api(
          this.endpoint,
          this.combinedFilters,
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
            this.$set(this, 'count', data.count)
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
    },
    setPage (value) {
      this.page = value
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
