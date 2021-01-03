<template>
    <div>
            <!-- shape Hero -->
        <section class="section-hero section-shaped my-0">
            <div class="shape shape-style-1 shape-primary">
            </div>
            <SideNav/>
            <card type="secondary" shadow
                          header-classes="bg-white pb-5"
                          body-classes="px-lg-5 py-lg-5"
                          class="border-0">
                <template>
                    <div class="text-center text-muted mb-4">
                        <h5>Create a Project</h5>
                    </div>
                    <form @submit.prevent="pressed" role="form">

                        <input type="file"
                                ref="fileInput"
                                accept="video/*"
                                class="d-none"
                                @change="onFilePicked">

                        <base-button type="primary" @click="onPickFile" class="my-4">Upload Video</base-button>
                        <!-- <video :src="videoURL64" style="max-width=150px"></video> -->
                        <!-- <base-input alternative
                                    class="mb-3"
                                    placeholder="Project Name"
                                    addon-left-icon="ni ni-hat-3"
                                    v-model="projectName">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Piece Title"
                                    addon-left-icon="ni ni-email-83"
                                    v-model="pieceTitle">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Composer"
                                    addon-left-icon="ni ni-lock-circle-open"
                                    v-model="composer">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Ensemble Name"
                                    addon-left-icon="ni ni-lock-circle-open"
                                    v-model="ensemble">
                        </base-input> -->
                        <div class="text-center">
                            <base-button type="primary" v-on:click="pressed" class="my-4">Create account</base-button>
                        </div>
                    </form>
                    <card>
                        <div style="width: 80px" v-for="video in project.videos" v-bind:key="video.title">
                            <img v-bind:src="video.url64" alt="video thumbnail">
                            <span>{{video.title}}</span>
                        </div>
                    </card>
                </template>
            </card>
        </section>
        <section class="section section-lg">
            <div class="container">
                <div class="row row-grid align-items-center">
                    <div class="col-md-6 order-md-2">
                        <img src="img/theme/promo-1.png" class="img-fluid floating">
                    </div>
                    <div class="col-md-6 order-md-1">
                        <div class="pr-md-5">
                            <icon name="ni ni-settings-gear-65" class="mb-5" size="lg" type="success" shadow
                                  rounded></icon>
                            <h3>Awesome features</h3>
                            <p>The kit comes with three pre-built pages to help you get started faster. You can change
                                the text and images and you're good to go.</p>
                            <ul class="list-unstyled mt-5">
                                <li class="py-2">
                                    <div class="d-flex align-items-center">
                                        <badge type="success" circle class="mr-3" icon="ni ni-settings-gear-65"></badge>
                                        <h6 class="mb-0">Carefully crafted components</h6>
                                    </div>
                                </li>
                                <li class="py-2">
                                    <div class="d-flex align-items-center">
                                        <badge type="success" circle class="mr-3" icon="ni ni-html5"></badge>
                                        <h6 class="mb-0">Amazing page examples</h6>
                                    </div>
                                </li>
                                <li class="py-2">
                                    <div class="d-flex align-items-center">
                                        <badge type="success" circle class="mr-3" icon="ni ni-satisfied"></badge>
                                        <h6 class="mb-0">Super friendly support team</h6>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import SideNav from "../layout/SideNav";
import firebase from "firebase/app";

export default {
    name: "home",
    components: {
        SideNav
    },
    data () {
        return {
            visible: true,
            project: {
                // projectName: '',
                // pieceTitle: '',
                // composer: '',
                // ensemble: '',
                videos: []
            }
        }
    },
    methods: {
        onPickFile() {
            this.$refs.fileInput.click()
        },
        onFilePicked(event) {
            
            const files = event.target.files
            const videoName = files[0].name
            let lastIndex = videoName.lastIndexOf('.')
            if ( lastIndex <= 0) {
                return alert('Please add a valid file')
            }

            // create singular video object
            const video = {
                    title: videoName,
                    url64: '',
                    raw: null
            }

            const fileReader = new FileReader()
            fileReader.addEventListener('load', () => {
                video.url64 = fileReader.result
            })
            fileReader.readAsDataURL(files[0])

            // add video object to list of videos
            video.raw = files[0]
            this.project.videos.push(video)
        },
        async pressed() {
            try {
                // handle video upload
                const metaData = {
                    contentType: '.mp4'
                }
                const userID = firebase.auth().currentUser.uid
                const storageRef = firebase.storage().ref()

                for (let i = 0; i < this.project.videos.length; i++) {
                    const filePath = 'user/' + userID + '/uploads/' + this.project.videos[i].title
                    const videoRef = storageRef.child(filePath)
                    let uploadTask = await videoRef.put(this.project.videos[i].raw, metaData)
                }
    
                // // get video link
                // videoRef.getDownloadURL()
                //     .then((url) => {
                //         video.url=url
                //     }).catch((error) => {
                //         console.log(error)
                //     })
            }
            catch (err) {
                console.log(err)
            }
        }
    }
};
</script>
