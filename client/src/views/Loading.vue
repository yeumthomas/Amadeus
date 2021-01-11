<template>
    <div>
        <section class="section-hero section-shaped mt-0">
            <!-- <div class="shape shape-style-1 shape-primary"> -->
                <div style="width:50rem; margin:0 auto;" class="row mt-5">
                    <div class="col-12 mt-2 align-items-center">
                        <card type="secondary" shadow
                                    header-classes="bg-white pb-5"
                                    body-classes="px-lg-5 py-lg-5"
                                    class="border-0 m-5">
                            <icon name="fa fa-check" class="ml-3 align-items-center align-self-start bg-primary" size="lg" type="white" shadow
                                  rounded></icon>
                            <span class="display-4 text-primary" style="font-family: Helvetica Neue">  Successfully Submitted Recordings</span>
                            <hr/>
                            <h6 class="text-default" style="font-family: Helvetica Neue">Your Virtual Ensemble will be Complete in 24-48 Hours!</h6>
                            <p class="text-default pt-2">Please keep a eye out for an email that will notify you that the 
                                virtual ensemble video is complete!</p>
                            <div class="row justify-items-right">
                                <div class="col-4">
                                    <base-button type="primary" v-on:click="routeHome" class="my-4">
                                        Return to Dashboard</base-button>

                                </div>  
                            </div>
                        </card> 
                    </div>
                </div>
            <!-- </div> -->
        </section>
    </div>
</template>

<script>

export default {
    name: "home",
    data () {
        return {
        }
    },
    methods: {
        routeHome() {
            this.$router.replace({name: 'dashboard'})

        }
    }
};
</script>
