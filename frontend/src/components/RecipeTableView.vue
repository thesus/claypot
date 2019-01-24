<template>
    <table>
        <thead>
            <tr>
                <th>Name</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="recipe in $props.recipes" :key="recipe.id">
                <td><recipe-link :recipe="recipe" /></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import RecipeLink from '@/components/RecipeLink'

export default {
    name: 'recipe-table',
    components: {
        RecipeLink
    },
    props: {
        recipes: Array
    }
}
</script>

<style lang="scss" scoped>
table {
    width: 100%;
    text-align: left;

    th {
        border-bottom: solid 1px #ccc;
    }
    td {
        border-bottom: solid 1px #eee;
    }
}
</style>

