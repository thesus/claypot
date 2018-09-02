import Vue from 'vue';
import axios from 'axios';
import 'babel-polyfill';
import Multiselect from 'vue-multiselect';


new Vue({
  el: '#recipe',
  delimiters: ['{(', ')}'],
  components: {
    'multiselect': Multiselect
  },
  data () {
    return {
      'searches': [],
      'newIngredients': [],
      'recipe': {},
      'ingredients': [],
      'url': '/' + location.pathname.substring(1),
      'config': {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      }
    }
  },
  mounted () {
    this.getRecipe()
    this.findIngredients('', -1)
  },
  computed: {
    getIngredients () {
      return this.ingredients.concat(this.newIngredients)
    }
  },
  methods: {
    isSearchLoading(id) {
      return this.searches.includes(id)
    },
    getAmount(id) {
      let ingredient = this.recipe.recipe_ingredients[id]
      return (ingredient.amount_numeric != null) ? ingredient.amount_numeric : ingredient.amount_approx
    },
    setAmount(event) {
      let id = parseInt(event.target.attributes.index.value)
      let ingredient = this.recipe.recipe_ingredients[id]
      let val = event.target.value
      if (isNaN(val)) {
        this.$set(ingredient, 'amount_approx', val)
        this.$set(ingredient, 'amount_type', 3)
        ingredient.amount_numeric = null
      } else {
        this.$set(ingredient, 'amount_numeric', Number(val))
        this.$set(ingredient, 'amount_type', 2)
        ingredient.amount_approx = null
      }
    },
    async getRecipe () {
      var response = await axios.get(this.url, this.config).catch(
        (error) => {
          console.log(error)
        }
      )

      let recipe = response.data
      this.$set(this, 'recipe', response.data)
    },
    async findIngredients(search, id) {
      this.searches.push(id)
      let searchUrl = '/ingredients?search=' + search
      var response = await axios.get(searchUrl, this.config).catch(
        (error) => {
          console.log(error)
          return
        }
      )
      this.$set(this, 'ingredients', response.data.search)
      let index = this.searches.indexOf(id)
      if (index > -1) {
        this.searches.splice(index, 1)
      }
    },
    createIngredient(search, id) {
      this.$set(
        this.recipe.recipe_ingredients[id],
        'ingredient',
        search
      )
      this.newIngredients.push(search)
    }
  }
})
