import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import ECharts from 'vue-echarts'
import axios from 'axios'

// 全局注册组件（也可以使用局部注册）
Vue.component('v-chart', ECharts)

Vue.config.productionTip = false
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

new Vue({
  render: h => h(App),
}).$mount('#app')