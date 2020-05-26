<template>
  <article>
    <div class="header">
      <SearchForm @input="updateFilters" />

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
import SearchForm from '@/components/utils/SearchForm'

import { api, endpoints } from '@/api'

export default {
  name: 'Home',
  components: {
    RecipeList,
    SearchForm
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
      filterOptions:this.$route.query
    }
  },
  computed: {
    allFilters () {
      return {...this.filters, ...this.filterOptions}
    },
    ...mapGetters([
      'isLoggedIn',
    ]),
  },
  methods: {
    addRecipe () {
      this.$router.push({
        'name': 'recipe-add'
      })
    },
    updateFilters(value) {
      this.$set(this, 'filterOptions', value)
    }
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
