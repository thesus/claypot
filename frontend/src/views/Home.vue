<template>
  <article>
    <div class="header">
      <DebounceInput
        v-model="search"
        :placeholder="$t('home.search')"
        class="search"
      />
      <router-link
        v-if="isLoggedIn"
        :to="{name: 'recipe-add'}"
        class="link"
      >
        {{ $t('home.add') }}
      </router-link>
    </div>
    <RecipeList
      :filters="allFilters"
      :is-embedded="false"
    />
  </article>
</template>

<script>
import Vue from 'vue'
import { mapGetters } from 'vuex'

import RecipeList from '@/components/utils/RecipeList'
import DebounceInput from '@/components/utils/DebounceInput'

import { api, endpoints } from '@/api'

export default {
  name: 'Home',
  components: {
    RecipeList,
    DebounceInput
  },
  props: {
    filters: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      // Use searchtext from history
      search: this.$route.query.search || ''
    }
  },
  computed: {
    allFilters () {
      return this.search === '' ? this.filters : {'search': this.search, ...this.filters}
    },
    ...mapGetters([
      'isLoggedIn',
    ]),
  },
  watch: {
    search () {
      // Add the search text to the url if not empty, otherwise delete the parameter
      if (this.search) {
        this.$router.push({ query: {search: this.search} })
      } else {
        let query = this.$route.query
        if (query.search) {
          delete query.search
          this.$router.push(query)
        }
      }
    }
  },
  methods: {
    addRecipe () {
      this.$router.push({
        'name': 'recipe-add'
      })
    },
  }
}
</script>

<style lang="scss" scoped>

.header {
  margin-bottom: 10px;
  display: flex;

  .link {
    width: 120px;
  }

  @media screen and (max-width: 500px) {
    flex-direction: column-reverse;
    .link {
      width: initial;
    }
  }
}
</style>
