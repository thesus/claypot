<template>
  <div v-if="loading">
    {{ $t('recipe_detail.loading') }}
  </div>
  <div v-else-if="error">
    {{ $t('recipe_detail.loading_error') }}
  </div>
  <article v-else-if="recipe">
    <header>
      <h1>{{ recipe.title }}</h1>
    </header>

    <div class="functions">
      <div class="left">
        <div class="stars">
          <div class="countainer">
            {{ $tc('recipes.stars', recipe.stars, {count: recipe.stars}) }}
          </div>
          <RecipeStarInput
            v-if="isLoggedIn"
            v-model="recipe.is_starred"
            :recipe-id="recipeId"
            class="button"
            @input="updateStars"
          />
        </div>

        <scale-input v-model="scaling" />

        <span
          v-if="isLoggedIn"
          class="fork button"
          @click="forkModal = true"
        >{{ $t('recipes.fork') }}
        </span>

        <Modal
          v-if="forkModal"
          :title="$t('recipe_detail.fork_title')"
          @close="forkModal = false"
        >
          <span class="fork info">{{ $t('recipe_detail.fork_confirm') }}</span>
          <button
            class="btn right"
            @click="fork"
          >
            {{ $t('recipes.fork') }}
          </button>
        </Modal>
      </div>

      <div class="right">
        <router-link
          v-if="canEdit"
          :to="{name: 'recipe-edit', params: {id: recipeId}}"
        >{{ $t('recipe_detail.edit') }}</router-link>
        <router-link
          v-if="recipe.parent_recipe"
          :to="{ name: 'recipe-detail', params: {id: recipe.parent_recipe }}"
        >{{ $t('recipes.parent') }}</router-link>
        <span>{{ $t('recipe_detail.posted_by', {user: author}) }}</span>
      </div>
    </div>

    <div
      v-if="recipe"
      class="header"
      :class="{
        'ingredients-single': (allIngredients.length == 1),
        'no-image': !(recipe.images && recipe.images.length > 0)
      }"
    >
      <div
        v-if="recipe && recipe.images && recipe.images.length > 0"
        class="images"
      >
        <ImageGallery :images="recipe.images" />
      </div>

      <RecipeIngredientTable
        v-for="(i, c) in allIngredients"
        :key="c + 1"
        :ingredients="i.is_group ? i.ingredients : i.ingredients"
        :caption="i.is_group ? i.title : ''"
        :scaling="scaling"
      />


      <div
        v-if="hasEstimatedWorkDuration || hasEstimatedWaitingDuration"
        class="information"
      >
        <div
          v-if="hasEstimatedWorkDuration"
          class="item"
        >
          {{ $t('recipe_detail.estimated_work_duration') }}:
          <duration-span :value="recipe.estimated_work_duration" />
        </div>
        <div class="item" v-if="hasEstimatedWaitingDuration">
          {{ $t('recipe_detail.estimated_waiting_duration') }}:
          <duration-span :value="recipe.estimated_waiting_duration" />
        </div>
      </div>
    </div>

    <ol
      v-if="recipe"
      class="instructions"
    >
      <li
        v-for="instruction in recipe.instructions"
        :key="instruction.order"
      >
        <p>{{ instruction.text }}</p>
      </li>
    </ol>

    <!-- Add recipe relation -->
    <Modal v-if="showAddRecipeRelationDialog" :title="$t('recipe_detail.add_recipe_relation')" @close="closeRecipeRelationDialog">
      <DebounceInput v-model="recipeRelationSearch" :placeholder="$t('home.search')" class="search"/>
      <RecipeList v-if="this.recipeRelationSearch.length" :filters="{recipe: this.recipeId, search: recipeRelationSearch}">
        <template v-slot:default="{data}">
          <p v-for="item in data" @click="addRecipeRelation(item)">{{ item.title }}</p>
        </template>
      </RecipeList>
    </Modal>

    <!-- Related recipes -->
    <RecipeList v-if="recipeId" :receiver-endpoint="recipeRelationEndpoint" :filters="recipeRelationFilter" :receiver-transform="transformRecipeRelation" :reload-trigger="reloadTrigger">
      <template v-slot:options>
        <button v-if="isLoggedIn" class="btn right" @click="openRecipeRelationDialog">+</button>
        <div v-else></div>
      </template>
      <template v-slot:default="props">
        <RecipeThumbnailView
          :recipes="props.data"
          class="recipes"
        >
          <template v-slot:toolbelt="{recipe}">
            <button v-if="isLoggedIn" tabindex="-1" class="btn recipe-relation-delete" @click="deleteRecipeRelation(recipe)">-</button>
          </template>
        </RecipeThumbnailView>
      </template>

      <template v-slot:noData>
        {{ $t('recipe_detail.no_linked_recipes') }}
      </template>
    </RecipeList>
  </article>
  <div v-else>
    {{ $t('recipe_detail.no_data') }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { api, endpoints } from '@/api'

import DebounceInput from '@/components/DebounceInput'
import DurationSpan from '@/components/DurationSpan'
import ImageGallery from '@/components/ImageGallery'
import Modal from '@/components/Modal'
import RecipeStarInput from '@/components/RecipeStarInput'
import RecipeIngredientTable from '@/components/RecipeIngredientTable'
import ScaleInput from '@/components/ScaleInput'
import Modal from '@/components/Modal'
import RecipeList from '@/components/RecipeList'
import RecipeThumbnailView from '@/components/RecipeThumbnailView'

export default {
  components: {
    DebounceInput,
    DurationSpan,
    ImageGallery,
    Modal,
    RecipeIngredientTable,
    RecipeList,
    RecipeStarInput,
    RecipeThumbnailView,
    ScaleInput,
    Modal
  },
  data () {
    return {
      forkModal: false,
      loading: false,
      error: false,
      recipe: {
      },
      scaling: 1.0,
      reloadTrigger: 0,

      showAddRecipeRelationDialog: false,
      recipeRelationSearch: "",
    }
  },
  computed: {
    recipeRelationEndpoint () {
      return endpoints.fetch_recipe_relation()
    },
    recipeRelationFilter () {
      return {recipe: this.recipeId}
    },
    recipeId () {
      return Number(this.$route.params.id)
    },
    author () {
      return this.recipe.author || this.$t('recipe_detail.unknown_user')
    },
    canEdit () {
      return (
        (
          this.recipe && this.recipe.author_id &&
          (this.userId == this.recipe.author_id)
        ) ||
        this.isSuperUser
      )
    },
    allIngredients () {
      return this.recipe.ingredients || []
    },
    hasEstimatedWorkDuration () {
      return typeof this.recipe.estimated_work_duration !== 'undefined' && this.recipe.estimated_work_duration !== null
    },
    hasEstimatedWaitingDuration () {
      return typeof this.recipe.estimated_waiting_duration !== 'undefined' && this.recipe.estimated_waiting_duration !== null
    },
    ...mapGetters([
      'isSuperUser',
      'userId',
      'isLoggedIn',
    ]),
  },
  watch: {
    recipeId: {
      handler () {
        this.update()
      },
      immediate: true,
    },
  },
  methods: {
    openRecipeRelationDialog () {
      this.showAddRecipeRelationDialog = true
    },
    closeRecipeRelationDialog () {
      this.showAddRecipeRelationDialog = false
    },
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
    async deleteRecipeRelation (recipe) {
      const r = await api(endpoints.fetch_recipe_relation(recipe.recipeRelationId), undefined, {method: 'DELETE'})
      if (r.ok) {
        this.reloadTrigger = this.reloadTrigger + 1
      } else {
        // TODO: error handling
      }
    },
    transformRecipeRelation (recipeRelations) {
      if (recipeRelations) {
        return recipeRelations.map(recipeRelation => Object.assign({recipeRelationId: recipeRelation.id}, recipeRelation.recipe1.id === this.recipeId ? recipeRelation.recipe2 : recipeRelation.recipe1))
      } else {
        return recipeRelations
      }
    },
    updateStars (result) {
      this.recipe.stars += (result) ? 1 : -1
    },
    async fork () {
      try {
        const r = await api(
          endpoints.fork(this.recipeId),
          {},
          { method: 'POST' }
        )
        if (r.ok) {
          this.$router.push(
            {
              name: 'recipe-detail',
              params: {
                id: await r.json()
              }
            }
          )
        } else {
          throw new Error("Fork not working!")
        }
      } catch (err) {
        console.log(err)
        // TODO: Show error
      }
    },
    async update () {
      if (!this.recipeId) {
        return
      }
      try {
        this.loading = true
        const r = await api(endpoints.fetch_recipe(this.recipeId))
        this.loading = false
        if (r.ok) {
          this.recipe = await r.json()
        } else {
          throw new Error("Display some kind of error")
        }
      } catch (err) {
        // TODO: Display some kind of error
        this.error = true
      }
    }
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/variables.scss';

.functions {
  line-height: 24px;

  @media screen and (max-width: 500px) {
    line-height: 40px;
    flex-direction: column;
  }

  display: flex;
  justify-content: space-between;

  .stars {
    border: solid 1px #ccc;
    display: inline-block;
    white-space: nowrap;
    margin-right: 5px;

    .countainer, .button {
      padding: 0 5px 0 5px;
      display: inline-block;
      border: none;
    }

    .button {
      border-left: solid 1px #ccc;
    }

  }

  .scale {
    margin-right: 5px;
  }

  .right {
    @media screen and (max-width: 500px) {
      line-height: 32px;
    }
    span {
      margin-left: 10px;
    }
    a {
      margin: 0 2px 0 2px;
    }
  }
}

.button {
  border: solid 1px #ccc;
  padding: 0 5px 0 5px;
  cursor: pointer;
  display: inline-block;

  &:hover {
    background-color: $font_color;
    color: white;
  }
}

.fork {
  &.info {
    display: block;
  }
}

.header {
  display: flex;
  flex-wrap: wrap;
  margin: 0px -10px 5px -10px;
  justify-content: space-between;
  border: none;

  .ingredients-group {
    padding: 0 5px 0 5px;
    margin: 5px;
    width: 220px;
    order: 3;
  }

  .images {
    border: solid 1px #ccc;
    padding: 0;
    margin: 5px 5px 0px 5px;
    height: 250px;
    width: 100%;
    img {
      width: 100%;
      object-fit: contain;
    }

  }

  .information {
    display: flex;
    margin: 5px 5px 0px 5px;
    width: 100%;
    justify-content: space-around;
    background-color: rgba(184, 203, 214, 0.4);
    padding: 6px;
    order: 2;
    border: solid 1px #B8CBD6;
  }

  @media screen and (min-width: 780px) {
    .images {
      height: 500px;
    }
  }

  @media screen and (min-width: 780px) {
    &.ingredients-single {
      flex-direction: row-reverse;

      .ingredients-group {
        order: 1;
      }

      &.no-image {
        flex-direction: row;

        .ingredients-group {
          order: 3;
        }
      }

      .images {
        flex: 1;
        width: auto;
        flex-basis: min-content;
      }
    }
  }
}


.instructions {
  margin: 5px;
  text-align: justify;
  padding-left: 20px;
}

article {
  margin: auto;
  max-width: 1000px;
}

.recipe-relation-delete {
  /* mobile clickability */
  min-width: 30px;
}
</style>
