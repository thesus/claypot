/* Handles a few pagination related tasks */
/* TODO (till): Add description */

const PaginationMixin = {
  data () {
    return {
      next: null,
      previous: null,
      count: 0,
      simplePage: 1
    }
  },
  computed: {
    simpleMode () {
      return (this.simple != undefined) ? this.simple : true
    },
    combinedFilters () {
      return {
        ...this.filters,
        page: this.page
      }
    },
    page: {
      get () {
        return (this.simpleMode ? this.simplePage : this.$route.query.page) || 1
      },
      set (value) {
        console.log(this.simpleMode)
        if (this.simpleMode) {
          this.simplePage = value
        } else {
          this.$router.push({ name: this.$route.name, query: { page: value } })
        }
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

export { PaginationMixin }
