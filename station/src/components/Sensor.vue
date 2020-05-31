<template>
<div>
  <div class="sensor"  >
    Sensor type:{{ type }} Status:{{ status }} 
    <img src="./assets/playpause.jpeg" width=20px v-on:click="paused ^= 1; updateStatus();"/>
      <p/>
       <div class="meassure" v-for="item in sensordata" :key="item.measure">
            <div v-on:click="track(item.measure)">{{item.measure}}: {{ item.value }} </div>
      </div>
  </div>
  <CChartLine
    v-bind:datasets="cdata"    
    v-bind:options="coptions"
    
  />
</div>
</template>

<script>
const refreshPeriod = 100;
import axios from "axios";
export default {
  name: "Sensor",
  props: {
    type: String,
    endpoint: String
  },
  data: () => {
    return { 
      status: "",
      sensordata: {} ,
      chartlen: 250,
      trackmeasure: "Presión",
      paused: 0,
      yWide: 0.01,

      cdata: [
        { data:[], 
          label: '' ,
          fill: true,    
          pointRadius: 0,
          tension: 0,
          cubicInterpolationMode: 'middle', 
          backgroundColor: "#FFA0A0",
          
        },
      ],
      coptions: {
        steppedLine: true  ,
        maintainAspectRatio: true,
        responsive: true,
        borderJoinStyle: "round",
        legend: {
            labels: {
                // This more specific font property overrides the global property
                fontColor: 'black'
            }
        }
        ,
        scales: {
            yAxes: [{
              ticks: {
                    suggestedMin: 0,
                    suggestedMax: 0,
                    beginAtZero: false,
                    fontSize: 16,
                },
              display: true,
              drawTicks: false,
                
            }], 
            xAxes: [{
              display: false,
              drawTicks: false,
            }]
        }
      }
    };
  },
  mounted() {    
    this.track(this.trackmeasure)
    this.updateStatus();

  },
  methods: {
    updateStatus: function() {
      axios
        .get(this.endpoint)
        .then(res => {
          var measures=[];
          for (var measure in res.data) {
            //console.log(measure) ;
            //console.log(res.data[measure]) ;
            measures.push( { 'measure': measure, 'value' : res.data[measure]} )
            if (measure == this.trackmeasure ) { 
              
              // IF this is a reset or every 100 points
              if (this.cdata[0].data.length % 100 == 0 ) {                 
                this.coptions.scales.yAxes[0].ticks.suggestedMin= (1-this.yWide) * res.data[measure] ;
                this.coptions.scales.yAxes[0].ticks.suggestedMax= (1+this.yWide) * res.data[measure] ;
                console.log("Reset Scale") ;
              }                           
              
              // Display only this.chartLen measues
              if (this.cdata[0].data.length > this.chartlen ) {                 
                this.cdata[0].data.shift() 
                } 
              this.cdata[0].data.push(res.data[measure]) ;                            
            }
          }
          this.sensordata = measures ;
          this.status = "OK " + ( (this.paused == 1) ? "Paused" : "" );
          
        })
        .catch(error => (this.status = error));      
      if (this.paused != 1 ) {
        setTimeout(() => this.updateStatus(), refreshPeriod);
      }
    },

    track: function(measure) {
      console.log("Now tracking " + measure);
      this.trackmeasure=measure;
      this.cdata[0].label=measure ;
      this.cdata[0].data=[];
    }
  }
};

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 0 10px;
}
a {
  color: #42b983;
}
.sensor {
  acolor: #e0e0e0;
  abackground: #2c3e50;
}
.meassure{
  font-size: 18px;
  float:left;
  padding: 5px 5px 5px 5px;
}
img {
  vertical-align: text-bottom;
}
</style>
