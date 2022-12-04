<script setup>
</script>

<script>
export default {
    props: {
        tags: { type: Array, required: true },
    }
}
</script>

<template>
    <span class="tag" v-for="tag in tags">{{ tag }}</span>
</template>

<style scoped>
.tag {
    color: #a33;
    display: inline-block;
    white-space: nowrap;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    text-decoration: none;
    text-align: center;
}
</style>
