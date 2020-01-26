<template>
  <transition name="modal">
    <div class="mask">
      <div class="wrapper">
        <div class="flex">
          <div class="container">
            <div class="header">
              <h2>{{ title }}</h2>
              <button
                class="btn"
                @click="$emit('close')"
              >
                Close
              </button>
            </div>
            <slot />
            <div style="clear: both;" />
          </div>
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

.mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  background-color: rgba(0, 0, 0, .5);

  display: table;
  transition: opacity .3s ease;

  z-index: 2000;
}

.flex {
  display: flex;
}

.wrapper {
  display: table-cell;
  vertical-align: middle;
}

.container {
  min-width: 220px;
  max-width: 600px;

  width: 66vw;
  margin: 0px auto;
  padding: 12px;

  transition: all .3s ease;
  background-color: white;


  .header {
    display: grid;
    grid-template-columns: 5fr 1fr;
    margin-bottom: 5px;

    h2 {
      margin: 0;
      text-align: left;
    }

    .btn {
      margin: 0;
    }
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

.btn {
  min-width: unset;
}
</style>
