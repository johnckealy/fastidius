<template>
  <q-layout view="lHh Lpr lFf">
    <q-toolbar class="bg-primary glossy text-white">
      <q-btn flat round dense icon="mdi-menu" class="q-mr-sm" />
      <q-toolbar-title>${ app_name }</q-toolbar-title>

      % if auth:
      <q-space />
      <div>
        <q-btn @click="store.methods.toggleLoginDialog()" no-caps flat dense>
          <strong class="q-pa-sm">{{  store.methods.getDisplayName() || "Login" }}</strong>
          <q-icon name="mdi-account" size="30px" />
        </q-btn>
      </div>
      % endif
    </q-toolbar>
      % if auth:
    <q-dialog v-model="store.state.prompt">
      <login-form />
    </q-dialog>
    % endif 

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>


<script>
import { defineComponent, inject } from "vue";
import LoginForm from "../components/LoginForm.vue";

export default defineComponent({
  name: "MainLayout",
  components: {
    % if auth:
    LoginForm,
    % endif
  },
  setup() {
    const store = inject('store');
    return {
      store
    }
  }
});
</script>
