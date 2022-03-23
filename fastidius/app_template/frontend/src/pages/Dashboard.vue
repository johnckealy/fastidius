<template>
  <q-page class="flex flex-center">
    <h4>Welcome to the dashboard 🚀</h4>
  </q-page>
</template>

<script>
import { inject } from "vue";

export default {
  name: "DashBoard",
  setup() {
    const store = inject("store");
    const api = inject("api");
  },
};
</script>

<style>
</style>
