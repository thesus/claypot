<template>
  <article v-if="recipe != null">
    <fieldset :disabled="saving">
      <Draft
        ref="drafts"
        :recipe="recipe"
        @draftLoad="loadDraft"
      />

      <input
        v-model="recipe.title"
        :placeholder="$t('recipes.title')"
        :class="formError('title')"
      >
      <FormFieldValidationError :errors="errors.title" />

      <textarea
        v-model="recipe.description"
        :placeholder="$t('recipes.description')"
        class="description"
        :class="formError('description')"
      />
      <FormFieldValidationError :errors="errors.description" />

      <div class="images">
        <ImageUpload
          v-model="recipe.images"
          :initial="imagesInitial"
        />
      </div>

      <div class="ingredients">
        <RecipeEditIngredientTable
          v-for="(group, i) in recipe.ingredients"
          :key="i"
          :single="recipe.ingredients.length == 1"
          :group.sync="recipe.ingredients[i]"
          :recipe-ingredient-error="recipeIngredientError(i)"
          @remove="recipe.ingredients.splice(i, 1)"
        />

        <button
          class="btn right"
          @click.prevent="addIngredientGroup"
        >
          {{ $t('recipe_edit.add_group') }}
        </button>
      </div>

      <div
        v-for="(instruction, i) in recipe.instructions"
        :key="i"
        class="instruction"
      >
        <div class="text">
          <textarea
            v-model="instruction.text"
            :placeholder="$t('recipes.instructions')"
            class="small"
          />
          <FormFieldValidationError
            :errors="recipeInstructionError(i).text"
          />
        </div>
        <button
          tabindex="-1"
          class="btn remove"
          @click="recipe.instructions.splice(i, 1)"
        >
          {{ $t('recipe_edit.remove') }}
        </button>
      </div>

      <div
        class="addInstruction"
      >
        <button
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
            v-model="recipe.estimated_work_duration"
          />
        </div>

        <div class="column">
          <label>
            {{ $t('recipe_edit.estimated_waiting_duration') }}
          </label>
          <duration-input
            v-model="recipe.estimated_waiting_duration"
          />
        </div>
      </div>

      <div class="options">
        <button
          v-if="canDeleteRecipe"
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
          class="btn save"
          @click.prevent="save"
        >
          {{ $t('recipe_edit.save') }}
        </button>
      </div>

      <div v-if="errors.client_side">
        {{ errors.client_side }}
      </div>
      <div v-if="errors.detail">
        {{ errors.detail }}
      </div>
    </fieldset>

    <Modal
      v-if="newIngredientsDecision"
      @close="newIngredientsDecision(false)"
    >
      <p>{{ $tc('recipes.confirm_new_ingredients.message', newIngredientsCount, {count: newIngredientsCount}) }}</p>
      <ul>
        <li
          v-for="(ingredient, i) in newIngredients"
          :key="i"
        >
          {{ ingredient }}
        </li>
      </ul>
      <button
        class="btn right"
        @click="newIngredientsDecision(true)"
      >
        {{ $tc('recipes.confirm_new_ingredients.accept', newIngredientsCount, {count: newIngredientsCount}) }}
      </button>
    </Modal>

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
import DurationInput from '@/components/recipe-edit/DurationInput'
import FormFieldValidationError from '@/components/utils/FormFieldValidationError'
import RecipeEditIngredientTable from '@/components/recipe-edit/RecipeEditIngredientTable'
import ImageUpload from '@/components/recipe-edit/ImageUpload'
import Modal from '@/components/utils/Modal'

import Draft from '@/components/recipe-edit/Draft'
import { createDefaultRecipe, createEmptyIngredientGroup, createEmptyInstruction, createDefaultRecipeError } from '@/components/recipe-edit/utils'

