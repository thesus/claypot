<template>
  <transition name="modal">
    <div class="mask">
      <div class="wrapper">
        <div class="container">
          <div class="header">
            <button class="btn right" @click="$emit('close')">Close</button>
            <h2>{{ title }}</h2>
          </div>
          <slot />
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: ''
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  background-color: rgba(0, 0, 0, .5);

  display: table;
  transition: opacity .3s ease;
}

.wrapper {
  display: table-cell;
  vertical-align: middle;
}

.container {
  width: 200px;
  height: 100px;
  margin: 0px auto;
  padding: 4px;

  transition: all .3s ease;
  background-color: white;

  .header {
    h2 {
      margin: 0;
    }

    height: 30px;
    width: 100%;
  }
}

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
