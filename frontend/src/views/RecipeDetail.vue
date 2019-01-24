<template>
  <div v-if="loading">{{ $t('recipe_detail.loading') }}</div>
  <div v-else-if="error">{{ $t('recipe_detail.loading_error') }}</div>
  <article v-else-if="recipe">
    <header>
      <h1>{{ recipe.title }}</h1>
    </header>

    <div class="functions">
      <div class="stars">
        <div class="countainer">{{ $tc('recipes.stars', recipe.stars, {count: recipe.stars}) }}</div>
        <recipe-star-input class="button" v-if="isLoggedIn" :recipeId="recipeId" v-model="recipe.is_starred" />
      </div>
      <router-link v-if="canEdit" :to="{name: 'recipe-edit', param: {id: recipeId}}">{{ $t('recipe_detail.edit') }}</router-link>
    </div>

    <div class="header">
      <table class="ingredients">
        <thead>
          <tr>
            <th class="amount">{{ $t('recipe_detail.amount') }}</th>
            <th class="ingredient">{{ $t('recipe_detail.ingredient') }}</th>
          </tr>
        </thead>
        <tbody v-if="recipe && recipe.recipe_ingredients">
          <tr v-for="ingredient in recipe.recipe_ingredients" :key="ingredient.ingredient">
            <td class="amount">{{ ingredient.amount_numeric }}&nbsp;{{ ingredient.unit }}</td>
            <td class="ingredient">{{ ingredient.ingredient }}<span v-if="ingredient.ingredient_extra">, {{ ingredient.ingredient_extra }}</span></td>
          </tr>
        </tbody>
      </table>
      <div class="images">
        image
      </div>
    </div>

    <p class="instructions" v-if="recipe">{{ recipe.instructions }}</p>

    <footer>
      <p>{{ $t('recipe_detail.posted_by',  {user: author}) }}</p>
    </footer>
  </article>
  <div v-else>{{ $t('recipe_detail.no_data') }}</div>
</template>

<script>
import {mapGetters} from 'vuex'
import {api, endpoints} from '@/api'

import RecipeStarInput from '@/components/RecipeStarInput'

export default {
  components: {
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
  }
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
