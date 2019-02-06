function getCookie(name) {
  const value = "; " + document.cookie
  const parts = value.split("; " + name + "=");
  if (parts.length == 2) {
    return parts.pop().split(";").shift();
  }
  return null
}

function sortedUnifiedIngredients (recipe) {
  if (!recipe || !recipe.ingredients || !recipe.ingredient_groups) {
    return []
  }
  const sorted = [
    ...recipe.ingredients,
    ...recipe.ingredient_groups.map(i => {
      const r = Object.assign({isGroup: true}, i)
      r.ingredients = r.ingredients.sort(i => -i.order)
      return r
    }),
  ].sort(i => -i.order)
  // pack ungrouped ingredients into arrays
  const result = []
  let tmp = []
  for (let i of sorted) {
    if (!i.isGroup) {
      tmp.push(i)
    } else {
      if (tmp.length > 0) {
        result.push({isGroup: false, ingredients: tmp, title: ''})
        tmp = []
      }
      result.push(i)
    }
  }
  if (tmp.length > 0) {
    result.push({isGroup: false, ingredients: tmp, title: ''})
  }
  return result
}

export {
  getCookie,
  sortedUnifiedIngredients,
}
