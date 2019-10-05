<template>
  <article>
    <header>
      <div class="drafts">
        <select
          v-if="drafts.length"
          class="select"
          @input="getDraft($event.target.value)"
        >
          <option
            disabled
            selected
            value
          >
            {{ $t('recipes.draft.multiple') }}
          </option>
          <option
            v-for="d in drafts"
            :key="d.id"
            :value="d.id"
          >
            {{ d.id }}
          </option>
        </select>

        <button
          v-else-if="recipe.draft_id"
          class="btn right"
          :disabled="!(recipe.draft_id && !draft)"
          @click="getDraft(recipe.draft_id)"
        >
          {{ $t('recipes.draft.single') }}
        </button>
      </div>

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
          <div>{{ ingredient }}</div>
          <FormFieldValidationError
            :errors="(((newIngredientsError || [])[i] || {}).text) || []"
          />
        </li>
      </ul>
      <button
        class="btn right"
        @click="newIngredientsDecision(true)"
      >
        {{ $tc('recipes.confirm_new_ingredients.accept', newIngredientsCount, {count: newIngredientsCount}) }}
      </button>
    </Modal>

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
import DurationInput from '@/components/recipe-edit/DurationInput'
import FormFieldValidationError from '@/components/utils/FormFieldValidationError'
import RecipeEditIngredientTable from '@/components/recipe-edit/RecipeEditIngredientTable'
import ImageUpload from '@/components/recipe-edit/ImageUpload'
import Modal from '@/components/utils/Modal'

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
          id: null,
          maingredient_groups: [],
          ingredients: [],
          title: '',
          description: '',
          estimated_work_duration: null,
          estimated_waiting_duration: null,
          draft_id: null,
        }
      },
    },
  },
  data () {
    return {
      deleteModal: false,
      drafts: [], /* Draft list for new recipes */
      draft: null, /* Currently selected draft, gets deleted after succesfull save */
      autosave: true, /* Save timer is running */
      changed: false,
      ...this.createDefaultRecipeDirty(),
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
    ingredientList () {
      return [].concat(...this.recipe_dirty.ingredients.map(group => group.ingredients.map(i => i.ingredient)))
    }
  },
  watch: {
    recipe_dirty: {
      handler () {
        if  (!this.autosave) {
          this.autosave = true
          this.saveDraft()

          /* Allow autosave again after 10 seconds */
          setTimeout(() => {
              this.autosave = false

              if (this.changed) {
                this.saveDraft()
                this.changed = false
                this.autosave = true
              }
          }, 10000)
        } else {
          this.changed = true
        }
      },
      deep: true
    },
    recipe: {
      handler () {
        if (!this.isExistingRecipe) {
          /* If this is a new recipe load drafts that are not associated with a recipe */
          this.getDraftList()
        } else {
          this.drafts = []
        }
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
      },
      immediate: true
    }
  },
  mounted () {
    /* Enable draft saving after 15 seconds. */
    setTimeout(() => {
      this.autosave = false
    }, 15000)
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
    createDefaultRecipeDirty () {
      return {
        recipe_dirty: {
          ingredients: [{is_group: false, title: '', ingredients: []}],
          instructions: [this.createEmptyInstruction()],
          images: [],
          estimated_work_duration: null,
          estimated_waiting_duration: null,
          description: ''
        }
      }
    },
    addInstruction () {
      this.recipe_dirty.instructions.push(this.createEmptyInstruction())
    },
    async getDraftList () {
      const r = await api(
        endpoints.recipe_draft()
      )
      if (r.ok) {
        this.drafts = (await r.json()).results
      }
    },
    async getDraft (id) {
      /* Set the current draft to the loaded one. */
      this.draft = id

      const r = await api(
        endpoints.recipe_draft(id)
      )
      if (r.ok) {
        /* Replace current version with the draft. Merged with the default, in case the saved draft is incomplete. */
        this.recipe_dirty = { ...this.createDefaultRecipeDirty(), ...(await r.json()).data }
      }
    },
    async saveDraft () {
      /* If save is called on a existing recipe with a existing draft, overwrite the draft. */
      /* This disables the 'load draft' button. */
      if (!this.draft && this.recipe.draft_id) {
        this.draft = this.recipe.draft_id
      }

      const r = await api(
        endpoints.recipe_draft(this.draft),
        { data: this.recipe_dirty, recipe: this.recipe.id },
        { method: this.draft ? 'put' : 'post' }
      )

      /* If a new draft is created, set the id for the next save */
      if (!this.draft && r.ok) {
        this.draft = (await r.json()).id
      }
    },
    async deleteDraft (id) {
      await api(
        endpoints.recipe_draft(id),
        null,
        { method: 'delete' }
      )
    },
    async save () {
      this.saveDraft()

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
                  // this will give the user a choice to cancel or continue the process. Executed with a call to newIngredientsDecision(true) or newIngredientsDecision(false)
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

          /* If a draft is created or loaded earlier, delete it after succesfull saving */
          if (this.draft) {
            await this.deleteDraft(this.draft)
          }

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

.drafts {
  display: inline-block;
  width: 100%;
}
</style>
