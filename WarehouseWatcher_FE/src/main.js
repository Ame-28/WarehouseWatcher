// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Vuetify
// https://vuetifyjs.com/en/getting-started/installation/#existing-projects
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue'
import router from './router'

const app = createApp(App)

const vuetify = createVuetify({
    components,
    directives,
})

app.use(createPinia())
app.use(router)
app.use(vuetify, {
    iconfont: 'mdi'
  })  

app.mount('#app')
