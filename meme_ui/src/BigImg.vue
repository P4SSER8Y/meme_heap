<script>
export default {
    props: {
        url: { type: String, default: "" },
        visible: { type: Boolean, default: false },
    },
    methods: {
        hide() {
            this.$emit("hide");
        }
    }
}
</script>

<template>
    <div v-show="visible" @click="hide" class="frame">
        <img class="img" :src="url" alt="nani?" />
    </div>
</template>

<style scoped>
.frame {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: black;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
}

.frame .img {
    display: block;
    max-width: 100%;
    max-height: 100%;
    text-align: center;
}
</style>
