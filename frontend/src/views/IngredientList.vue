<template>
  <div>
    <DebounceInput
      v-model="search"
      :placeholder="$t('home.search')"
      class="search"
    />
    <Receiver
      :endpoint="endpoint"
      :filters="combinedFilters"
      @pagination="updatePagination"
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

    <Pagination
      :next="next"
      :previous="previous"
      @update="setPage"
    />
  </div>
</template>

<script>
import { api, endpoints } from '@/api'

import Receiver from '@/components/Receiver'
import DebounceInput from '@/components/DebounceInput'

import Pagination from '@/components/Pagination'
import { PaginationMixin } from '@/mixins/pagination'

export default {
  components: {
    Receiver,
    DebounceInput,
    Pagination
  },
  mixins: [PaginationMixin],
  data () {
    return {
      endpoint: endpoints.fetch_ingredients(),
      search: ''
    }
  },
  computed: {
    filters () {
      return this.search != '' ? { name: this.search } : {}
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/table.scss';

.search {
  margin-bottom: 10px;
}
</style>