export default {
  name: 'RecipeEditForm',
  components: {
    DurationInput,
    FormFieldValidationError,
    RecipeEditIngredientTable,
    ImageUpload,
    Modal,
    Draft
  },
  props: {
    id: {
      type: Number,
      default: null
    }
  },
  data () {
    return {
      deleteModal: false,
      saving: false,

      errors: createDefaultRecipeError(),
      // Gets populated if id changes or immediately
      recipe: null,

      // Initial state of images, @see this.loadRecipe
      imagesInitial: [],
      newIngredientsDecision: null,
      newIngredients: [],
      newIngredientsCount: 0,
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
      return !!this.id
    },
    canDeleteRecipe () {
      return this.isExistingRecipe && this.recipe.deletable
    },
    ingredientList () {
      return [].concat(...this.recipe.ingredients.map(group => group.ingredients.filter(i => i.ingredient != "").map(i => i.ingredient)))
    }
  },
  watch: {
    id: {
      handler () {
        if (this.id != null) {
          this.loadRecipe()
        } else {
          this.$set(this, 'recipe', createDefaultRecipe())
        }
      },
      immediate: true
    }
  },
  methods: {
    formError (key) {
      return {
        'form-error': !!this.errors[key].length
      }
    },
    /**
    * Replaces the current recipe with the draft.
    */
    loadDraft (value) {
      this.recipe = value
    },
    addIngredientGroup () {
      this.recipe.ingredients.push(createEmptyIngredientGroup())
    },
    addInstruction () {
      this.recipe.instructions.push(createEmptyInstruction())
    },
    async save () {
      // Save draft before trying to save the recipe
      const draftSavePromise = this.$refs.drafts.saveDraft()

      this.saving = true
      try {
        // Step 1: Check for new ingredients
        {
          const r = await api(endpoints.check_new_ingredients(), {
            ingredients: this.ingredientList,
          })

          if (r.ok) {
            const newIngredients = (await r.json()).ingredients
            if (newIngredients.length > 0) {
              this.newIngredients.push(...newIngredients)
              this.newIngredientsCount = newIngredients.length
              try {
                const userDecision = await new Promise((resolve) => {
                  // this will give the user a choice to cancel or continue the process.
                  // Executed with a call to newIngredientsDecision(true) or newIngredientsDecision(false)
                  this.newIngredientsDecision = resolve
                })
                if (!userDecision) {
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
            this.ingredientList.forEach((k, i) => {
              errorsByIngredient[k] = errors.ingredients[String(i)]
            })

            this.recipe.ingredients.forEach((group, groupIndex) => {
              group.ingredients.forEach((ingredient, ingredientIndex) => {
                // create group
                if (!this.errors.ingredients[groupIndex]) {
                  this.$set(this.errors.ingredients, groupIndex, {ingredients: []})
                }
                // create ingredient in group
                if (!this.errors.ingredients[groupIndex].ingredients[ingredientIndex]) {
                  this.$set(this.errors.ingredients[groupIndex].ingredients, ingredientIndex, {})
                }

                // Append error
                const error = errorsByIngredient[ingredient.ingredient]
                if (error) {
                    this.$set(
                    this.errors.ingredients[groupIndex].ingredients[ingredientIndex],
                    'ingredient',
                    error
                  )
                }
              })
            })

            return
          }
        }

        const d = {
          title: this.recipe.title,
          description: this.recipe.description,
          estimated_work_duration: this.recipe.estimated_work_duration,
          estimated_waiting_duration: this.recipe.estimated_waiting_duration,
          images: this.recipe.images,
          instructions: this.recipe.instructions.map((instruction, i) => { return {order: i, text: instruction.text}}),
          ingredients: this.recipe.ingredients,
        }

        const r = await api(endpoints.post_recipe(this.recipe.id), d, {method: this.recipe.id ? 'put' : 'post'})
        if (r.ok) {
          this.errors.client_side = ''
          this.recipe = await r.json()

        // If a draft is created or loaded earlier, delete it after succesfull saving
        // Draft must be saved before it can be removed
        await draftSavePromise
        this.$refs.drafts.deleteDraft()

        // Close page on success
        this.$emit('update', this.recipe.id)
        } else {
          // TODO: Notify user about broken fields?

          this.$set(this, 'errors', {...createDefaultRecipeError(), ...(await r.json())})
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
    async loadRecipe () {
      try {
        this.$emit('loadingStart')

        const response = await api(endpoints.fetch_recipe(this.id))

        if (response.ok) {
          const recipe = await response.json()

          // inital images consists of url for the thumbnails
          // on save recipe.images is an array of ids of the images
          this.imagesInitial = recipe.images
          delete recipe.images

          this.$set(this, 'recipe', recipe)
        } else {

        }
      } catch (error) {
        this.$emit('error', error)
      } finally {
        this.$emit("loadingEnd")
      }
    }
  }
}
</script>

<style lang="scss" scoped>
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
