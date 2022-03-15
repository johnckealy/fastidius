<template>
  <div class="fullscreen text-center q-pa-md flex flex-center">
    <div>
      <div style="font-size: 10vh">
        404
      </div>

      <div class="text-h4" style="opacity:.4">
        Oops! Nothing here...
      </div>

      <q-btn
        class="q-mt-xl"
        color="blue"
        text-color="white"
        to="/"
        label="Back to Home"
        no-caps
      />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Error404'
})
</script>
