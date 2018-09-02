import Vue from 'vue';
import axios from 'axios';
import Multiselect from 'vue-multiselect';
import 'babel-polyfill';

new Vue({
  el: '#search',
  delimiters: ['{(', ')}'],
  components: {
    'multiselect': Multiselect
  },
  data () {
    return {
      searchTerm: '',
      searchTags: [],
      recipes: [],
      allTags: ['Gluten', 'Milch']
    }
  },
  computed: {
    getSearch() {
      let params = {}
      if (this.searchTags.length >= 1) {
        params['tags']= this.searchTags.join(",")
      }
      if (this.searchTerm.length >= 1) {
        params['title'] = this.searchTerm
      }
      return params
    }
  },
  methods: {
    async runSearch() {
      let response = await axios.get(
        '/recipes/search',
        {
          params: this.getSearch
        }
      )
      this.$set(this, 'recipes', response.data)
    }
  },
  watch: {
    getSearch () {
      this.runSearch()
    }
  }
})
