<template>
  <div id="app">
    <div id="banner">
      <p>Data Management Project</p>
    </div>
    <div id="body">
      <navigator/>
    </div>
  </div>
</template>

<script>
import navigator from './components/Navigator.vue'

export default {
  name: 'App',
  components: {
    navigator,
    // dataWindow,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

#banner {
  background-color: rgb(49,47,47);
  font-family: 'Courier New', Courier, monospace;
  font-size: xx-large;
  margin: 0;
  line-height: 2.5em;
}

#banner p{
  color:aliceblue;
  font: bolder;
  vertical-align: middle;
  text-align: left;
  margin-left: 1em;
}

#body {
  margin-left: 1em;
}

</style>
