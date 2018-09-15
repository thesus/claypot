<template>
  <div>
      {{ recipe }}
  </div>
</template>

<script>

export default {
  name: 'home',
  apollo: {
    recipe: gql`query {
          recipes(instructions_Icontains: "180") {
            edges {
              node {
                id
                title
                instructions
                recipeIngredients {
                  edges {
                    node {
                      id
                      ingredient {
                        name
                      }
                      amountType
                      amountNumeric
                      amountApprox
                      unit {
                        id
                        name
                        code
                        namePlural
                      }
                    }
                  }
                }
              }
            }
          }
        }`
  },
  data () {
    return {
      recipe: null
    }
  }
}
</script>
