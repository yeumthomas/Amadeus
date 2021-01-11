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
                                <h6>Forgot your Password?</h6>
                                <p>We'll send a password reset link to the email below</p>
                            </div>
                            <form role="form">
                                <base-input alternative
                                            class="mb-3"
                                            placeholder="Email"
                                            addon-left-icon="ni ni-email-83"
                                            v-model="email"
                                            @keyup.enter.native="sendEmail()">
                                </base-input>
                                <div class="alert alert-success m-0 p-2 text-center" role="success" v-if="success">
                                    Sent reset email!
                                </div>
                                <div class="alert alert-danger m-0 p-2 text-center" role="fail" v-if="fail">
                                    Account does not exist with this email.
                                </div>
                                <div class="text-center" v-if="show">
                                    <base-button type="primary" v-on:click='sendEmail()' class="my-4">Send Email</base-button>
                                </div>
                            </form>
                        </template>
                    </card>
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
            fail: false,
            success: false,
            show: true
        }
    },
    methods: {
        async sendEmail() {
            try{
                this.success = false
                this.fail = false
                await firebase.auth().sendPasswordResetEmail(this.email)
                this.success = true
                this.show = false
            }
            catch(err) {
                this.fail = true

            }
        }
    }
};
</script>
<style>
</style>
