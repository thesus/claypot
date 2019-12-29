const AMOUNT_TYPE_NONE = 1
const AMOUNT_TYPE_NUMERIC = 2
const AMOUNT_TYPE_APPROX = 3

function createEmptyInstruction () {
  return {text: ''}
}

function createEmptyIngredient () {
  return {
    ingredient: '',
    ingredient_extra: '',
    optional: false,
    amount_type: AMOUNT_TYPE_NUMERIC,
    amount_approx: '',
    amount_numeric: 0,
    unit: '',
  }
}

function createEmptyIngredientGroup () {
  return {title: '', ingredients: [createEmptyIngredient()]}
}

function createDefaultRecipe () {
  return {
    id: null,
    ingredients: [createEmptyIngredientGroup()],
    instructions: [createEmptyInstruction()],
    images: [],
    estimated_work_duration: null,
    estimated_waiting_duration: null,
    description: ''
  }
}

function createDefaultRecipeError () {
  return {
    title: [],
    description: [],
    estimated_work_duration: [],
    estimated_waiting_duration: [],
    ingredients: [],
    ingredient_groups: [],
    instructions: [],
    client_side: '',
    detail: '',
  }
}

export {
  createEmptyIngredientGroup,
  createEmptyIngredient,
  createEmptyInstruction,
  createDefaultRecipe,
  createDefaultRecipeError,

  AMOUNT_TYPE_NUMERIC,
  AMOUNT_TYPE_APPROX,
  AMOUNT_TYPE_NONE
}
