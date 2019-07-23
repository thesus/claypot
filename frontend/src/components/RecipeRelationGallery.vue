<template>
  <div>
    <!-- Add recipe relation -->
    <Modal
      v-if="showAddRecipeRelationDialog"
      :title="$t('recipe_detail.add_recipe_relation')"
      @close="closeRecipeRelationDialog"
    >
      <DebounceInput
        v-model="recipeRelationSearch"
        class="search"
        :placeholder="$t('home.search')"
      />
      <RecipeList
        v-if="recipeRelationSearch.length"
        :filters="{recipe: recipeId, search: recipeRelationSearch}"
      >
        <template v-slot:options>
          <div />
        </template>
        <template v-slot:default="{data}">
          <p
            v-for="item in data"
            :key="item.id"
            @click="addRecipeRelation(item)"
          >
            {{ item.title }}
          </p>
        </template>
      </RecipeList>
    </Modal>

    <!-- Related recipes -->
    <RecipeList
      v-if="recipeId"
      :receiver-endpoint="recipeRelationEndpoint"
      :filters="recipeRelationFilter"
      :receiver-transform="transformRecipeRelation"
      :reload-trigger="reloadTrigger"
    >
      <template v-slot:options>
        <template v-if="isLoggedIn">
          <button
            class="btn right recipe-relation"
            @click="openRecipeRelationDialog"
          >
            +
          </button>
          <button
            class="btn right recipe-relation"
            @click="toggleRecipeRelationRemoveMode"
          >
            <span v-if="!overlayMode">-</span><span v-else>x</span>
          </button>
        </template>
        <div v-else />
      </template>
      <template v-slot:default="props">
        <RecipeThumbnailView
          :recipes="props.data"
          small
        >
          <template
            v-if="overlayMode"
            v-slot:overlay="{recipe}"
          >
            <button
              class="btn remove"
              tabindex="-1"
              @click="deleteRecipeRelation(recipe)"
            >
              Remove
            </button>
          </template>
        </RecipeThumbnailView>
      </template>

      <template v-slot:noData>
        {{ $t('recipe_detail.no_linked_recipes') }}
      </template>
    </RecipeList>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { api, endpoints } from '@/api'

import DebounceInput from '@/components/DebounceInput'
import Modal from '@/components/Modal'
import RecipeList from '@/components/RecipeList'
import RecipeThumbnailView from '@/components/RecipeThumbnailView'

export default {
  name: "RecipeRelationGallery",
  components: {
    DebounceInput,
    Modal,
    RecipeList,
    RecipeThumbnailView,
  },
  props: {
    recipeId: {
      type: Number,
      required: true,
    },
  },
  data () {
    return {
      showAddRecipeRelationDialog: false,
      recipeRelationSearch: "",
      reloadTrigger: 0,
      overlayMode: false,
    }
  },
  computed: {
    recipeRelationEndpoint () {
      return endpoints.fetch_recipe_relation()
    },
    recipeRelationFilter () {
      return {recipe: this.recipeId}
    },
    ...mapGetters([
      'isLoggedIn',
    ]),
  },
  methods: {
    async addRecipeRelation (relatedRecipe) {
      const type = 1  // addition
      const r = await api(endpoints.fetch_recipe_relation(), {recipe1: this.recipeId, recipe2: relatedRecipe.id, type: type}, {method: 'POST'})
      if (r.ok) {
        this.closeRecipeRelationDialog()
        this.reloadTrigger = this.reloadTrigger + 1
      } else {
        // TODO: error handling
      }
    },
    closeRecipeRelationDialog () {
      this.showAddRecipeRelationDialog = false
    },
    async deleteRecipeRelation (recipe) {
      const r = await api(endpoints.fetch_recipe_relation(recipe.recipeRelationId), undefined, {method: 'DELETE'})
      if (r.ok) {
        this.reloadTrigger = this.reloadTrigger + 1
        this.overlayMode = false
      } else {
        // TODO: error handling
      }
    },
    openRecipeRelationDialog () {
      this.showAddRecipeRelationDialog = true
    },
    transformRecipeRelation (recipeRelations) {
      if (recipeRelations) {
        return recipeRelations.map(recipeRelation => Object.assign({recipeRelationId: recipeRelation.id}, recipeRelation.recipe1.id === this.recipeId ? recipeRelation.recipe2 : recipeRelation.recipe1))
      } else {
        return recipeRelations
      }
    },
    toggleRecipeRelationRemoveMode () {
      this.overlayMode = !this.overlayMode
    }
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.btn {
  &.recipe-relation {
    /* mobile clickability */
    min-width: 30px;
  }

  &.remove {
    position: absolute;
    right: 14px;
    bottom: 14px
  }
}

p {
  cursor: pointer;
  transition: border-color .3s;
  border: 1px solid;
  border-color: transparent;
  box-sizing: border-box;

  &:hover {
    border-color: #e0e0e0;
  }
}

</style>
