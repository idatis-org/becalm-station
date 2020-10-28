/*
# This file is part of becalm-station
# https://github.com/idatis-org/becalm-station
# Copyright: Copyright (C) 2020 Enrique Melero <enrique.melero@gmail.com>
# License:   Apache License Version 2.0, January 2004
#            The full text of the Apache License is available here
#            http://www.apache.org/licenses/
*/

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
