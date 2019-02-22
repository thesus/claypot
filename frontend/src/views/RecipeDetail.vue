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
      <div class="stars">
        <div class="countainer">
          {{ $tc('recipes.stars', recipe.stars, {count: recipe.stars}) }}
        </div>
        <RecipeStarInput
          v-if="isLoggedIn"
          v-model="recipe.is_starred"
          :recipe-id="recipeId"
          class="button"
        />
      </div>
      <router-link
        v-if="canEdit"
        :to="{name: 'recipe-edit', param: {id: recipeId}}"
      >
        {{ $t('recipe_detail.edit') }}
      </router-link>
    </div>

    <div
      v-if="recipe"
      class="header"
    >
      <RecipeIngredientTable
        v-for="(i, c) in allIngredients"
        :key="c + 1"
        :ingredients="i.is_group ? i.ingredients : i.ingredients"
        :caption="i.is_group ? i.title : ''"
      />
      <div class="images">
        image
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

    <footer>
      <p>{{ $t('recipe_detail.posted_by', {user: author}) }}</p>
    </footer>
  </article>
  <div v-else>
    {{ $t('recipe_detail.no_data') }}
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import {api, endpoints} from '@/api'

import RecipeStarInput from '@/components/RecipeStarInput'
import RecipeIngredientTable from '@/components/RecipeIngredientTable'

export default {
  components: {
    RecipeIngredientTable,
    RecipeStarInput,
  },
  data () {
    return {
      loading: false,
      error: false,
      recipe: {
      }
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
      return this.recipe.ingredients
    },
    ...mapGetters([
      'isSuperUser',
      'userId',
      'isLoggedIn',
    ]),
  },
  watch: {
    recipeId() {
      this.update()
    }
  },
  mounted () {
    this.update()
  },
  methods: {
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
.stars {
  border: solid 1px #ccc;
  display: inline;
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

.functions {
  display: flex;
  justify-content: space-between;
}

.header {
  display: flex;
  flex-wrap: wrap;
  margin: 15px -10px;

  @media screen and (max-width: 850px) {
    flex-wrap: wrap-reverse;
    .images, .ingredients {
      flex-basis: 100% !important;
    }
  }

  .ingredients {
    padding: 0 5px 0 5px;
    width: 25%;

    .amount {
      text-align: right;
    }

    .ingredient {
      text-align: left;
      padding-left: 10px;
    }
  }
  .images {
    margin: 0 10px;
    border: solid 1px #ccc;
    flex: 1;
    height: 400px;
  }
}

.instructions {
  text-align: justify;
}
</style>
