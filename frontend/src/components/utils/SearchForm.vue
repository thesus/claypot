<template>
  <div class="search">
    <div class="option">
      <input
        v-model="filters.search"
        :placeholder="$t('search.textsearch')"
      >
    </div>
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
</template>


<script>
import { cleanObject } from '@/utils'


export default {
  data () {
    return {
      filters: {
        ordering: this.$route.query.ordering || '',
        search: this.$route.query.search || ''
      },
      debounce: null
    }
  },
  watch: {
    filters: {
      handler () {
        clearTimeout(this.debounce)
        this.debounce = setTimeout(() => {
          this.$emit('input', { ...this.filters })

          this.$router.push({query: cleanObject(this.filters)})
        }, 600)
      },
      deep: true
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
