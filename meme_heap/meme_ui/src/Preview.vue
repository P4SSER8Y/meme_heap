<script setup>
import Tags from "./Tags.vue"
</script>

<script>
export default {
    props: {
        filename: { type: String, required: true },
        thumbnail: { type: String, required: false, default: "" },
        tags: () => [],
    },
    computed: {
        rawPath() {
            return "raw/" + this.filename;
        },
        thumbnailPath() {
            return "thumbnail/" + this.thumbnail;
        },
    }
}
</script>

<template>
    <div>
        <img class="thumbnail" v-lazy="thumbnailPath" :v-key="thumbnailPath" />
    </div>
</template>

<style scoped>
.thumbnail {
    width: 100%;
    height: auto;
}
</style>
