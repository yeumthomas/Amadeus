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
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Project Name"
                                    addon-left-icon="ni ni-hat-3"
                                    v-model="project.projectName">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Piece Title"
                                    addon-left-icon="ni ni-email-83"
                                    v-model="project.pieceTitle">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Composer"
                                    addon-left-icon="ni ni-lock-circle-open"
                                    v-model="project.composer">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Ensemble Name"
                                    addon-left-icon="ni ni-lock-circle-open"
                                    v-model="project.ensemble">
                        </base-input>
                        <div class="text-center">
                            <base-button type="primary" v-on:click="pressed" class="my-4">Generate Virtual Ensemble</base-button>
                        </div>
                    </form>
                    <card>
                        <div class="mx-3 p-0" v-for="video in project.videos" v-bind:key="video.title">
                            <card class="p-2 border-1">
                                <div class="row">
                                    <div class="col-2">
                                        <video style="width: 25px" v-bind:src="video.url64" alt="video thumbnail"></video>
                                    </div>
                                    <div class="col-9">
                                    <h6>{{video.title}}</h6>
                                    </div>
                                    <div class="col-1">
                                        <base-button    type="primary" 
                                                        v-on:click="deleteVideo(video)" 
                                                        class="m-0 py-0 px-1">
                                            <i class="p-0 ni ni-fat-remove"></i>
                                        </base-button>
                                    </div>
                                </div>
                            </card>
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
                projectName: '',
                pieceTitle: '',
                composer: '',
                ensemble: '',
                videos: []
            }
        }
    },
    methods: {
        onPickFile() {
            this.$refs.fileInput.click()
        },
        deleteVideo(video) {

            const index = this.project.videos.indexOf(video);
            if (index > -1) {
                this.project.videos.splice(index, 1);
            }
            console.log(this.project.videos)
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
                    raw: null,
                    link: ''
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
                const projectPath = 'user/' + userID + '/' + this.project.projectName

                for (let i = 0; i < this.project.videos.length; i++) {
                    const videoPath = projectPath + '/uploads/' + this.project.videos[i].title
                    const videoRef = storageRef.child(videoPath)
                    let uploadTask = await videoRef.put(this.project.videos[i].raw, metaData)

                    // get video link
                    videoRef.getDownloadURL()
                        .then((url) => {
                            this.project.videos[i].link=url
                        }).catch((error) => {
                            console.log(error)
                        })
                    
                    // Don't need this anymore
                    delete this.project.videos[i].raw
                }

                // upload JSON with Project Info
                const jsonString = JSON.stringify(this.project)
                const blob = new Blob([jsonString], {type: "application/json"})

                const jsonPath = projectPath + "/projectInfo.json"
                storageRef.child(jsonPath).put(blob).then(function(snapshot) {
                });
                console.log(this.project)
    
            }
            catch (err) {
                console.log(err)
            }
        }
    }
};
</script>
