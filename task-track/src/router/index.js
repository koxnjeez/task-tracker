import { createRouter, createWebHashHistory } from "vue-router";
import ViewProjects from "@/view/ViewProjects.vue";
import ViewProfile from "@/view/ViewProfile.vue";
import ViewAuth from "@/view/ViewAuth.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "projects",
      component: ViewProjects,
    },
    {
      path: "/profile",
      name: "profile",
      component: ViewProfile,
    },
    {
      path: "/auth",
      name: "authorization",
      component: ViewAuth,
    },
  ],
});

export default router;
