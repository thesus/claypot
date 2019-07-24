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

      <textarea
        v-model="recipe_dirty.description"
        :placeholder="$t('recipes.description')"
        :disabled="saving"
        class="description"
        :class="{'form-error': !!errors.description.length}"
      />
    </header>

    <FormFieldValidationError :errors="errors.description" />
    <div class="images">
      <ImageUpload
        v-model="recipe_dirty.images"
        :initial="images"
      />
    </div>

    <div class="ingredients">
      <RecipeEditIngredientTable
        v-for="(ingredientBatch,i) in recipe_dirty.ingredients"
        :key="i"
        v-model="recipe_dirty.ingredients[i]"
        :recipe-ingredient-error="recipeIngredientError(i)"
        :saving="saving"
        @remove="recipe_dirty.ingredients.splice(i, 1)"
      />
      <button
        :disabled="saving"
        class="btn right"
        @click.prevent="addIngredientGroup"
      >
        {{ $t('recipe_edit.add_group') }}
      </button>
    </div>

    <div
      v-for="(instruction, i) in recipe_dirty.instructions"
      ref="instructions"
      :key="i"
      class="instruction"
    >
      <div class="text">
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
      </div>
      <button
        :disabled="saving"
        tabindex="-1"
        class="btn remove"
        @click="recipe_dirty.instructions.splice(i, 1)"
      >
        {{ $t('recipe_edit.remove') }}
      </button>
    </div>
    <div
      class="addInstruction"
    >
      <button
        :disabled="saving"
        class="btn right"
        @click.prevent="addInstruction"
      >
        {{ $t('recipe_edit.add_instruction') }}
      </button>
    </div>

    <div class="estimation">
      <div class="column">
        <label>
          {{ $t('recipe_edit.estimated_work_duration') }}
        </label>
        <duration-input
          v-model="recipe_dirty.estimated_work_duration"
          :disabled="saving"
        />
      </div>

      <div class="column">
        <label>
          {{ $t('recipe_edit.estimated_waiting_duration') }}
        </label>
        <duration-input
          v-model="recipe_dirty.estimated_waiting_duration"
          :disabled="saving"
        />
      </div>
    </div>

    <div class="options">
      <button
        v-if="canDeleteRecipe"
        :disabled="saving"
        class="btn"
        style="float: left;"
        @click.prevent="deleteModal = true"
      >
        {{ $t('recipe_edit.delete') }}
      </button>

      <Modal
        v-if="deleteModal"
        :title="$t('recipe_edit.delete_title')"
        @close="deleteModal = false"
      >
        <span>{{ $t('recipe_edit.delete_confirm') }}</span>
        <button
          class="btn right"
          @click.prevent="deleteRecipe"
        >
          {{ $t('recipe_edit.delete') }}
        </button>
      </Modal>

      <button
        :disabled="saving"
        class="btn save"
        @click.prevent="save"
      >
        {{ $t('recipe_edit.save') }}
      </button>
    </div>

    <div v-if="newIngredientsDecision">
      <p>{{ $tc('recipes.confirm_new_ingredients.message', newIngredientsCount, {count: newIngredientsCount}) }}</p>
      <ul>
        <li
          v-for="(ingredient, i) in newIngredients"
          :key="i"
        >
          <div>{{ ingredient }}</div>
          <FormFieldValidationError
            :errors="(((newIngredientsError || [])[i] || {}).text) || []"
          />
        </li>
      </ul>
      <button
        class="btn"
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
    <div v-if="!newIngredientsDecision && newIngredientsError">
      <ul>
        <li
          v-for="(ingredient, i) in newIngredients"
          :key="i"
        >
          <div>{{ ingredient }}</div>
          <FormFieldValidationError
            :errors="(((newIngredientsError || [])[i] || {}).text) || []"
          />
        </li>
      </ul>
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
import Vue from 'vue'

import {api, endpoints} from '@/api'
import {clone} from '@/utils'
import DurationInput from '@/components/DurationInput'
import FormFieldValidationError from '@/components/FormFieldValidationError'
import RecipeEditIngredientTable from '@/components/RecipeEditIngredientTable'
import ImageUpload from '@/components/ImageUpload'
import Modal from '@/components/Modal'

const amount_types = {
  none: 1,
  numeric: 2,
  approx: 3,
}

