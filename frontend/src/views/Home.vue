<template>
  <article>
    <div class="header">
      <DebounceInput v-model="search" :placeholder="$t('home.search')" class="search"/>
      <router-link
        v-if="isLoggedIn"
        :to="{name: 'recipe-add'}"
        class="link"
      >
        {{ $t('home.add') }}
      </router-link>
    </div>
    <RecipeList :filters="getFilters" />
  </article>
</template>

<script>
import Vue from 'vue'
import { mapGetters } from 'vuex'

import RecipeList from '@/components/RecipeList'
import DebounceInput from '@/components/DebounceInput'

import { api, endpoints } from '@/api'

export default {
  name: 'Home',
  components: {
    RecipeList,
    DebounceInput
  },
  data () {
    return {
      search: ''
    }
  },
  computed: {
    getFilters () {
      return this.search === '' ? {} : {'search': this.search}
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
  },
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
