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
.centering {
  position: absolute;
  left: 50%;
  top: calc(50% - (1.75rem));
  translate: -50% -50%;
}
.button {
  min-height: 3rem;
  min-width: 9rem;
  padding: 0 1rem;
  border-radius: 16px;
  border: none;
  font-family: inherit;
  font-size: 15px;
  font-weight: 900;
  background: rgba(255, 255, 255, 0.4);
  color: white;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
  backdrop-filter: blur(16px);
  outline: none;
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
.modal-background {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100vh;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
}
dialog {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: none;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
}
.switch {
  position: relative;
  display: inline-block;
  height: 1.8rem;
  width: 3.6rem;
  outline: none;
  border: none;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 34px;
  transition: 0.3s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 1.3rem;
  width: 1.3rem;
  left: 0.25rem;
  bottom: 0.25rem;
  background: rgba(255, 255, 255, 0.6);
  transition: 0.3s;
  border-radius: 50%;
}
input:checked + .slider {
  background: rgba(255, 95, 30, 0.6);
}
input:checked + .slider:before {
  transform: translateX(1.8rem);
}
[type="text"] {
  height: 1.8rem;
  outline: none;
  border: none;
  padding-left: 0.5rem;
  background: rgba(255, 255, 255, 0.4);
  box-shadow: 0 4px 8px rgba(27, 27, 27, 0.3);
  color: black;
  backdrop-filter: blur(16px);
  font-family: inherit;
  font-size: 16px;
  font-weight: 500;
  border-radius: 5px;
}
</style>
