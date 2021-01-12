<template>
    <div>
            <!-- shape Hero -->
    <section class="section-shaped section-lg my-0">
        <div class="shape shape-style-1 shape-white h-100">
        </div>
        <div class="mx-5 mt-5 h-100">
            <div class="row mb-5" >
                <div class="col-4">
                    <h1 style="font-family: Helvetica Neue">My Projects</h1>
                </div>
            </div>
            <div class='row d-flex align-items-stretch'>
                <div class="col-md-4 align-self-stretch" v-for="project in projects" :key=project.projectName>
                    <card class="h-100"
                        type="secondary" 
                        shadow>
                        <div class='row d-flex px-3'>
                            <div class='col'>
                                <div v-if="project.final_url.length == 0" class="align-items-left alert alert-warning m-0 p-2 text-center" role="alert">
                                    Status: Editing in progress...
                                </div>
                                <div v-else class="align-items-left alert alert-success m-0 p-2 text-center" role="alert">
                                    Status: Video ready for download!
                                </div>
                                <h4 class='pt-3'><b>{{project.projectName}}</b></h4>
                                <h6 class="pb-2">__</h6>
                                <h6 class="mb-0">Piece: {{project.pieceTitle}}</h6>
                                <h6 class="mb-0">Composer: <i>{{project.composer}}</i></h6>
                                <h6 class="mb-0">Performed By: {{project.ensemble}}</h6>
                            </div>
                        </div>
                        <div class='row'>
                            <div class='col d-flex' v-if="project.final_url.length == 0">
                                <div class='row d-flex'>
                                    <div class="col align-items-left align-self-end" >
                                        <base-button type="primary" 
                                            class="mt-5 mb-3"
                                            icon="fa fa-download"
                                            disabled>Video Download
                                        </base-button>
                                    </div>
                                </div>
                            </div>
                            <div class='col d-flex' v-else>
                                <div class='row d-flex'>
                                    <div class="col align-items-left align-self-end">
                                        <base-button tag="a"
                                            type="primary" 
                                            class="mt-5 mb-3"
                                            icon="fa fa-download"
                                            :href="project.final_url"
                                            >Video Download
                                        </base-button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </card>
                </div>
                <div class="col-md-4 d-flex">
                    <card class="d-flex w-100"
                        style="padding: 5.5rem 0;"
                        type="secondary" 
                        shadow>
                        <div class="py-5 row align-items-center d-flex h-100">
                            <div class='col text-center align-self-center'>
                                <base-button tag="a"
                                    type="primary" 
                                    class="my-3"
                                    icon="fa fa-plus"
                                    href="/create"
                                    >New Project
                                </base-button>
                            </div>
                        </div>
                    </card>
                </div>
            </div>
        </div>
    </section>
    </div>
</template>

<script>
import firebase from 'firebase/app'
import "firebase/database";

export default {
    name: "home",
    data () {
    return {
        projects: {},
        }
    },
    mounted() {
        let database = firebase.database()
        let currEmail = firebase.auth().currentUser.email.split('.').join(','); // also replaces all dots
        let ref = database.ref('user/' + currEmail).once('value')
            .then((snapshot) => {
                // console.log(snapshot.val())
                this.projects = snapshot.val()
            })
    }
}
</script>
