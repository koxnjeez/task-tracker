<template>
  <div class="background">
    <div class="background-box"></div>
  </div>

  <nav-bar></nav-bar>

  <div class="container">
    <router-view></router-view>
  </div>
</template>

<script setup>
import NavBar from "./components/layouts/NavBar.vue";
</script>

<style>
body {
  background-color: #111;
  color: #fff;
  font-size: 18px;
  font-family: "Elms Sans", sans-serif;
  margin: 0;
}
.background {
  height: 100%;
  width: 100%;
  z-index: -2;
  position: fixed;
  left: 0;
  top: 0;
  background: url("images/background_gradient.jpg") center / cover no-repeat
    border-box;
}
.background-box {
  height: 100%;
  width: 100%;
  z-index: -1;
  position: fixed;
  left: 0;
  top: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(5px);
}
@supports (display: grid) {
  html {
    height: 100%;
  }
  body {
    width: 100%;
    display: grid;
    grid-template-rows: [main-start] 1fr [main-end];
    grid-template-areas: "main";
  }
}
.container {
  grid-area: "main";
}
</style>
