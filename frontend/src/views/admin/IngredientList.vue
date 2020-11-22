<template>
  <div>
    <DebounceInput
      v-model="search"
      :placeholder="$t('home.search')"
      class="search"
    />
    <Receiver
      :endpoint="endpoint"
      :filters="filters"
    >
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
import { mapActions } from 'vuex'
import { api, endpoints } from '@/api'

import Receiver from '@/components/utils/Receiver'
import DebounceInput from '@/components/utils/DebounceInput'

export default {
  components: {
    Receiver,
    DebounceInput
  },
  data () {
    return {
      endpoint: endpoints.fetch_ingredients(),
      search: '',
      simple: false
    }
  },
  computed: {
    filters () {
      return this.search != '' ? { name: this.search } : {}
    }
  },
  mounted () {
    this.updateTitle({name: "titles.admin.ingredient-list"})
  },
  methods: {
    ...mapActions(["updateTitle"]),
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/table.scss';

.search {
  margin-bottom: 10px;
}
</style>
