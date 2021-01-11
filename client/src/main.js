import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import Argon from "./plugins/argon-kit";
import './registerServiceWorker';

import axios from 'axios';
// import firebase from 'firebase';
import firebase from 'firebase/app';
import 'firebase/auth'

const firebaseConfig = {
  apiKey: process.env.VUE_APP_API_KEY,
  authDomain: process.env.VUE_APP_AUTH_DOMAIN,
  projectId: process.env.VUE_APP_PROJECT_ID,
  storageBucket: process.env.VUE_APP_STORAGE_BUCKET,
  messagingSenderId: process.env.VUE_APP_MESSAGING_SENDER_ID,
  appId: process.env.VUE_APP_APP_ID,
  measurementId: process.env.VUE_APP_MEASUREMENT_ID
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// firebase.analytics(); does not work for node
Vue.prototype.$axios = axios
Vue.config.productionTip = false;
Vue.use(Argon);
let app;

firebase.auth().onAuthStateChanged(user => {
  if(!app){
    new Vue({
      router,
      render: h => h(App)
    }).$mount("#app");
  }
})

