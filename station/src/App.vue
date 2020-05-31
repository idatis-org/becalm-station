<template>
  <div id="app">
    <img alt="Vue logo" class="center" src="./assets/logo.png" />
    <HelloWorld msg="Welcome to Becalm v0.1" />
    <Sensor type="BMP280" endpoint="http://becalm02:8888/debug" />
    
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
import Sensor from "./components/Sensor.vue";

export default {
  name: "App",
  components: {
    HelloWorld,
    Sensor
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  acolor: #e0e0e0;
  abackground: #2c3e50;
  margin-top: 10px;
}
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 15%;
}
</style>
