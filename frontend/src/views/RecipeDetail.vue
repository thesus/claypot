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

        <ScaleInput
          v-model="scaling"
          :recipe="recipe"
        />

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
        >
          {{ $t('recipe_detail.edit') }}
        </router-link>
        <router-link
          v-if="recipe.parent_recipe"
          :to="{ name: 'recipe-detail', params: {id: recipe.parent_recipe }}"
        >
          {{ $t('recipes.parent') }}
        </router-link>
        <span>{{ $t('recipe_detail.posted_by', {user: author}) }}</span>
      </div>
    </div>

    <p
      v-if="recipe && recipe.description && recipe.description.length > 0"
      class="description"
    >
      {{ recipe.description }}
    </p>

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
        :ingredients="i.ingredients"
        :caption="allIngredients.length > 1 ? i.title : ''"
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
          <DurationSpan :value="recipe.estimated_work_duration" />
        </div>
        <div
          v-if="hasEstimatedWaitingDuration"
          class="item"
        >
          {{ $t('recipe_detail.estimated_waiting_duration') }}:
          <DurationSpan :value="recipe.estimated_waiting_duration" />
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

    <RecipeRelationGallery :recipe-id="recipeId" />
  </article>
  <div v-else>
    {{ $t('recipe_detail.no_data') }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { api, endpoints } from '@/api'

import DurationSpan from '@/components/recipe-detail/DurationSpan'
import ImageGallery from '@/components/recipe-detail/ImageGallery'
import Modal from '@/components/utils/Modal'
import RecipeIngredientTable from '@/components/recipe-detail/RecipeIngredientTable'
import RecipeRelationGallery from '@/components/recipe-detail/RecipeRelationGallery'
import RecipeStarInput from '@/components/recipe-detail/RecipeStarInput'
import ScaleInput from '@/components/recipe-detail/ScaleInput'

export default {
  components: {
    DurationSpan,
    ImageGallery,
    Modal,
    RecipeIngredientTable,
    RecipeRelationGallery,
    RecipeStarInput,
    ScaleInput,
  },
  data () {
    return {
      forkModal: false,
      loading: false,
      error: false,
      recipe: {
      },
      scaling: 1.0,
    }
  },
  computed: {
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
    margin: 2px 5px 2px 2px;

    .countainer, .button {
      padding: 0 5px 0 5px;
      display: inline-block;
      border: none;
    }

    .button {
      border-left: solid 1px #ccc;
      margin: 0;
    }

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
  margin: 2px 5px 2px 2px;

  &.info {
    display: block;
  }
}

.description {
  margin: 4px 0 0 0;
  text-align: justify;
  color: #6a7783;
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
</style>
