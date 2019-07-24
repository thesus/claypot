<template>
  <span>
    <span @click="showModal = true">
      <span>{{ full }}</span>
      <span v-if="remainder !== 0">
        <sup>{{ remainder }}</sup>
        /
        <sub>{{ denominator }}</sub>
      </span>
    </span>
    <Modal v-if="showModal" @close="showModal = false">
      <div class="fraction-modal">
        <div>
          <input class="full" :value="full">
        </div>
        <div class="fraction">
          <input class="remainder" :value="remainder">
          <input class="denominator" :value="denominator">
        </div>
      </div>
    </Modal>
  </span>
</template>

<script>
import Modal from '@/components/Modal'

export default {
  components: {
    Modal,
  },
  props: {
    value: {
      type: Number,
      default: 1.0,
    },
  },
  data () {
    return {
      numerator: 1.0,
      denominator: 1.0,
      showModal: false,
    }
  },
  computed: {
    full () {
      return Math.floor(this.numerator / this.denominator)
    },
    remainder () {
      return this.numerator % this.denominator
    },
  },
}
</script>

<style lang="scss" scoped>
.fraction-modal {
  display: flex;
  flex-direction: row;

  & > div {
    flex: 1;
  }

  .fraction {
    display: flex;
    flex-direction: column;
  }
}
</style>
