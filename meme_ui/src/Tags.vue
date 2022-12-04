<script setup>
import { NTag } from 'naive-ui';
</script>

<script>
export default {
    props: {
        tags: { type: Array, required: true },
    },
    methods: {
        clicked(tag) {
            this.$emit("tagClicked", tag);
        },
    }
}
</script>

<template>
    <n-tag class="tag" v-for="tag in tags" size="small" round :bordered="false" @click="clicked(tag)">{{ tag }}</n-tag>
</template>

<style scoped>
.tag {
    margin: auto 0.2rem;
    cursor: pointer;
}
</style>
