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
import { mapActions, mapGetters } from 'vuex'

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
    },
    titleName: {
      type: String,
      default: "titles.home",
    },
  },
  data () {
    return {
      // Use searchtext from history
      filterOptions: this.$route.query
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
  watch: {
    titleName: {
      handler () {
        this.updateTitle({name: this.titleName})
      },
    },
  },
  mounted () {
    this.updateTitle({name: this.titleName})
  },
  methods: {
    addRecipe () {
      this.$router.push({
        'name': 'recipe-add'
      })
    },
    updateFilters(value) {
      this.$set(this, 'filterOptions', value)
    },
    ...mapActions(["updateTitle"])
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
