import { createApp } from 'vue'
import App from './App.vue'
import VueLazyload from 'vue-lazyload'

const app = createApp(App)

app.mount('#app')
app.use(VueLazyload)
