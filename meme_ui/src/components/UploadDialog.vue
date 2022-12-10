<script setup>
import { ref } from "vue";

const props = defineProps({
  token: String,
});

const emit = defineEmits(["success", "fail"]);

const tags = ref("");

function factory(files) {
  return {
    url: "meme/?token=" + props.token,
    method: "POST",
    formFields: [{ name: "tags", value: tags.value }],
    fieldName: "file",
  };
}

function success() {
  emit("success");
}

function fail() {
  emit("fail");
}
</script>

<template>
  <q-card>
    <q-card-section>
      <q-uploader
        flat
        accept="image/*"
        :label="'meme ' + token"
        bordered
        style="width: 100%; height: 100%; max-height: 100%"
        :factory="factory"
        @finish="success"
        @failed="fail"
      >
      </q-uploader>
    </q-card-section>
    <q-card-section>
      <q-input v-model="tags" label="tags"> </q-input>
    </q-card-section>
  </q-card>
</template>
