<template>
  <div
    v-if="drafts.length || recipe.draft"
    class="drafts"
  >
    <select
      v-if="drafts.length"
      class="select"
      @input="getDraft($event.target.value)"
    >
      <option
        disabled
        selected
        value
      >
        {{ $t('recipes.draft.multiple') }}
      </option>
      <option
        v-for="d in drafts"
        :key="d.id"
        :value="d.id"
      >
        {{ getDraftString(d) }}
      </option>
    </select>

    <button
      v-else-if="recipe.draft"
      class="btn right"
      :disabled="!(recipe.draft && !draft)"
      @click="getDraft(recipe.draft)"
    >
      {{ $t('recipes.draft.single') }}
    </button>
  </div>
</template>

<script>
import { api, endpoints } from '@/api'
import { createDefaultRecipe } from '@/components/recipe-edit/utils'

export default {
  name: 'Draft',
  props: {
    recipe: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      drafts: [],
      draft: null,

      autoSaveEnabled: false,
      saveScheduled: false,

      timer: {
        autoSaveDelay: null,
        autoSaveLoop: null
      }
    }
  },
  watch: {
      /* Desired behaviour:
         `autoSaveEnabled` is `false` initially and is automatically changed to `true` after 15 seconds.
         If a change to any part of the recipe happens before that first 15 second interval, no draft will be saved. This is intentional.
         If a change happens after this first 15 seconds, the recipe will be saved as a draft, but at most once every 10 seconds.
         Also note: If changes happen in the first 15 seconds, but no changes happen after that, no draft will be saved; this is intentional as well.
       */
    recipe: {
      handler() {
        // If this is a new recipe load the draft list
        if (!this.recipe.id) {
          this.getDraftList()
        }

        if (this.autoSaveEnabled && !this.saveScheduled) {
          this.saveScheduled = true

          this.timer.autoSaveLoop = setTimeout(() => {
            this.saveDraft()
            this.saveScheduled = false
          }, 10000)
        }
      },
      deep: true,
    }
  },
  mounted () {
    this.timer.autoSaveDelay = setTimeout(() => {
      this.autoSaveEnabled = true
    }, 15000)
  },
  beforeDestroy () {
    clearTimeout(this.timer.autoSaveDelay)
    clearTimeout(this.timer.autoSaveLoop)

    // Save immediately beforeDestroy closing
    if (this.changed && this.draft) {
      this.saveDraft()
    }
  },
  methods: {
    /**
    * Formats a draft in a human readable format
    */
    getDraftString(draft) {
      return new Date(draft.date).toLocaleString() + " " + (draft.title || this.$t('recipes.draft.no_title'))
    },
    /**
    * Saves the current draft.
    * If a draft is selected, the existing one is overwritten.
    */
    async saveDraft () {
      // This disables the 'load draft' button.
      if (!this.draft && this.recipe.draft) {
        this.draft = this.recipe.draft
      }

      try {
        const r = await api(
          endpoints.recipe_draft(this.draft),
          { data: this.recipe, recipe: this.recipe.id },
          { method: this.draft ? 'put' : 'post' }
        )

        // If a new draft is created, set the id for the next save
        if (!this.draft && r.ok) {
          this.draft = (await r.json()).id
        }
      } catch (e) {
        // TODO (till): Error handling
        console.log(e)
      }
    },
    async getDraft (id) {
      // Set the current draft to the loaded one.
      this.draft = id

      try {
        const r = await api(
          endpoints.recipe_draft(id)
        )
        if (r.ok) {
          // Replace current version with the draft. Merged with the default, in case the saved draft is incomplete.

          this.$emit(
            'draftLoad',
            { ...createDefaultRecipe(), ...(await r.json()).data }
          )
        }
      } catch (e) {
        // Don't show visual indication
        console.log(e)
      }
    },
    /**
    * Deletes a draft by a given id.
    * @param id: draft id to delete
    */
    async deleteDraft () {
      // TODO (till) : Error handling
      await api(
        endpoints.recipe_draft(this.draft),
        null,
        { method: 'delete' }
      )
    },
    async getDraftList () {
      try {
        const r = await api(
          endpoints.recipe_draft()
        )
        if (r.ok) {
          this.drafts = (await r.json()).results
        }
      } catch (e) {
        // Don't show visual indication
        console.log(e)
      }
    },
  }
}
</script>

<style lang="scss" scoped>
.drafts {
  display: inline-block;
  width: 100%;

  .select {
    float: right;
  }
}
</style>
