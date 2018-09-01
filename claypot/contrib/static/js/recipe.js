import Vue from 'vue';
import axios from 'axios';
import 'babel-polyfill';

new Vue({
    el: '#recipe',
    delimiters: ['{(', ')}'],
    data () {
        return {
            'recipe': {}
        }
    },
    mounted () {
        this.getRecipe()
    },
    methods: {
        async getRecipe () {
            let url = '/' + location.pathname.substring(1)
            var response = axios.get(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).catch((error) => {
                console.log(error)
            })
            this.$set(this, 'recipe', await response.data)
        }
    }
})
