<template>
    <header class="header-global">
        <base-nav class="navbar-main" transparent type="" effect="light" expand>
            <router-link slot="brand" class="navbar-brand mr-lg-5" to="/">
                <img src="img/brand/white.png" alt="logo">
            </router-link>

            <div class="row" slot="content-header" slot-scope="{closeMenu}">
                <div class="col-6 collapse-brand">
                    <a href="https://demos.creative-tim.com/vue-argon-design-system/documentation/">
                        <img src="img/brand/blue.png">
                    </a>
                </div>
                <div class="col-6 collapse-close">
                    <close-button @click="closeMenu"></close-button>
                </div>
            </div>
            <ul class="navbar-nav align-items-lg-center ml-lg-auto">
                <li class="nav-item d-none d-lg-block ml-lg-4">
                    <base-button @click="signOut">
                        <span class="btn-inner--icon">
                            <i class="ni ni-circle-08 mr-2"></i>
                        </span>
                        <span v-if="loggedIn" class="nav-link-inner--text">Log Out</span>
                        <span v-else class="nav-link-inner--text">Log In</span>
                    </base-button>
                </li>
            </ul>
        </base-nav>
    </header>
</template>
<script>
import BaseNav from "@/components/BaseNav";
import BaseDropdown from "@/components/BaseDropdown";
import CloseButton from "@/components/CloseButton";
import firebase from "firebase/app";
import "firebase/auth";

export default {
    created() {
        firebase.auth().onAuthStateChanged(user=> {
                this.loggedIn = !! user;
            })
    },
    data () {
        return { 
            loggedIn: false
            }
    },
    methods: {
        async signOut() {
            try {
                const data = await firebase.auth().signOut();
                // console.log(data);
                this.$router.replace({name: 'login'})
            }
            catch (err) {
                // console.log(err)
            }
        }
    },
    components: {
        BaseNav,
        CloseButton,
        BaseDropdown
    }
};
</script>
<style>
</style>