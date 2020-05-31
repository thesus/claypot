<template>
  <form
    class="search"
    @submit.prevent
  >
    <div class="main">
      <input
        v-model="filters.search"
        :placeholder="$t('search.textsearch')"
      >
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
    </div>
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
          <option value="">
            {{ $t('search.ordering.relevance') }}
          </option>
          <option value="time">
            {{ $t('search.ordering.time') }}
          </option>
          <option value="popularity">
            {{ $t('search.ordering.popularity') }}
          </option>
        </select>
      </div>
    </div>
  </form>
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
      this.$set(this.filters, 'ordering', '')
    }
  }
}
</script>

<style lang="scss">
.search {
  width: 100%;
  display: flex;
  flex-flow: column;

  .main {
    width: 100%;
    display: flex;
    flex-flow: column;

    .btn {
      /* Please keep going. This is due to funky firefox behavior */
      min-width: unset !important;
      white-space: nowrap;
    }

    @media screen and (min-width: 500px) {
      flex-flow: row;
    }
  }

  .extended {
    display: flex;
    flex-flow: row;
    padding: 5px;
    margin-top: 5px;
    background-color: rgba(184, 203, 214, 0.4);

    .option {
      width: 100%;
      margin: 5px;
    }
  }
}

label {
  margin-right: 8px;
}
</style>
