<script setup>
import { computed } from "vue";
import { VueFlexWaterfall } from "vue-flex-waterfall";

const props = defineProps({
  spacing: Number,
  width: Number,
  maxWidth: Number,
});

const break_at = computed(() => {
  let key = 2 * props.width + 2 * props.spacing - 1;
  let n = 1;
  let ret = {};
  while (key <= props.maxWidth) {
    ret[key] = n;
    key += props.width + 2 * props.spacing;
    n += 1;
  }
  console.log(ret);
  return ret;
});
</script>

<template>
  <VueFlexWaterfall col="1" :break-at="break_at" :break-by-container="true">
    <slot></slot>
  </VueFlexWaterfall>
</template>
