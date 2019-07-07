<template>
  <div>
    <Receiver :endpoint="endpoint">
      <template v-slot:default="props">
        <table>
          <tr
            v-for="ingredient in props.data"
            :key="ingredient.id"
          >
            <td>{{ ingredient.name }}</td>
          </tr>
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
</style>
