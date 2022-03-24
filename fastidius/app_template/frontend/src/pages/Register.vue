<template>
  <q-page class="flex flex-center">
    <div class="" style="max-width: 700px">
      <q-card class="q-px-lg my-card">
        <q-card-section>
          <h5 class="q-mt-sm">Register</h5>
          <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
            <q-input
              filled
              v-model="email"
              type="email"
              label="Email *"
              lazy-rules
              no-error-icon
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
            />

            <q-input
              filled
              no-error-icon
              type="password"
              v-model="password"
              label="Password *"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
            />

            <q-input
              filled
              no-error-icon
              type="password"
              v-model="password2"
              label="Re-Type Password *"
              lazy-rules
              :rules="[(val) => val === password || 'Passwords must match']"
            />

            <div>
              <q-btn label="Register" type="submit" color="primary" />
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
  </q-page>
</template>

<script>
import { useQuasar } from "quasar";
import { ref, inject } from "vue";
import { useRouter, useRoute } from "vue-router";

export default {
  setup() {
    const store = inject("store");
    const api = inject("api");
    const route = useRoute();
    const router = useRouter();

    const $q = useQuasar();
    const email = ref(null);
    const password = ref(null);
    const password2 = ref(null);

    return {
      email,
      password,
      password2,
      store,

      async onSubmit() {
        const formData = {
          email: email.value,
          password: password.value,
        };
        try {
          await api.post("/auth/register", formData);
          router.push({ path: "/registered-successfully" });

          $q.notify({
            color: "green-4",
            textColor: "white",
            icon: "mdi-check-circle",
            message: "Submitted",
          });
        } catch (e) {
          $q.notify({
            color: "red-5",
            textColor: "white",
            icon: "mdi-alert",
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
