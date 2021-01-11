<template>
    <section class="section-shaped section-lg my-0">
        <div class="shape shape-style-1 shape-primary">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
        </div>
        <div class="container pt-lg-md" style="margin-bottom: 10rem !important;">
            <div class="row justify-content-center">
                <div class="col-lg-5">
                    <card type="secondary" shadow
                          header-classes="bg-white pb-5"
                          body-classes="px-lg-5 py-lg-5"
                          class="border-0">
                        <template>
                            <div class="text-center text-muted mb-4">
                                <h6>Welcome Back to Amadeus</h6>
                            </div>
                            <form role="form">
                                <base-input alternative
                                            class="mb-3"
                                            placeholder="Email"
                                            addon-left-icon="ni ni-email-83"
                                            v-model="email">
                                </base-input>
                                <base-input alternative
                                            type="password"
                                            placeholder="Password"
                                            addon-left-icon="ni ni-lock-circle-open"
                                            v-model="password"
                                            @keyup.enter.native="signIn()">
                                </base-input>
                                <div class="alert alert-danger m-0 p-2 text-center" role="alert" v-if="alert">
                                    Incorrect Email or Password
                                </div>
                                <div class="text-center">
                                    <base-button type="primary" v-on:click=signIn() class="my-4">Sign In</base-button>
                                </div>
                                <div class="error" v-if="error">{{error.message}}</div>
                            </form>
                        </template>
                    </card>
                    <div class="row mt-3">
                        <div class="col-6">
                            <a href="/" class="text-white text-light">
                                <small>Forgot password?</small>
                            </a>
                        </div>
                        <div class="col-6 text-right">
                            <a href="/register" class="text-white text-light">
                                <small>Create new account</small>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
<script>
import firebase from "firebase/app";
import "firebase/auth";

export default {
    data() {
        return{ 
            email: '',
            password: '',
            error: '',
            alert: false
        }
    },
    methods: {
        async signIn() {
            try {
                const val = await firebase.auth().signInWithEmailAndPassword(this.email, this.password)
                this.$router.replace({name: 'dashboard'})
                await this.email.destroy()
                await this.password.destroy()
            }
            catch (err) {
                // console.log(err)
                this.alert = true
            }
        }
    }
};
</script>
<style>
</style>
