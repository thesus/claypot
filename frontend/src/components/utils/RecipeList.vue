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
      :reload-trigger="reloadTrigger"
      :filters="filters"
      :has-url-pages="!isEmbedded"
      @page="scrollTop"
    >
      <template v-slot:default="props">
        <slot
          :get-home-view="getHomeView"
          v-bind="props"
        >
          <RecipeThumbnailView
            v-if="getHomeView"
            :recipes="props.data"
            class="p-5"
          />
          <RecipeTableView
            v-else
            :recipes="props.data"
            class="p-5"
          />
        </slot>
      </template>
      <template v-slot:noData>
        <slot name="noData" />
      </template>
    </Receiver>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import { endpoints } from '@/api'

import RecipeThumbnailView from '@/components/utils/RecipeThumbnailView'
import RecipeTableView from '@/components/utils/RecipeTableView'

import Receiver from '@/components/utils/Receiver'

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
    },
    // If this is false we show the page in the url and scroll to the top after changing the page
    isEmbedded: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      mode: true,
    }
  },
  computed: {
    ...mapGetters(['getHomeView']),
  },
  methods: {
    updateMode() {
      this.$store.commit('updateProfile', { homeView: !this.getHomeView})
    },
    showAllRecipes () {
      this.$set(this, 'filters', {})
    },
    showMyFavorites () {
      this.$set(this, 'filters', {is_starred: 2})
    },
    showMyRecipes () {
      this.$set(this, 'filters', {is_my_recipe: 2})
    },
    scrollTop() {
      if (!this.isEmbedded) {
        window.scrollTo(0, 0)
      }
    }
  },
}
</script>

<style lang="scss" scoped>

.p-5 {
  padding: 5px;
}

.options {
  display: flex;
  flex-direction: row-reverse;
}
</style>
