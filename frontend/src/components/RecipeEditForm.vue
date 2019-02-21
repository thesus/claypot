<template>
  <article>
    <header>
      <div>
        <input
          v-model="recipe_dirty.title"
          :placeholder="$t('recipes.title')"
          :disabled="saving"
          :class="{'form-error': !!errors.title.length}"
        >
      </div>
      <FormFieldValidationError :errors="errors.title" />
    </header>

    <div class="ingredients">
      <div class="table">
        <RecipeEditIngredientTable
          v-for="(ingredientBatch,i) in recipe_dirty.ingredients"
          :key="i"
          v-model="recipe_dirty.ingredients[i]"
          :recipe-ingredient-error="recipeIngredientError(i)"
          :saving="saving"
          @remove="recipe_dirty.ingredients.splice(i, 1)"
        />
      </div>
      <button
        :disabled="saving"
        class="btn btn-right submit add-group"
        @click.prevent="addIngredientGroup"
      >
        {{ $t('recipe_edit.add_group') }}
      </button>
    </div>

    <ol>
      <li
        v-for="(instruction, i) in recipe_dirty.instructions"
        ref="instructions"
        :key="i"
      >
        <div class="instruction">
          <textarea
            v-model="instruction.text"
            :placeholder="$t('recipes.instructions')"
            :disabled="saving"
            class="small"
          />
          <FormFieldValidationError
            :errors="recipeInstructionError(i).text"
            :saving="saving"
          />
          <button
            :disabled="saving"
            tabindex="-1"
            class="btn btn-right remove"
            @click="recipe_dirty.instructions.splice(i, 1)"
          >
            {{ $t('recipe_edit.remove') }}
          </button>
        </div>
      </li>
    </ol>
    <div>
      <button
        :disabled="saving"
        class="btn btn-right submit"
        @click.prevent="addInstruction"
      >
        {{ $t('recipe_edit.add_instruction') }}
      </button>
    </div>

    <div>
      <button
        :disabled="saving"
        class="btn btn-right btn-primary"
        @click.prevent="save"
      >
        {{ $t('recipe_edit.save') }}
      </button>
    </div>
    <div v-if="newIngredientsDecision">
      <p>{{ $tc('recipes.confirm_new_ingredients.message', newIngredientsCount, {count: newIngredientsCount}) }}</p>
      <button
        class="btn new-ingredient"
        @click="newIngredientsDecision(true)"
      >
        {{ $tc('recipes.confirm_new_ingredients.accept', newIngredientsCount, {count: newIngredientsCount}) }}
      </button>
      <button
        class="btn"
        @click="newIngredientsDecision(false)"
      >
        {{ $tc('recipes.confirm_new_ingredients.decline', newIngredientsCount, {count: newIngredientsCount}) }}
      </button>
    </div>
    <div v-if="errors.client_side">
      {{ errors.client_side }}
    </div>
    <div v-if="errors.detail">
      {{ errors.detail }}
    </div>

    <footer>
      <p v-if="recipe.id">
        {{ $t('recipe_edit.posted_by', {user: author}) }}
      </p>
    </footer>
  </article>
</template>

<script>
import {api, endpoints} from '@/api'
import {sortedUnifiedIngredients} from '@/utils'
import FormFieldValidationError from '@/components/FormFieldValidationError'
import RecipeEditIngredientTable from '@/components/RecipeEditIngredientTable'

const amount_types = {
  none: 1,
  numeric: 2,
  approx: 3,
}

