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
    localStorage.authenticatedUser = JSON.stringify(user)
  },
  async verifyUser(api) {
    try {
      const response = await api.get("/users/me");
      if (response.status == 200) {
        state.user = response.data;
        localStorage.authenticatedUser = JSON.stringify(state.user)
      }
    }
    catch {
      localStorage.authenticatedUser = null
    }
  },
  getDisplayName() {
    if (state.user) {
      return state.user.email
    }
  },
  async onLogout(api) {
    await api.post("/auth/jwt/logout");
    localStorage.authenticatedUser = null
    state.user = null
  }
  % endif
}

export default {
  state,
  methods
}