export default {
  name: 'RecipeEditForm',
  components: {
    DurationInput,
    FormFieldValidationError,
    RecipeEditIngredientTable,
    ImageUpload,
    Modal
  },
  props: {
    recipe: {
      type: Object,
      default: function () {
        return {
          images: [],
          ingredient_groups: [],
          ingredients: [],
          title: '',
          description: '',
          estimated_work_duration: null,
          estimated_waiting_duration: null,
        }
      },
    },
  },
  data () {
    return {
      deleteModal: false,
      recipe_dirty: {
        ingredients: [{is_group: false, title: '', ingredients: []}],
        instructions: [this.createEmptyInstruction()],
        images: [],
        estimated_work_duration: null,
        estimated_waiting_duration: null,
      },
      /* Used to pass image data with urls to ImageUpload Component.
         recipe_diry.images is filled by the component and consists only of id's */
      images: null,
      saving: false,
      errors: {
        title: [],
        description: [],
        estimated_work_duration: [],
        estimated_waiting_duration: [],
        ingredients: [],
        ingredient_groups: [],
        instructions: [],
        client_side: '',
        detail: '',
      },
      newIngredientsDecision: null,
      newIngredients: [],
      newIngredientsCount: 0,
      newIngredientsError: [],
    }
  },
  computed: {
    author () {
      return this.recipe.author || this.$t('recipe_edit.unknown_user')
    },
    recipeIngredientError () {
      return i => {
        const subsetOfErrors = (this.errors.ingredients[i] || {}).ingredients
        return j => {
          const e = subsetOfErrors || []
          // note e might be a sparsely populated array
          const r = e.length > j ? (e[j] || {}) : {}
          for (let p of ['ingredient', 'ingredient_extra', 'amount_numeric', 'amount_approx', 'unit', 'optional']) {
            r[p] = r[p] || []
          }
          return r
        }
      }
    },
    recipeInstructionError () {
      return i => {
        const e = this.errors
        const r = e.length > i ? e[i] : {}
        for (let p of ['text']) {
          r[p] = r[p] || []
        }
        return r
      }
    },
    isExistingRecipe () {
      return !!this.recipe.id
    },
    canDeleteRecipe () {
      return this.isExistingRecipe && this.recipe.deletable
    },
  },
  watch: {
    recipe () {
      const r = this.recipe
      this.recipe_dirty = {
        title: r.title,
        description: r.description,
        estimated_work_duration: r.estimated_work_duration,
        estimated_waiting_duration: r.estimated_waiting_duration,
        instructions: clone(r.instructions || []),
        ingredients: clone(r.ingredients || []),
      }

      this.images = clone(r.images) || []
    }
  },
  methods: {
    addIngredientGroup () {
      this.recipe_dirty.ingredients.push(this.createEmptyIngredientGroup())
    },
    createEmptyIngredientGroup () {
      return {is_group: true, title: '', ingredients: []}
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
          const inquiredIngredients = [].concat(...this.recipe_dirty.ingredients.map(group => group.ingredients.map(i => i.ingredient)))
          const r = await api(endpoints.check_new_ingredients(), {
            ingredients: inquiredIngredients,
          })
          if (r.ok) {
            const newIngredients = (await r.json()).ingredients
            if (newIngredients.length > 0) {
              this.newIngredients.push(...newIngredients)
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
                  this.newIngredientsError.splice(0)
                  const r2 = await api(endpoints.create_many_ingredients(), newIngredientData)
                  if (r2.ok) {
                  } else {
                    this.newIngredientsError.push(...(await r2.json()))
                    return
                  }
                } else {
                  this.newIngredients.length = 0
                  this.newIngredientsCount = 0

                  return
                }
              } finally {
                this.newIngredientsDecision = null
              }
            }
          } else {
            // TODO: Proper error propagation
            const errors = await r.json()
            const errorsByIngredient = {}
            inquiredIngredients.forEach((k, i) => {
              errorsByIngredient[k] = errors.ingredients[String(i)]
            })
            this.recipe_dirty.ingredients.forEach((group, groupI) => {
              group.ingredients.forEach((ingredient, ingredientI) => {
                if (typeof errorsByIngredient[ingredient.ingredient] !== 'undefined') {
                  const thisError = errorsByIngredient[ingredient.ingredient]
                  if (typeof this.errors.ingredients[groupI] === 'undefined') {
                    Vue.set(this.errors.ingredients, groupI, {})
                  }
                  if (typeof this.errors.ingredients[groupI].ingredients === 'undefined') {
                    Vue.set(this.errors.ingredients[groupI], 'ingredients', [])
                  }
                  if (typeof this.errors.ingredients[groupI].ingredients[ingredientI] === 'undefined') {
                    Vue.set(this.errors.ingredients[groupI].ingredients, ingredientI, [])
                  }
                  if (typeof this.errors.ingredients[groupI].ingredients[ingredientI].ingredient === 'undefined') {
                    Vue.set(this.errors.ingredients[groupI].ingredients[ingredientI], 'ingredient', [])
                  }
                  this.errors.ingredients[groupI].ingredients[ingredientI].ingredient = thisError
                }
              })
            })
            return
          }
        }

        const d = {
          title: this.recipe_dirty.title,
          description: this.recipe_dirty.description,
          estimated_work_duration: this.recipe_dirty.estimated_work_duration,
          estimated_waiting_duration: this.recipe_dirty.estimated_waiting_duration,
          images: this.recipe_dirty.images,
          instructions: this.recipe_dirty.instructions.map((instruction, i) => { return {order: i, text: instruction.text}}),
          ingredients: this.recipe_dirty.ingredients,
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
          this.errors.description = errors.description || []
          this.errors.estimated_work_duration = errors.estimated_work_duration || []
          this.errors.estimated_waiting_duration = errors.estimated_waiting_duration || []
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
    async deleteRecipe () {
      this.saving = true
      try {
        const r = await api(endpoints.post_recipe(this.recipe.id), null, {method: 'delete'})
        if (r.ok) {
          this.$emit('remove', {})
        } else {
            this.errors.detail = errors.detail || ''
        }
      } finally {
        this.saving = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/variables.scss';

.description {
  margin-top: 5px;
  min-height: 100px;
}

.ingredients {
  margin-bottom: 5px;
  display: inline-block;
  box-sizing: border-box;
  width: 100%;
}

.instruction {
  display: flex;
  width: 100%;
  margin: 3px 0 3px 0;

  .text, textarea {
    width: 100%;
  }

  .btn {
    margin: auto 0 auto 5px;
  }
}

.addInstruction {
  height: 25px;
}

.images {
  padding: 10px;
}

.estimation {
  width: 100%;
  margin-top: 5px;
  display: flex;

  @media screen and (max-width: 500px) {
      flex-direction: column;
   }

  .column {
    @media screen and (min-width: 501px) {
      &:first-child {
         padding-right: 5px;
      }
      &:last-child {
        padding-left: 5px;
      }
      flex: 50%;
    }
  }
}

.options {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;

  .btn {
    margin-right: 0;
  }
}
</style>
