<script setup>
import { ref } from "vue";
import { fasPenToSquare } from "@quasar/extras/fontawesome-v6";
import { useQuasar } from "quasar";

const $q = useQuasar();

const props = defineProps({
  token: String,
});

const emit = defineEmits(["success", "fail"]);

const tags = ref("");
const uploader = ref(null);

function factory(files) {
  return {
    url: "meme/?token=" + props.token,
    method: "POST",
    formFields: [{ name: "tags", value: tags.value }],
    fieldName: "file",
  };
}

function success(info) {
  emit("success");
  let res = JSON.parse(info.xhr.response);
  $q.notify({
    progress: true,
    timeout: 3000,
    message: "Uploaded: " + res.uuid,
    caption: 'tags: ' + res.tags.join(', '),
    color: 'positive',
  });
  setTimeout(() => {
    uploader.value.reset();
    tags.value = "";
  }, 250);
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
        label="Upload"
        color="dark"
        style="width: 100%; height: 100%; max-height: 100%"
        max-files="1"
        :factory="factory"
        ref="uploader"
        @uploaded="success"
        @failed="fail"
      >
      </q-uploader>
    </q-card-section>
    <q-card-section>
      <q-input v-model="tags" label="tags" hint="use comma to separate tags">
        <template #prepend>
          <q-icon :name="fasPenToSquare" />
        </template>
      </q-input>
    </q-card-section>
  </q-card>
</template>
