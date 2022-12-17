<script setup name="Preview">
import { ref, reactive } from "vue";
import { api } from "src/boot/axios";
import {
  fasTrashCan,
  fasImage,
  fasBiohazard,
  fasPlus,
} from "@quasar/extras/fontawesome-v6";
import { useQuasar } from "quasar";

const $q = useQuasar();

const props = defineProps({
  token: String,
  tags: Array,
  filename: String,
  uuid: String,
});

const emit = defineEmits(["hide", "update", "removeTag", "addTag"]);

const isConfirming = ref(false);
const img = ref(null);
const naturalInfo = reactive({
  valid: false,
  width: 0,
  height: 0,
});
const addingTag = ref("");

function toggleDeleteConfirm() {
  isConfirming.value = !isConfirming.value;
}

function updateSize(src) {
  try {
    let element = img.value.$el.getElementsByTagName("img")[0];
    naturalInfo.width = element.naturalWidth;
    naturalInfo.height = element.naturalHeight;
    naturalInfo.valid = true;
  } catch (e) {
    naturalInfo.valid = false;
  }
}

async function deleteMe() {
  let res = (
    await api.delete("meme/", {
      params: {
        uuid: props.uuid,
        token: props.token,
      },
    })
  ).data;
  $q.notify({
    progress: true,
    timeout: 3000,
    message: "Deleted: " + res.uuid,
    color: "negative",
  });
  emit("hide");
  emit("update");
}

async function addTag(value, initValue) {
  console.log(value);
  let res = (
    await api.put("tag/", {
      tag: value,
      uuid: props.uuid,
      token: props.token,
    })
  ).data;
  $q.notify({
    progress: true,
    timeout: 1000,
    message: "Added tag: " + value,
  });
  emit("addTag", { tag: value, uuid: props.uuid });
  addingTag.value = "";
}

function cleanAddingTag() {
  addingTag.value = "";
}

async function deleteTag(tag) {
  let res = (
    await api.delete("tag/", {
      params: {
        tag: tag,
        uuid: props.uuid,
        token: props.token,
      },
    })
  ).data;
  $q.notify({
    progress: true,
    timeout: 1000,
    message: "Deleted tag: " + tag,
  });
  emit("removeTag", { tag: tag, uuid: props.uuid });
}
</script>

<template>
  <q-card class="no-scroll" style="width: 100vw; height: auto">
    <q-bar>
      <q-icon :name="fasImage" />
      <div v-show="naturalInfo.valid">
        {{ naturalInfo.width }} x {{ naturalInfo.height }}
      </div>
      <q-space />
      <q-btn dense flat :icon="fasTrashCan" @click="toggleDeleteConfirm" />
    </q-bar>
    <q-card-section @click="$emit('hide')">
      <div
        class="full-width column wrap justify-start items-start content-center"
      >
        <q-img
          :src="props.filename"
          loading="lazy"
          fit="scale-down"
          draggable
          @load="updateSize"
          ref="img"
        />
      </div>
    </q-card-section>
    <q-card-section>
      <div
        class="full-width row wrap justify-start items-start content-center text-caption"
      >
        <q-chip
          v-for="item in props.tags"
          outline
          clickable
          @click="deleteTag(item)"
        >
          {{ item }}
          <q-tooltip>remote</q-tooltip>
        </q-chip>

        <q-chip outline clickable>
          <q-icon :name="fasPlus"></q-icon>
          {{ addingTag }}
          <q-tooltip>add</q-tooltip>
          <q-popup-edit
            v-model="addingTag"
            v-slot="scope"
            persistent
            @save="addTag"
            @before-hide="cleanAddingTag"
          >
            <q-input
              v-model="scope.value"
              dense
              autofocus
              @keyup.enter.prevent="scope.set"
              @keyup.escape.prevent="scope.cancel"
            />
          </q-popup-edit>
        </q-chip>
      </div>
    </q-card-section>
    <q-dialog v-model="isConfirming">
      <q-card>
        <q-card-section class="text-h6 text-weight-bolder">
          <q-avatar :icon="fasBiohazard" text-color="primary" size="xl" />
          <span class="text-primary text-uppercase text-weight-bolder text-h6"
            >Delete this?</span
          >
        </q-card-section>
        <q-separator />
        <q-card-actions align="right">
          <q-btn
            outline
            label="no"
            class="text-positive text-weight-bold"
            v-close-popup
          />
          <q-btn
            outline
            label="YES"
            class="text-negative text-weight-bold"
            v-close-popup
            @click="deleteMe"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-card>
</template>
