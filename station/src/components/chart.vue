/*
# This file is part of becalm-station
# https://github.com/idatis-org/becalm-station
# Copyright: Copyright (C) 2020 Enrique Melero <enrique.melero@gmail.com>
# License:   Apache License Version 2.0, January 2004
#            The full text of the Apache License is available here
#            http://www.apache.org/licenses/
*/
<template>
  <CChartBar
    style="height:300px"
    :datasets="[
      {
        data: [10, 22, 34, 46, 58, 70, 46, 23, 45, 78, 34, 12],
        backgroundColor: '#E55353',
        label: 'Sales',
      }
    ]"
    labels="months"
    :options="{ maintainAspectRatio: false,  duration: 1}"
  />

</template>

<script>

export default {
  //glData: store.$state,
  name: "Chart",
  props: ["title", "measureid", "width", "height"],
  data: function() {
    return {
      chartData: {
        chartType: "vLineChart",
        title: this.title,
        width: this.width,
        height: this.height,
        dim: "time",
        metric: "measure"
      }
    };
  },
  computed: {
    becalmData() {
      let gData = [];
      for (let timeStamp in this.$store.state.dbBecalm[this.measureid]) {
        let measure = this.$store.state.dbBecalm[this.measureid][timeStamp];
        if (measure > 0) gData.push({ acc: timeStamp, balance: measure });
      }
      return { data: gData };
      //return this.$store.getters.moneyData;
    }
  }
};
</script>

<style>
.graph {
  display: inline-block;
  *display: inline;
  margin-left: 20px;
  vertical-align: bottom;
}
</style>
