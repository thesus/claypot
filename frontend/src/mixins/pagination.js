/* Handles a few pagination related tasks */
/* TODO (till): Add description */

const PaginationMixin = {
  data () {
    return {
      next: null,
      previous: null,
      count: 0,
      page: 1
    }
  },
  computed: {
    combinedFilters () {
      return {
        ...this.filters,
        page: this.page
      }
    }
  },
  watch: {
    filters: {
      handler() {
        this.page = 1
      },
      deep: true
    }
  },
  methods: {
    updatePagination (pagination) {
      this.next = pagination.next
      this.previous = pagination.previous
      this.count = pagination.count
    },
    setPage (page) {
      this.page = page
    }
  }
}

const UrlPageMixin = {
  watch: {
    page () {
    }
  }
}

export { PaginationMixin }
