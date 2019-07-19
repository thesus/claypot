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
        <button
          v-if="isLoggedIn"
          class="btn right recipe-relation"
          @click="openRecipeRelationDialog"
        >
          +
        </button>
        <div v-else />
      </template>
      <template v-slot:default="props">
        <RecipeThumbnailView
          :recipes="props.data"
          small
        >
          <template v-slot:toolbelt="{recipe}">
            <button
              v-if="isLoggedIn"
              tabindex="-1"
              class="btn recipe-relation"
              @click="deleteRecipeRelation(recipe)"
            >
              -
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
  },
}
</script>

<style scoped>
.btn.recipe-relation {
  /* mobile clickability */
  min-width: 30px;
}

p {
  cursor: pointer;
  transition: border-color .3s;
  border: 1px solid;
  border-color: transparent;
  box-sizing: border-box;
}
p:hover {
  border-color: #e0e0e0;
}
</style>
