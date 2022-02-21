import { reactive } from 'vue';

const state = reactive({
  user: null,
  prompt: true
})

const methods = {
  toggleLoginDialog() {
    state.prompt = !state.prompt;
  },
  setUser(user) {
    state.user = user;
  },
  getDisplayName() {
    if (state.user) {
      return state.user.email
    }
  }
}

export default {
  state,
  methods
}
