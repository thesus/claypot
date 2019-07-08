<template>
  <div>
    <Receiver :endpoint="endpoint">
      <template v-slot:default="props">
        <table>
          <thead>
            <tr>
              <th>Name</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="ingredient in props.data"
              :key="ingredient.id"
            >
              <td>
                <router-link
                  :to="{name: 'ingredient-edit', params: {id: ingredient.id }}"
                >
                  {{ ingredient.name }}
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
    </Receiver>
  </div>
</template>

<script>
import { api, endpoints } from '@/api'

import Receiver from '@/components/Receiver'

export default {
  components: {
    Receiver
  },
  data () {
    return {
      endpoint: endpoints.fetch_ingredients()
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/table.scss';
</style>
