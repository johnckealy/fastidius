<template>
  <q-page class="flex flex-center">
    <login-form />
  </q-page>
</template>

<script>
import LoginForm from "../components/LoginForm.vue";

export default {
  name: "MainLayout",
  components: {
    LoginForm,
  }
};
</script>

<style>
</style>
