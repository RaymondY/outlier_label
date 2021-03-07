import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import ECharts from 'vue-echarts'

// 全局注册组件（也可以使用局部注册）
Vue.component('v-chart', ECharts)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
