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
        :filters="{search: recipeRelationSearch, exclude: recipeId}"
      >
        <template v-slot:options>
          <div />
        </template>
        <template v-slot:default="{data}">
          <table>
            <thead>
              <th>
                <td>Name</td>
              </th>
            </thead>
            <tbody>
              <tr
                v-for="item in data"
                :key="item.id"
                class="choice"
                @click="addRecipeRelation(item)"
              >
                <td>{{ item.title }}</td>
              </tr>
            </tbody>
          </table>
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
            <template v-if="!overlayMode">-</template><template v-else>x</template>
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
            <div class="overlay">
              <button
                class="btn remove"
                tabindex="-1"
                @click="deleteRecipeRelation(recipe)"
              >
                Remove
              </button>
            </div>
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
@import '@/modules/table.scss';


.btn {
  /* mobile clickability */
  &.recipe-relation {
    min-width: 35px;
  }

  &.remove {
    position: absolute;
    right: 14px;
    bottom: 14px
  }
}

table {
  border-collapse: collapse;
  margin: 4px 0 0 0;

  tr {
    cursor: pointer;

    &:hover {
      background-color: rgba(184, 203, 214, 0.4);
    }
  }

  td {
    padding: 2px;
  }
}

/* Overlay link with div containing the remove button */
.overlay {
  position: absolute;
  top: 0px;
  bottom: 0px;
  left: 0px;
  right: 0px;
  z-index: 1003;
}
</style>
