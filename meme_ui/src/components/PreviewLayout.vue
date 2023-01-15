<script setup>
import { computed, onMounted, onUnmounted, ref, defineEmits } from "vue";
import { VueFlexWaterfall } from "vue-flex-waterfall";

const props = defineProps({
  margin: Number,
  width: Number,
  maxWidth: Number,
});

const emit = defineEmits(["updateMaxElementWidth"]);

const main = ref(null);

onMounted(() => {
  foobar();
  window.addEventListener("resize", foobar);
});

onUnmounted(() => {
  window.removeEventListener("resize", foobar);
});

function foobar() {
  let clientWidth = main.value.$el.clientWidth;
  let maxElementWidth = (clientWidth - props.margin * 2) / 2;
  emit("updateMaxElementWidth", maxElementWidth);
}

const break_at = computed(() => {
  let key = 3 * props.width + 4 * props.margin - 1;
  let n = 2;
  let ret = {};
  while (key <= props.maxWidth) {
    ret[key] = n;
    key += props.width + 2 * props.margin;
    n += 1;
  }
  return ret;
});
</script>

<template>
  <VueFlexWaterfall
    col="1"
    :break-at="break_at"
    :break-by-container="true"
    ref="main"
  >
    <slot></slot>
  </VueFlexWaterfall>
</template>
