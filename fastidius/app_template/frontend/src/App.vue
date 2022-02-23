<template>
  <router-view />
</template>


<script>
import { provide } from 'vue';
import store from 'src/store';

export default {
  setup() {
    provide('store', store)
  }
}

</script>
