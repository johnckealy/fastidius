import { reactive } from 'vue';

const state = reactive({
  % if auth:
  user: null,
  prompt: true
  % endif
})

const methods = {
  % if auth:
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
  % endif
}

export default {
  state,
  methods
}
