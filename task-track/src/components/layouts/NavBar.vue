<template>
  <div class="navbar-container">
    <div class="logo-container">
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M2 7C2 4.23858 4.23858 2 7 2H17C19.7614 2 22 4.23858 22 7V17C22 19.7614 19.7614 22 17 22H7C4.23858 22 2 19.7614 2 17V7ZM7 4C5.34315 4 4 5.34315 4 7V17C4 18.6569 5.34315 20 7 20H17C18.6569 20 20 18.6569 20 17V7C20 5.34315 18.6569 4 17 4H7Z"
          fill="white"
        />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M10.7148 7.19623C11.2978 6.2275 12.7022 6.2275 13.2852 7.19623L14.2841 8.85613L16.1715 9.29324C17.273 9.54835 17.707 10.8841 16.9658 11.7379L15.6958 13.2009L15.8633 15.1309C15.9611 16.2573 14.8249 17.0828 13.7838 16.6418L12 15.886L10.2162 16.6418C9.1751 17.0828 8.03888 16.2573 8.13663 15.1309L8.30414 13.2009L7.03417 11.7379C6.293 10.8841 6.727 9.54835 7.82847 9.29324L9.71582 8.85613L10.7148 7.19623ZM12 8.93936L11.3202 10.0689C11.1108 10.4169 10.7692 10.6651 10.3734 10.7568L9.08913 11.0542L9.95333 12.0498C10.2196 12.3565 10.3501 12.7581 10.315 13.1627L10.201 14.4761L11.4148 13.9619C11.7888 13.8034 12.2111 13.8034 12.5851 13.9619L13.799 14.4761L13.685 13.1627C13.6499 12.7581 13.7804 12.3565 14.0466 12.0498L14.9108 11.0542L13.6265 10.7568C13.2308 10.6651 12.8892 10.4169 12.6797 10.0689L12 8.93936Z"
          fill="white"
        />
      </svg>
      <router-link to="/" class="program-name">Tracky</router-link>
    </div>
    <div class="links-container">
      <router-link to="/">Projects</router-link>
      <router-link to="/auth" v-if="!employeeStore.isAuthenticated">
        Log in
      </router-link>
      <router-link to="/profile" v-else>Profile</router-link>
    </div>
  </div>
</template>

<script setup>
import { useStoreEmployee } from "@/stores/storeEmployee";

const employeeStore = useStoreEmployee();
</script>

<style scoped>
.navbar-container {
  width: 100%;
  height: 3.5rem;
  /* background: pink; */
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  z-index: 1;
}
.logo-container {
  display: flex;
  gap: 0.4rem;
  align-items: center;
  position: absolute;
  left: 1rem;
}
.navbar-container a {
  color: #fff;
  text-decoration: none;
}
.navbar-container a:focus {
  outline: none;
}
.program-name {
  font-weight: 600;
  font-size: 20px;
}
.links-container {
  display: flex;
  gap: 2rem;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-weight: 300;
}
</style>
