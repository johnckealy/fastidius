<template>
  <q-layout view="lHh Lpr lFf">
    <q-toolbar class="bg-primary glossy text-white">
      <q-btn flat round dense icon="menu" class="q-mr-sm" />
      <q-toolbar-title>Fastly</q-toolbar-title>

      <q-space />
      <div>
        <q-btn @click="store.methods.toggleLoginDialog()" no-caps flat dense>
          <strong class="q-pa-sm">{{  store.methods.getDisplayName() || "Login" }}</strong>
          <q-icon name="person" size="30px" />
        </q-btn>
      </div>
    </q-toolbar>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>


<script>
import { defineComponent, inject } from "vue";

export default defineComponent({
  name: "MainLayout",

  setup() {
    const store = inject("store");
    return {
      store,
    };
  },
});
</script>
