<template>
    <header class="header-global fixed-top">
        <base-nav class="bg-default fixed-top" transparent type="" effect="light" expand>
            <router-link slot="brand" class="navbar-brand mr-lg-5" to="/">
                <img src="img/brand/white.png" alt="logo">
            </router-link>

            <!-- For Mobile View -->
            <div class="row" slot="content-header" slot-scope="{closeMenu}">
                <div class="col-6 collapse-brand">
                    <a href="https://www.google.com">
                        <img src="img/brand/blue.png">
                    </a>
                <div class="btn-wrapper mt-2 mb-2">
                </div>
                </div>
                <div class="col-6 collapse-close">
                    <close-button @click="closeMenu"></close-button>
                </div>
                
            </div>
            <div class="btn-wrapper mt-2 mb-2">
                <base-button tag="a"
                                href="/create"
                                class="mb-3 mb-sm-0 btn-neutral"
                                type="default"
                                icon="fa fa-plus">
                    Create Project
                </base-button>
            </div>
            <ul class="navbar-nav align-items-lg-center ml-lg-auto">
                
                <a slot="title" href="/dashboard" class="nav-link" data-toggle="dropdown" role="button">
                    <i class="ni ni-ui-04 d-lg-none"></i>
                    <span class="nav-link-inner--text">Dashboard</span>
                </a>
                <li class="nav-item d-none d-lg-block ml-lg-4">
                    <base-button @click="signOut" class="btn-neutral">
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
                console.log(data);
                this.$router.replace({name: 'login'})
            }
            catch (err) {
                console.log(err)
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