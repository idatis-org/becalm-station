<template>
  <div class="hello">
    <h2>{{ msg }}</h2>
    <!-- p>
      Esto es Becalm Station, el software que corre en tu estación becalm.<br>
        <p>Para más información por favor dirígete
          <a href=https://github.com/sismotur/becalm3>aquí</a>
    </p -->
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.hello {
  text-align: center;
  padding: 10px 10px 10px 10px;
}
p {
 line-height: 15px
}
h3 {
  margin: 10px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
