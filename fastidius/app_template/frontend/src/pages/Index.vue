<template>
  <q-page class="flex flex-center">
    <h4>Welcome to ${ app_name } 🚀</h4>
    % if auth:
    <router-link to="/dashboard">Dashboard</router-link>
    % endif
  </q-page>
</template>


<script>

export default {
  name: "Index",
};
</script>
