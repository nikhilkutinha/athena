import Vue from 'vue'
import App from './App'
import router from './router'

import Buefy from 'buefy'
import HighchartsVue from 'highcharts-vue'

Vue.config.productionTip = false

// Additional libraries
Vue.use(Buefy)
Vue.use(HighchartsVue)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
