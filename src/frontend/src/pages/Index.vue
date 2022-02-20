<template>
  <q-page class="flex flex-center">
    <q-dialog v-model="store.state.prompt">
      <login-form />
    </q-dialog>
  </q-page>
</template>


<script>
import { inject } from "vue";
import LoginForm from "../components/LoginForm.vue";


export default {
  name: "Index",
  components: {
    LoginForm,
  },
  setup() {
    const store = inject('store');
    return {
      store
    }
  }
};
</script>
