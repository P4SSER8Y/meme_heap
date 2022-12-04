<script setup>
import Tags from "./Tags.vue"
import { NImage, NEmpty } from "naive-ui";
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
    <n-image :src="thumbnailPath" lazy object-fit="cover" :preview-src="rawPath" :show-toolbar="false" width="256">
        <n-empty />
    </n-image>
</template>

<style scoped>

</style>
