import Vue from "vue";
import Router from "vue-router";

import AppHeader from "./layout/AppHeader";
import AppFooter from "./layout/AppFooter";
import DashboardHeader from "./layout/DashboardHeader";

import Components from "./views/Components.vue";
import Landing from "./views/Landing.vue";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Profile from "./views/Profile.vue";
import Dashboard from "./views/Dashboard.vue";
import Create from "./views/Create.vue";
import Loading from "./views/Loading.vue";
import NotFound from "./views/NotFound.vue";
import Reset from "./views/ResetPass.vue";

import firebase from "firebase/app"
import "firebase/auth"


Vue.use(Router);

const router = new Router({
  linkExactActiveClass: "active",
  mode: 'history',
  history: true,
  historyApiFallback: true,
  routes: [
    {
      path: '*',
      name: 'notfound',
      components: {
        header: AppHeader,
        default: NotFound,
        footer: AppFooter
      }
    },
    {
      path: "/dashboard",
      name: "dashboard",
      components: {
        header: DashboardHeader,
        default: Dashboard,
        footer: AppFooter
      },
      meta: {requiresAuth: true}
    },
    {
      path: "/landing",
      name: "landing",
      components: {
        header: AppHeader,
        default: Landing,
        footer: AppFooter
      }
    },
    {
      path: "/create",
      name: "create",
      components: {
        header: DashboardHeader,
        default: Create,
        footer: AppFooter
      }
    },
    {
      path: "/loading",
      name: "loading",
      components: {
        header: DashboardHeader,
        default: Loading,
        footer: AppFooter
      }
    },
    {
      path: "/login",
      name: "login",
      components: {
        header: AppHeader,
        default: Login,
        footer: AppFooter
      }
    },
    {
      path: "/",
      name: "login",
      components: {
        header: AppHeader,
        default: Login,
        footer: AppFooter
      }
    },
    {
      path: "/reset",
      name: "reset",
      components: {
        header: AppHeader,
        default: Reset,
        footer: AppFooter
      }
    },
    {
      path: "/register",
      name: "register",
      components: {
        header: AppHeader,
        default: Register,
        footer: AppFooter
      }
    },
    {
      path: "/profile",
      name: "profile",
      components: {
        header: AppHeader,
        default: Profile,
        footer: AppFooter
      }
    }
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  },
  
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = firebase.auth().currentUser;
  if (requiresAuth && !isAuthenticated){
    next('/login');
  }
  else {
    next()
  }
})

export default router;

