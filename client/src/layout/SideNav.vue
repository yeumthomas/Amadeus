<template>  
    <div>
        <b-sidebar v-model=visible id="sidebar-1" title="" width="320px" shadow>
            <div class="navbar px-3 py-2">
                <h1>AMAEDUS</h1>
                <div class="btn-wrapper mt-2 mb-2">
                    <base-button tag="a"
                                    href="/create"
                                    class="mb-3 mb-sm-0"
                                    type="default"
                                    icon="fa fa-plus">
                        Create Project
                    </base-button>
                </div>
                <div class="col">
                        <div class="d-flex mx-0 align-items-left">
                            <i class="fa fa-home"></i>
                            <a href="/dashboard"><h6 class="mb-0"> Home</h6></a>
                        </div>
                        <div class="d-flex mx-0 align-items-left">
                            <i class="fa fa-envelope"></i>
                            <a href="/"><h6 class="mb-0"> Contact</h6></a>
                        </div>
                </div>
            </div>
        </b-sidebar>
    </div>
</template>
<script>
export default {
    data () {
        return {
            visible: true
        }
    }
};
</script>