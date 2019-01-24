<template>
  <article>
    <header>
      <div><input :placeholder="$t('recipes.title')" v-model="recipe_dirty.title" :disabled="saving" :class="{'form-error': !!errors.title.length}"></div>
      <form-field-validation-error :errors="errors.title" />
    </header>

    <div class="ingredients">
      <div class="table">
        <table v-show="recipe_dirty.ingredients.length > 0">
          <thead>
            <tr>
              <th>{{ $t('recipe_edit.amount') }}</th>
              <th>{{ $t('recipe_edit.unit') }}</th>
              <th>{{ $t('recipe_edit.ingredient') }}</th>
              <th>{{ $t('recipe_edit.ingredient_extra') }}</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(ingredient, i) in recipe_dirty.ingredients" :key="i" ref="ingredients">
              <td>
                <div class="input">
                  <input v-model="ingredient.amount_numeric" :class="{'form-error': !!recipeIngredientError(i).amount_numeric.length}">
                </div>
                <form-field-validation-error :errors="recipeIngredientError(i).amount_numeric" />
              </td>
              <td>
                <div class="input">
                  <input v-model="ingredient.unit" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).unit.length}">
                </div>
                <form-field-validation-error :errors="recipeIngredientError(i).unit" />
              </td>
              <td>
                <div class="input">
                  <ingredient-input v-model="ingredient.ingredient" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).ingredient.length}" />
                </div>
                <form-field-validation-error :errors="recipeIngredientError(i).ingredient" />
              </td>
              <td>
                <div class="input">
                  <input v-model="ingredient.ingredient_extra" :disabled="saving" :class="{'form-error': !!recipeIngredientError(i).ingredient_extra.length}">
                </div>
                <form-field-validation-error :errors="recipeIngredientError(i).ingredient_extra" />
              </td>
              <td><button tabindex="-1" class="btn btn-right remove" :disabled="saving" @click="recipe_dirty.ingredients.splice(i, 1)">{{ $t('recipe_edit.remove') }}</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      <button class="btn btn-right submit" @click.prevent="addIngredient" :disabled="saving">{{ $t('recipe_edit.add') }}</button>
    </div>

    <ol>
      <li v-for="(instruction, i) in recipe_dirty.instructions" ref="instructions">
        <div><textarea class="small" :placeholder="$t('recipes.instructions')" v-model="instruction.text" :disabled="saving"></textarea></div>
        <form-field-validation-error :errors="recipeInstructionError(i).text" />
        <button tabindex="-1" class="btn btn-right remove" :disabled="saving" @click="recipe_dirty.instructions.splice(i, 1)">{{ $t('recipe_edit.remove') }}</button>
      </li>
    </ol>
    <div>
      <button class="btn btn-right submit" @click.prevent="addInstruction" :disabled="saving">{{ $t('recipe_edit.add') }}</button>
    </div>

    <div><button class="btn btn-right btn-primary" @click.prevent="save" :disabled="saving">{{ $t('recipe_edit.save') }}</button></div>
    <div v-if="newIngredientsDecision">
      <p>{{ $tc('recipes.confirm_new_ingredients.message', newIngredientsCount, {count: newIngredientsCount}) }}</p>
      <button class="btn new-ingredient" @click="newIngredientsDecision(true)">{{ $tc('recipes.confirm_new_ingredients.accept', newIngredientsCount, {count: newIngredientsCount}) }}</button>
      <button class="btn" @click="newIngredientsDecision(false)">{{ $tc('recipes.confirm_new_ingredients.decline', newIngredientsCount, {count: newIngredientsCount}) }}</button>
    </div>
    <div v-if="errors.client_side">{{ errors.client_side }}</div>
    <div v-if="errors.detail">{{ errors.detail }}</div>

    <footer>
      <p v-if="recipe.id">{{ $t('recipe_edit.posted_by',  {user: author}) }}</p>
    </footer>
  </article>
</template>

<script>
import {api, endpoints} from '@/api'
import FormFieldValidationError from '@/components/FormFieldValidationError'
import IngredientInput from '@/components/IngredientInput'

const amount_types = {
  none: 1,
  numeric: 2,
  approx: 3,
}

export default {
  name: 'recipe-edit-form',
  components: {
    FormFieldValidationError,
    IngredientInput,
  },
  props: {
    recipe: Object,
  },
  data () {
    return {
      recipe_dirty: {
        ingredients: [this.createEmptyIngredient()],
        instructions: [this.createEmptyInstruction()],
      },
      saving: false,
      errors: {
        title: [],
        ingredients: [],
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
        const e = this.errors.ingredients
        const r = e.length > i ? e[i] : {}
        for (let p of ['ingredient', 'ingredient_extra', 'amount_numeric', 'unit']) {
          r[p] = r[p] || []
        }
        return r
      }
    },
    recipeInstructionError () {
      return i => {
        const e = this.errors.instructions
        const r = e.length > i ? e[i] : {}
        for (let p of ['text']) {
          r[p] = r[p] || []
        }
        return r
      }
    },
  },
  methods: {
    createEmptyIngredient () {
      return {ingredient: '', ingredient_extra: '', amount_numeric: 0, unit: ''}
    },
    createEmptyInstruction () {
      return {text: ''}
    },
    addIngredient () {
      this.recipe_dirty.ingredients.push(this.createEmptyIngredient())

      const pos = this.recipe_dirty.ingredients.length - 1
      /* Select the first field in the input after it was created */
      /* And yeah. This is pretty dirty. */
      this.$nextTick(() => { this.$refs.ingredients[pos].children[0].children[0].children[0].focus() })
    },
    addInstruction () {
      this.recipe_dirty.instructions.push(this.createEmptyInstruction())

      const pos = this.recipe_dirty.instructions.length - 1
      /* Select the first field in the input after it was created */
      /* And yeah. This is pretty dirty. */
      this.$nextTick(() => { this.$refs.instructions[pos].children[0].children[0].focus() })
    },
    async save () {
      this.saving = true
      try {
        // Step 1: Check for new ingredients
        {
          const r = await api(endpoints.check_new_ingredients(), {
            ingredients: this.recipe_dirty.ingredients.map(i => i.ingredient),
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

        const ri = this.recipe_dirty.ingredients.map((i, order) => {
          return {
            order: order,
            ingredient: i.ingredient,
            ingredient_extra: i.ingredient_extra,
            optional: false,
            amount_type: amount_types.numeric,
            amount_numeric: Number(i.amount_numeric),
            amount_approx: '',
            unit: i.unit,
          }
        })
        const d = {
          title: this.recipe_dirty.title,
          instructions: this.recipe_dirty.instructions.map((instruction, i) => { return {order: i, text: instruction.text}}),
          ingredients: ri,
          ingredient_groups: [],
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
  watch: {
    recipe () {
      const r = this.recipe
      this.recipe_dirty = {
        title: r.title,
        ingredients: [],
        instructions: r.instructions,
      }
      for (let ri of r.ingredients) {
        this.recipe_dirty.ingredients.push({
          amount_numeric: ri.amount_numeric,
          amount_approx: ri.amount_approx,
          amount_type: ri.amount_type,
          ingredient: ri.ingredient,
          ingredient_extra: ri.ingredient_extra,
          unit: ri.unit,
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
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

article {
  margin: 5px;
  /* smaller after threshold?
  @media screen and (min-width: 1000px) {
    width: 60%;
    margin: auto;
  }
  */
}
</style>
