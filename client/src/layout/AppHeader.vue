<template>
    <header class="header-global">
        <base-nav class="navbar-main" transparent type="" effect="light" expand>
            <a class="navbar-brand mr-lg-5" href="https://amadeus.video">
                <img src="../../public/logo-white.png" alt="logo">
            </a>

            <div class="row" slot="content-header" slot-scope="{closeMenu}">
                <div class="col-6 collapse-brand">
                    <a href="https://amadeus.video">
                        <img src="../../public/logo-blue.png">
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
                        <span v-if="loggedIn" class="nav-link-inner--text">Sign Out</span>
                        <span v-else class="nav-link-inner--text">Sign In</span>
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