import { createApp } from 'vue'
import { Quasar, Cookies, Meta } from 'quasar'
import quasarLang from 'quasar/lang/zh-CN'
import quasarIconSet from 'quasar/icon-set/material-icons-round'

// Import icon libraries
import '@quasar/extras/material-icons-round/material-icons-round.css'

// A few examples for animations from Animate.css:
// import @quasar/extras/animate/fadeIn.css
// import @quasar/extras/animate/fadeOut.css

// Import icon libraries
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

// Assumes your root component is App.vue
// and placed in same folder as main.js
import App from './App.vue'

const app = createApp(App)

app.use(Quasar, {
  plugins: { Cookies, Meta }, // import Quasar plugins and add here
  lang: quasarLang,
  iconSet: quasarIconSet,
})

// Assumes you have a <div id="app"></div> in your index.html
app.mount('#app')
