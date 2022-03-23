<template>
  <q-layout view="lHh Lpr lFf">
    <q-toolbar class="bg-primary glossy text-white">
      <q-btn flat round dense icon="mdi-menu" class="q-mr-sm" />
      <q-toolbar-title>
        <q-btn to="/" flat dense>${ app_name }</q-btn>
      </q-toolbar-title>

      % if auth:
      <q-space />
      <div v-if="store.state.user">
        <q-btn no-caps flat dense>
          {{ store.methods.getDisplayName() }}
          <q-icon name="mdi-account" size="30px" />
          <q-menu transition-show="jump-down" transition-hide="jump-up">
            <q-list style="min-width: 100px">
              <q-item clickable>
                <q-item-section>Menu Item 1</q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>Menu Item 2</q-item-section>
              </q-item>
              <q-separator />
              <q-item @click="onClickLogout" clickable>
                <q-item-section>Logout</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </div>
      <div v-else>
        <q-btn @click="toggleLoginDialog" no-caps flat dense>
          <strong class="q-pa-sm">Login</strong>
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
import { onMounted, defineComponent, inject } from "vue";
% if auth:
import LoginForm from "../components/LoginForm.vue";
import { useRoute, useRouter } from "vue-router";
% endif

export default defineComponent({
  name: "MainLayout",
  components: {
    % if auth:
    LoginForm,
    % endif
  },
  setup() {
    const store = inject("store");
    % if auth:
    const api = inject("api");
    const route = useRoute();
    const router = useRouter();

    const toggleLoginDialog = () => {
      if (route.fullPath !== "/login") store.methods.toggleLoginDialog();
    };

    const onClickLogout = () => {
      store.methods.onLogout(api);
      router.push("/");
    };

    onMounted(() => {
      if (store.state.user || localStorage.authenticatedUser) store.methods.verifyUser(api);
    });
    % endif

    return {
      % if auth:
      toggleLoginDialog,
      onClickLogout,
      % endif
      store,
    };
  },
});
</script>