export default {
  name: 'RecipeEditForm',
  components: {
    FormFieldValidationError,
    RecipeEditIngredientTable,
  },
  props: {
    recipe: {
      type: Object,
      default: function () {
        return {}
      },
    },
  },
  data () {
    return {
      recipe_dirty: {
        ingredients: [{isGroup: false, title: '', ingredients: []}],
        instructions: [this.createEmptyInstruction()],
      },
      saving: false,
      errors: {
        title: [],
        ingredients: [],
        ingredient_groups: [],
        instructions: [],
        client_side: '',
        detail: '',
      },
      newIngredientsDecision: null,
      newIngredientsCount: 0,
    }
  },
  computed: {
    author () {
      return this.recipe.author || this.$t('recipe_edit.unknown_user')
    },
    recipeIngredientError () {
      return i => {
        const subsetOfErrors = (this.sortedUnifiedErrors.ingredients[i] || {}).ingredients
        return j => {
          const e = subsetOfErrors || []
          const r = e.length > j ? e[j] : {}
          for (let p of ['ingredient', 'ingredient_extra', 'amount_numeric', 'unit']) {
            r[p] = r[p] || []
          }
          return r
        }
      }
    },
    unifiedErrors () {
      const addKeys = function (src, setter) {
        if (typeof src === 'string' || typeof src === 'number' || src === null || typeof src === 'undefined' || typeof src === 'boolean') {
          setter([])
        } else if (Array.isArray(src)) {
          const c = []
          c.length = src.length
          src.forEach((item, i) => {
            addKeys(item, function (v) {c[i]=v})
          })
          setter(c)
        } else if (typeof src === 'object') {
          const c = {}
          for (let k of Object.keys(src)) {
            addKeys(src[k], function (v) {c[k]=v})
          }
          setter(c)
        } else {
          throw new Error('you missed a spot:' + src)
        }
      }
      let r
      addKeys(this.recipe, function (v) {r=v})
      // mixin errors
      const addErrors = function (src, unifiedErrorPart, setter) {
        if (typeof src === 'string' || typeof src === 'number' || src === null || typeof src === 'undefined' || typeof src === 'boolean') {
          setter(src)
        } else if (Array.isArray(src)) {
          src.forEach((item, i) => {
            addErrors(item, unifiedErrorPart[i], function (v) {unifiedErrorPart[i]=v})
          })
        } else if (typeof src === 'object') {
          for (let k of Object.keys(src)) {
            addErrors(src[k], unifiedErrorPart[k], function (v) {unifiedErrorPart[k]=v})
          }
        } else {
          throw new Error('you missed a spot: ' + src)
        }
      }
      addErrors(this.errors, r, function (v) {r=v})
      return r
    },
    sortedUnifiedErrors () {
      const unifiedErrors = this.unifiedErrors
      const {title, instructions} = unifiedErrors
      const ingredients = sortedUnifiedIngredients(unifiedErrors)
      return {
        title,
        instructions,
        ingredients,
      }
    },
    recipeInstructionError () {
      return i => {
        const e = this.sortedUnifiedErrors
        const r = e.length > i ? e[i] : {}
        for (let p of ['text']) {
          r[p] = r[p] || []
        }
        return r
      }
    },
  },
  watch: {
    recipe () {
      const r = this.recipe
      this.recipe_dirty = {
        title: r.title,
        instructions: r.instructions,
        ingredients: sortedUnifiedIngredients(r),
      }
    }
  },
  methods: {
    addIngredientGroup () {
      this.recipe_dirty.ingredients.push(this.createEmptyIngredientGroup())
    },
    createEmptyIngredientGroup () {
      return {isGroup: true, title: '', ingredients: []}
    },
    createEmptyInstruction () {
      return {text: ''}
    },
    addInstruction () {
      this.recipe_dirty.instructions.push(this.createEmptyInstruction())
    },
    async save () {
      this.saving = true
      try {
        // Step 1: Check for new ingredients
        {
          const r = await api(endpoints.check_new_ingredients(), {
            ingredients: [].concat(...this.recipe_dirty.ingredients.map(group => group.ingredients.map(i => i.ingredient))),
          })
          if (r.ok) {
            const newIngredients = (await r.json()).ingredients
            if (newIngredients.length > 0) {
              this.newIngredientsCount = newIngredients.length
              try {
              const userDecision = await new Promise((resolve) => {
                // this will give the user a choice to cancel or continue the process.
                this.newIngredientsDecision = resolve
              })
              if (userDecision) {
                const newIngredientData = newIngredients.map(i => {
                  return {
                    name: i,
                  }
                })
                const r2 = await api(endpoints.create_many_ingredients(), newIngredientData)
                if (r2.ok) {

                } else {
                  // TODO: Proper error propagation
                  throw new Error('it broke. pls fix.')
                }
              } else {
                // cancel process
                return
              }
              } finally {
                this.newIngredientsDecision = null
              }
            }
          } else {
            // TODO: Proper error propagation
            const errors = await r.json()
            throw new Error(errors.error.join('; '))
          }
        }

        const ri = []
        let order = 1
        const rig = []
        for (let groupLike of this.recipe_dirty.ingredients) {
          const target = groupLike.isGroup ? [] : ri
          let innerOrder = 1
          for (let i of groupLike.ingredients) {
            target.push({
              order: groupLike.isGroup ? innerOrder : order,
              ingredient: i.ingredient,
              ingredient_extra: i.ingredient_extra,
              optional: false,
              amount_type: amount_types.numeric,
              amount_numeric: Number(i.amount_numeric),
              amount_approx: '',
              unit: i.unit,
            })
            if (!groupLike.isGroup) {
              order++
            } else {
              innerOrder++
            }
          }
          if (groupLike.isGroup) {
            rig.push({
              order: order,
              title: groupLike.title,
              ingredients: target,
            })
            order++
          }
        }
        const d = {
          title: this.recipe_dirty.title,
          instructions: this.recipe_dirty.instructions.map((instruction, i) => { return {order: i, text: instruction.text}}),
          ingredients: ri,
          ingredient_groups: rig,
        }
        const r = await api(endpoints.post_recipe(this.recipe.id), d, {method: this.recipe.id ? 'put' : 'post'})
        if (r.ok) {
          this.errors.client_side = ''
          this.recipe_dirty = await r.json()
          // TODO: Notify user about success.
          this.$emit('input', this.recipe_dirty)
        } else {
          // TODO: Notify user about broken fields?
          const errors = await r.json()
          this.errors.title = errors.title || []
          this.errors.ingredients = errors.ingredients || []
          this.errors.ingredient_groups = errors.ingredient_groups || []
          this.errors.instructions = errors.instructions || []
          this.errors.detail = errors.detail || ''
        }
      } catch (err) {
        this.errors.client_side = err.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>

<style lang="scss">
@import '@/modules/inputs.scss';
@import '@/modules/variables.scss';

.btn {
  margin: 0;
}

.new-ingredient {
  border-right: none;
}

.ingredients {
  margin-bottom: 5px;
  border: solid 1px #ccc;
  display: inline-block;
  box-sizing: border-box;
  width: 100%;
  padding: 4px;

  .submit {
    margin: 2px 2px 3px 0;
  }

  .add-group {
    margin-right: 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;

    .remove {
      float: right;
    }

    tr {
      position: relative;
    }

    td {
      vertical-align:top;
      padding: 2px 2px 0 2px;
      margin: 0;

      height: 100%;
    }

    .input, td > button {
      padding: 0;
      margin: 0;
      min-height: 25px;
    }
  }
}

.instruction {
  display: inline-block;
  width: 100%;
  text-align: center;
  textarea {
    margin: 0;
    float: left;
    width: calc(100% - 65px);
  }
}
</style>
