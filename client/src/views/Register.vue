<template>
    <section class="section section-shaped section-lg my-0">
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
        <div v-if="error" class="error">{{error.message}}</div>


        <div class="container pt-lg-md " style="margin-bottom: 10rem !important;">
            <div class="row justify-content-center">
                <div class="col-lg-5">
                    <card type="secondary" shadow
                          header-classes="bg-white pb-5"
                          body-classes="px-lg-5 py-lg-5"
                          class="border-0">
                        <template>
                            <div class="text-center text-muted mb-4">
                                <h5>Welcome to Amadeus</h5>
                            </div>
                            <form @submit.prevent="pressed" role="form">
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
                                            v-model="password">
                                </base-input>
                                <base-input alternative
                                            placeholder="Access Code"
                                            addon-left-icon="fa fa-pencil"
                                            v-model="code">
                                </base-input>
                                <div class="alert alert-danger m-0 p-2 text-center" role="alert" v-if="alert">
                                    Incorrect Access Code
                                </div>
                                <div class="text-center">
                                    <base-button type="primary" v-on:click="pressed" class="my-4">Create account</base-button>
                                </div>
                            </form>
                        </template>
                    </card>
                    <div class="row mt-2">
                        <div class="col-6"></div>
                        <div class="col-6 text-right">
                            <a href="/login" class="text-white text-light">
                                <small>Already have an account?</small>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
<script>
import firebase from "firebase/app"
import "firebase/auth"
export default {
    data () {
        return {
            code: "",
            email: "",
            password: "",
            error: "",
            alert: false
        }
    },
    methods: {
        async pressed() {
            try {
                if (this.code == "beethoven") {
                    const user = await firebase.auth().createUserWithEmailAndPassword(this.email, this.password)
                    this.$router.replace({name: "dashboard"});
                }
                else {
                    this.alert = true
                }
            }
            catch (err) {
                console.log(err)
                this.alert = true
            }
        }
    }
};
</script>
<style>
</style>
