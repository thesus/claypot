<template>
  <div>
    <div class="options">
      <button
        class="btn right"
        @click="updateMode"
      >
        {{ $t('home.mode') }}
      </button>
    </div>
    <Receiver
      :endpoint="endpoint"
      :filters="filters"
    >
      <template v-slot:default="props">
        <RecipeThumbnailView
          v-if="getHomeView"
          :recipes="props.data"
          class="recipes"
        />
        <RecipeTableView
          v-else
          :recipes="props.data"
          class="recipes"
        />
      </template>
    </Receiver>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import { endpoints } from '@/api'

import RecipeThumbnailView from '@/components/RecipeThumbnailView'
import RecipeTableView from '@/components/RecipeTableView'

import Receiver from '@/components/Receiver'

export default {
  name: 'RecipeList',
  components: {
    RecipeThumbnailView,
    RecipeTableView,
    Receiver
  },
  props: {
    filters: {
      type: Object,
      default: () => ({}),
    },
  },
  data () {
    return {
      endpoint: endpoints.fetch_recipes(),
      mode: true,
    }
  },
  computed: {
    ...mapGetters(['getHomeView'])
  },
  methods: {
    updateMode() {
      this.$store.commit('updateProfile', { homeView: !this.getHomeView})
    },
    addRecipe () {
      this.$router.push({
        'name': 'recipe-add'
      })
    },
    showAllRecipes () {
      this.$set(this, 'filters', {})
    },
    showMyFavorites () {
      this.$set(this, 'filters', {is_starred: 2})
    },
    showMyRecipes () {
      this.$set(this, 'filters', {is_my_recipe: 2})
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.recipes {
  padding: 5px;
}

.options {
  display: flex;
  flex-direction: row-reverse;
}
</style>
