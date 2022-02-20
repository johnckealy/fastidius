import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)

// const api = axios.create({
//   baseURL: process.env.VUE_APP_API || 'http://localhost:8000/'
// })
const api = axios.create({
  baseURL:  'http://localhost:8000/',
  withCredentials: true
})



export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
  app.provide('api', app.config.globalProperties.$api)
})

export { api }
