import { createRouter, createWebHistory } from "vue-router";
import { useStoreEmployee } from "@/stores/storeEmployee";
import { useStoreProjects } from "@/stores/storeProjects";
import ViewProjects from "@/view/ViewProjects.vue";
import ViewProfile from "@/view/ViewProfile.vue";
import ViewAuth from "@/view/ViewAuth.vue";
import ViewProject from "@/view/ViewProject.vue";
import ViewNotFound from "@/view/ViewNotFound.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/projects",
    },
    {
      path: "/projects",
      name: "projects",
      component: ViewProjects,
    },
    {
      path: "/projects/:id",
      name: "project",
      component: ViewProject,
    },
    {
      path: "/profile",
      name: "profile",
      component: ViewProfile,
    },
    {
      path: "/auth",
      name: "auth",
      component: ViewAuth,
    },
    {
      path: "/:notFound(.*)",
      component: ViewNotFound,
    },
  ],
  linkActiveClass: "active",
});

router.beforeEach(async (to, from) => {
  const employeeStore = useStoreEmployee();
  const projectsStore = useStoreProjects();

  if (employeeStore.token && !employeeStore.user) {
    try {
      await employeeStore.fetchCurrentUser();
    } catch (error) {
      employeeStore.logout();
      return "/auth";
    }
  }

  if (to.name === "auth" && employeeStore.isAuthenticated) {
    return "/profile";
  } else if (to.name === "profile" && !employeeStore.isAuthenticated) {
    return "/auth";
  }
  return true;
});

export default router;
