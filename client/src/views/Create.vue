<template>
    <div>
            <!-- shape Hero -->
        <section class="section-hero section-shaped">
            <div class="shape shape-style-1 shape-white">
            </div>
            <!-- <SideNav/> -->
            <card type="secondary" shadow
                          header-classes="bg-white pb-5"
                          body-classes="px-lg-5 py-lg-5"
                          class="border-0 m-5">
                <template>
                    <div class="text-center text-muted mb-4">
                        <h5>Create a Project</h5>
                    </div>
                    <form @submit.prevent="pressed" role="form">

                        <input  multiple
                                type="file"
                                ref="fileInputs"
                                accept="video/*"
                                class="d-none"
                                @change="onFilesPicked">

                        <base-button type="primary" 
                                    @click="onPickFiles" 
                                    class="my-4"
                                    icon="fa fa-video-camera">Upload Videos
                        </base-button>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Project Name"
                                    addon-left-icon="fa fa-film"
                                    v-model="project.projectName">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Piece Title"
                                    addon-left-icon="fa fa-music"
                                    v-model="project.pieceTitle">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Composer"
                                    addon-left-icon="fa fa-user"
                                    v-model="project.composer">
                        </base-input>
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="Ensemble Name"
                                    addon-left-icon="fa fa-cubes"
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
        onPickFiles() {
            this.$refs.fileInputs.click()
        },
        deleteVideo(video) {

            const index = this.project.videos.indexOf(video);
            if (index > -1) {
                this.project.videos.splice(index, 1);
            }
            console.log(this.project.videos)
        },
        onFilesPicked(event) {

            const files = event.target.files

            for (let i = 0; i < files.length; i++) {
                const videoName = files[i].name
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

                // const fileReader = new FileReader()
                // fileReader.addEventListener('load', () => {
                //     video.url64 = fileReader.result
                // })

                // fileReader.readAsDataURL(files[i])

                // add video object to list of videos
                video.raw = files[i]
                this.project.videos.push(video)
                console.log("Uploaded: " + video.title)
            }
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
                    await videoRef.getDownloadURL()
                        .then((url) => {
                            this.project.videos[i].link = url
                            console.log(url)
                        }).catch((error) => {
                            console.log(error)
                        })

                    // Don't need raw anymore
                    delete this.project.videos[i].raw
                }

                // // upload JSON with Project Info
                // const jsonString = JSON.stringify(this.project)
                // const blob = new Blob([jsonString], {type: "application/json"})

                // const jsonPath = projectPath + "/projectInfo.json"
                // storageRef.child(jsonPath).put(blob).then(function(snapshot) {
                // });
                // console.log(this.project)


                // Update project JSON to database
                const db = firebase.database().ref(projectPath)
                db.set(this.project)
            }
            catch (err) {
                console.log(err)
            }
        }
    }
};
</script>
