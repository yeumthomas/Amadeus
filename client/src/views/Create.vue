<template>
    <div>
        <section class="">
            <div class="row mt-5">
                <div class="col-12 mt-2">
                    <card type="secondary" shadow
                                header-classes="bg-white pb-5"
                                body-classes="px-lg-5 py-lg-5"
                                class="border-0 m-5">
                            <template>
                                <div class="text-left text-muted mb-4">
                                    <h1 style="font-family: Helvetica Neue">Generate your Ensemble</h1>
                                </div>
                                    <form @submit.prevent="pressed" role="form">
                                        <div class="row align-items-start">
                                            <div class="col-md-6 p-0 m-0 pr-4">
                                                <div class="text-left">
                                                    <h6 style="font-family: Helvetica Neue">Step 1: Fill in Video Details</h6>
                                                </div>
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
                                            </div>
                                            <div class="col-md-6 p-0 m-0 pl-4">
                                                <div class="text-left">
                                                    <h6 style="font-family: Helvetica Neue">Step 2: Upload Recordings</h6>
                                                </div>


                                                <card>
                                                    <input  multiple
                                                            type="file"
                                                            ref="fileInputs"
                                                            accept="video/*"
                                                            class="d-none"
                                                            @change="onFilesPicked">
                                                    <base-button type="primary" 
                                                                @click="onPickFiles" 
                                                                class="my-1 mb-3"
                                                                icon="fa fa-folder-o">Search Directory
                                                    </base-button>
                                                </card>
                                            </div>
                                        </div>
                                        <div class="row align-items-start mt-3">
                                            <div class="col-md-12 p-0 m-0">
                                                <div class="text-left">
                                                    <h6 style="font-family: Helvetica Neue">Step 3: Check that All Recordings are Ready for Upload</h6>
                                                </div>
                                                <card>
                                                    <div class="row px-2">
                                                        <div class="col-4 m-0 p-0 overflowScrolll" id="content" v-for="video in project.videos" v-bind:key="video.title">
                                                            <card class="p-0 border-1"
                                                                body-classes="p-3">
                                                                <div class="row">
                                                                    <div class="col-10 pr-0">
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
                                                    </div>
                                                </card>
                                            </div>
                                        </div>
                                        <div class="row align-items-start mt-3">
                                            <div class="col-md-12 px-0">
                                                <div class="alert alert-danger m-0 x-0" role="alert" v-if="alert">
                                                    Please double-check all inputs before generating video - you will not be able to edit this submission!
                                                </div>
                                                <div class="text-center">
                                                    <base-button type="primary" v-on:click="pressed" class="my-4">Generate Virtual Ensemble</base-button>
                                                </div>
                                            </div>
                                        </div>
                                    </form>
                            </template>    
                        </card> 
                    </div>  
                </div>
        </section>
    </div>
</template>

<script>
import firebase from "firebase/app";
import "firebase/database";
import "firebase/storage"

export default {
    name: "home",
    data () {
        return {
            visible: true,
            project: {
                projectName: '',
                pieceTitle: '',
                composer: '',
                ensemble: '',
                final_url: '',
                videos: []
            },
            alert: false,
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
                // console.log("Uploaded: " + video.title)
            }
        },
        async pressed() {
            if (this.project.projectName != '' && this.project.pieceTitle != '' && this.project.composer != ''
                && this.project.ensemble != '' && this.project.videos.length != 0) {
                try {
                    this.$router.replace({name: 'loading'})
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
                                // console.log(url)
                            }).catch((error) => {
                                // console.log(error)
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
                    // console.log(err)
                }
            }
            else {
                this.alert = true
            }
        }
    }
};
</script>