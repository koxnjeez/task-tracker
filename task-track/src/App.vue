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
import NavBar from "@/components/layouts/NavBar.vue";
</script>

<style>
body {
  background-color: #111;
  color: #fff;
  font-size: 18px;
  font-family: "Elms Sans", sans-serif;
  margin: 0;
}
@supports (display: grid) {
  html {
    height: 100%;
  }
  body {
    height: 100%;
    display: grid;
    grid-template-areas: "main";
    grid-template-rows: [main-start] 1fr [main-end];
  }
}
.container {
  margin: 3.5rem 2rem 0 2rem;
  grid-area: main;
  min-height: calc(100vh - 3.5rem);
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
.button {
  min-height: 3rem;
  min-width: 9rem;
  padding: 0;
  border-radius: 16px;
  border: none;
  font-family: inherit;
  font-size: 15px;
  font-weight: 900;
  background: rgba(255, 255, 255, 0.4);
  color: white;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
  backdrop-filter: blur(16px);
}
.button:hover {
  background: rgba(255, 255, 255, 0.32);
}
.button:active {
  background: rgba(255, 255, 255, 0.2);
}
.button-dark {
  background: rgba(255, 255, 255, 0.04);
}
.button-dark:hover {
  background: rgba(0, 0, 0, 0.05);
}
.button-dark:active {
  background: rgba(0, 0, 0, 0.2);
}
</style>
