<script setup>
import { defineProps, defineEmits, ref, computed } from "vue";

const props = defineProps({
  data: Object,
  width: Number,
});
const emit = defineEmits(["click"]);
const main = ref(null);

let width = ref(256);
let height = ref(256);

function clicked() {
  emit("click");
}

function resizeThumbnail() {
  let img = main.value.$el.getElementsByTagName("img")[0];
  width.value = (img.naturalWidth > 256) ? Image.naturalWidth : 256;
  height.value = img.naturalHeight / img.naturalWidth * width.value;
}

const computedWidth = computed(() => {
  return width.value > props.width ? props.width : width.value;
});

const computedHeight = computed(() => {
  return (height.value / width.value) * computedWidth.value;
});
</script>

<template>
  <q-img
    :width="computedWidth + 'px'"
    :height="computedHeight + 'px'"
    loading="lazy"
    :src="data.thumbnail"
    fit="cover"
    @click="clicked"
    @load="resizeThumbnail"
    ref="main"
    style="margin: 5px"
  />
</template>
