<template>
  <div class="search">
    <div class="option">
      <input
        v-model="filters.search"
        :placeholder="$t('search.textsearch')"
      >
    </div>
    <button
      class="btn"
      @click="toggleExtendedSearch"
    >
      <template v-if="extendedSearchOpen">
        {{ $t('search.close') }}
      </template>
      <template v-else>
        {{ $t('search.open') }}
      </template>
    </button>
    <div
      v-show="extendedSearchOpen"
      class="extended"
    >
      <div class="option">
        <label for="ordering">{{ $t('search.ordering.label') }}</label>
        <select
          id="ordering"
          v-model="filters.ordering"
        >
          <option value="time">
            {{ $t('search.ordering.time') }}
          </option>
          <option value="">
            {{ $t('search.ordering.relevance') }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
import { cleanObject } from '@/utils'
import { mapGetters } from 'vuex'

function isSet (element) {
  return !(element === '' || element === null || element === undefined)
}

export default {
  data () {
    return {
      // Load the filters from the url when mounted
      filters: {
        ordering: this.$route.query.ordering || '',
        search: this.$route.query.search || '',
      },
      debounce: null,
      // Even if the extended search is no longer in use
      // keep the dialog open until it is toggled via the button
      keepOpen: false
    }
  },
  computed: {
    extendedFilters() {
      return {
        ordering: this.filters.ordering
      }
    },
    // Returns true if any of the extendend filtering options is used
    extendedFiltersInUse() {
      return Object.values(this.extendedFilters).some(isSet)
    },
    extendedSearchOpen() {
      return this.keepOpen || this.getExtendedSearch
    },
    ...mapGetters(['getExtendedSearch'])
  },
  watch: {
    // Emit filters with debounce to the parent component
    filters: {
      handler () {
        clearTimeout(this.debounce)
        this.debounce = setTimeout(() => {
          this.$emit('input', { ...this.filters })

          this.$router.push({query: cleanObject(this.filters)})
        }, 600)
      },
      deep: true
    },
    // Ensures the dialog stays open after filters had been used and then were reset to default
    extendedFiltersInUse: {
      handler () {
        if (this.extendedFiltersInUse) {
          this.keepOpen = true;
        }
      },
      immediate: true
    }
  },
  methods: {
    toggleExtendedSearch () {
      this.keepOpen = false
      this.$store.commit('updateProfile', { extendedSearch: !this.extendedSearchOpen })

      // clear the extended options on closing them so nobody can get confused by hidden search options
      if (this.extendedSearchOpen) {
        this.$set(this.filters, 'ordering', '')
      }
    }
  }
}
</script>

<style lang="scss">
.search {
  width: 100%;
  display: flex;
  flex-flow: row;

  @media screen and (max-width: 780px) {
    flex-flow: column;
  }

  .option {
    width: 100%;
    margin: 5px;
  }
}

label {
  margin-right: 8px;
}
</style>
