import Vue from "vue";
import App from "./App.vue";
import store from "./store"; 
import CoreuiVueCharts from '@coreui/vue-chartjs'
Vue.use(CoreuiVueCharts)
Vue.config.productionTip = false;

new Vue({
  store,
  render: h => h(App)
}).$mount("#app");
