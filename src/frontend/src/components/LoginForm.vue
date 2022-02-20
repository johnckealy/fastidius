<template>
  <div class="" style="max-width: 700px">
    <q-card class="q-px-lg my-card">
      <q-card-section>
        <h5 class="q-mt-sm">Please Login</h5>
        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
          <q-input
            filled
            v-model="email"
            type="text"
            label="Email *"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
          />

          <q-input
            filled
            v-model="password"
            label="Password *"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
            ]"
          />

          <div>
            <q-btn label="Submit" type="submit" color="primary" />
            <q-btn
              label="Reset"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { useQuasar } from "quasar";
import { ref, inject } from "vue";

export default {
  setup() {
    const store = inject("store");
    const api = inject("api");

    const $q = useQuasar();
    const email = ref(null);
    const password = ref(null);

    const getUser = async () => {
      try {
        const response = await api.get("/users/me");
        store.methods.setUser(response.data)
      } catch {
        console.log("Error: Issue getting the current user");
      }
    };

    return {
      email,
      password,
      store,

      async onSubmit() {
        const formData = new FormData();
        formData.set("username", email.value);
        formData.set("password", password.value);
        try {
          await api.post("/auth/jwt/login", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });

          getUser();

          store.methods.toggleLoginDialog();
          $q.notify({
            color: "green-4",
            textColor: "white",
            icon: "cloud_done",
            message: "Submitted",
          });
        } catch (e) {
          $q.notify({
            color: "red-5",
            textColor: "white",
            icon: "warning",
            message: "Oops! Something went wrong logging you in",
          });
        }
      },

      onReset() {
        email.value = null;
        password.value = null;
      },
    };
  },
};
</script>
