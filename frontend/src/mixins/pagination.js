/* Handles a few pagination related tasks */
/* The Receiver component emits an 'pagination' event once the page changes.
 * The number is incorporated in this.filters and can be accessed via
 * 'combinedFilters'. If the filter changes the page is set back to 1.
 * This event can be passed to the 'updatePagination' function and
 * the Pagination component can be setup like in the following example:
 *
 * <Pagination
 *   :next="next"
 *   :previous="previous"
 *   @update="setPage"
 * />
 *
 * If the page should be encoded into the url set 'this.simple' via a prop,
 * computed or data value to false. (defaults to true)
 */

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
