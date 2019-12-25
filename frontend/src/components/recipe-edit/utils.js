function createEmptyIngredientGroup () {
  return {is_group: true, title: '', ingredients: []}
}

function createEmptyInstruction () {
  return {text: ''}
}

function createDefaultRecipe () {
  return {
    id: null,
    ingredients: [{is_group: false, title: '', ingredients: []}],
    instructions: [createEmptyInstruction()],
    images: [],
    estimated_work_duration: null,
    estimated_waiting_duration: null,
    description: ''
  }
}

export {
  createEmptyIngredientGroup,
  createEmptyInstruction,
  createDefaultRecipe
}
