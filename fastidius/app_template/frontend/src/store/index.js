import { reactive } from 'vue';

const state = reactive({
  % if auth:
  user: null,
  prompt: false
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
  async verifyUser(api) {
    try {
      const response = await api.get("/users/me");
      if (response.status_code == 200) {
        debugger
      }
    }
    catch {
      localStorage.isAuthenticated = false
    }
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
