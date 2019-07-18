<template>
  <div>
    <div class="options">
      <slot name="options">
        <button
          class="btn right"
          @click="updateMode"
        >
          {{ $t('home.mode') }}
        </button>
      </slot>
    </div>
    <Receiver
      :endpoint="receiverEndpoint"
      :transform="receiverTransform"
      :filters="filters"
      :reload-trigger="reloadTrigger"
    >
      <template v-slot:default="props">
        <slot :get-home-view="getHomeView" v-bind="props">
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
        </slot>
      </template>
      <template v-slot:noData><slot name="noData"/></template>
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
    receiverEndpoint: {
      type: Object,
      default: () => endpoints.fetch_recipes(),
    },
    receiverTransform: {
      type: Function,
      default: null,
    },
    reloadTrigger: {
      type: Number,
      default: 0,
    }
  },
  data () {
    return {
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
  },
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
