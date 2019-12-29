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

export {
  createEmptyIngredientGroup,
  createEmptyIngredient,
  createEmptyInstruction,
  createDefaultRecipe,

  AMOUNT_TYPE_NUMERIC,
  AMOUNT_TYPE_APPROX,
  AMOUNT_TYPE_NONE
}
