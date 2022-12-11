<script setup name="Gallery">
import { ref, reactive, computed, watch } from "vue";
import { useStore } from "src/stores/store";
import { api } from "src/boot/axios";
import LargePreview from "src/components/LargePreview.vue";
import UploadDialog from "src/components/UploadDialog.vue";
import {
  fasTags,
  fasBars,
  fasLock,
  fasLockOpen,
  fasRotate,
} from "@quasar/extras/fontawesome-v6";

const store = useStore();

const emit = defineEmits(["setTag"]);

const tags = ref([]);
const query = ref("");
const records = ref([]);
const isPreviewing = ref(false);
const previewItem = reactive({ tags: [], uuid: "", filename: "" });
const isRightDrawerOpen = ref(false);
const isTokenValid = ref(false);
const thumbnails = ref(null);

function toggleRightDrawer() {
  isRightDrawerOpen.value = !isRightDrawerOpen.value;
}

function preview(item) {
  isPreviewing.value = true;
  previewItem.filename = "raw/" + item.filename;
  previewItem.tags = item.tags;
  previewItem.uuid = item.uuid;
}

function resizeThumbnail(item) {
  let index = thumbnails.value.findIndex(
    (x) => x.$el.attributes.uuid.value == item.uuid
  );
  let img = thumbnails.value[index].$el.getElementsByTagName("img")[0];
  item.width = (img.naturalWidth * 256) / img.naturalHeight + "px";
}

async function checkToken() {
  await api
    .get("user/", {
      params: { token: store.token },
    })
    .then(() => (isTokenValid.value = true))
    .catch(() => (isTokenValid.value = false));
}

async function updateTags() {
  if (isTokenValid.value) {
    await api
      .get("tag/", {
        params: { token: store.token },
      })
      .then((response) => {
        tags.value = response.data;
      })
      .catch(() => {
        tags.value = [];
      });
    tags.value.sort((a, b) => b.count - a.count);
  } else {
    tags.value = [];
  }
}

async function updateMemes() {
  if (isTokenValid.value) {
    await api
      .get("meme/", {
        params: { token: store.token, tag: query.value },
      })
      .then((response) => {
        records.value = response.data;
      })
      .catch(() => {
        records.value = [];
      });
  } else {
    records.value = [];
  }
}

async function updateAll() {
  await checkToken();
  await updateTags();
  await updateMemes();
}

function setQuery(value) {
  query.value = value.tag;
}

watch(query, async (newQuery) => {
  await updateMemes();
});

store.$subscribe(async (mutation, state) => {
  await updateAll();
});
updateAll();
</script>

<template>
  <q-layout view="hHr LpR fFr">
    <q-header elevated>
      <q-toolbar class="bg-info">
        <q-toolbar-title>
          <q-input
            v-model="query"
            label="tags"
            clearable
            borderless
            debounce="200"
          >
            <template #prepend>
              <q-icon :name="fasTags" />
            </template>
          </q-input>
        </q-toolbar-title>
        <q-btn dense flat round :icon="fasRotate" @click="updateAll" />
        <q-btn dense flat round :icon="fasBars" @click="toggleRightDrawer" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page padding>
        <div
          class="full-width row wrap justify-start items-start content-center"
        >
          <q-chip
            v-for="item in tags"
            clickable
            outline
            @click="setQuery(item)"
          >
            <q-avatar v-if="item.count > 1">{{ item.count }}</q-avatar>
            {{ item.tag }}
          </q-chip>
        </div>
        <div
          class="full-width row wrap justify-around items-center content-center"
        >
          <q-img
            v-for="item in records"
            :width="item.width ? item.width : '256px'"
            :height="item.height ? item.height : '256px'"
            loading="lazy"
            :src="'thumbnail/' + item.thumbnail"
            fit="scale-down"
            @click="preview(item)"
            @load="resizeThumbnail(item)"
            :key="item.uuid"
            ref="thumbnails"
            :uuid="item.uuid"
          />
        </div>
      </q-page>

      <q-drawer
        v-model="isRightDrawerOpen"
        side="right"
        overlay
        behavior="mobile"
      >
        <q-card>
          <q-card-section>
            <q-input
              v-model="store.token"
              label="token"
              :error="!isTokenValid"
              debounce="200"
            >
              <template #prepend>
                <q-icon
                  :name="isTokenValid ? fasLockOpen : fasLock"
                  :color="isTokenValid ? '' : 'negative'"
                />
              </template>
            </q-input>
          </q-card-section>
        </q-card>
        <q-separator spaced="lg" />
        <UploadDialog :token="store.token" @success="updateAll" />
      </q-drawer>

      <q-dialog v-model="isPreviewing">
        <LargePreview
          :token="store.token"
          :tags="previewItem.tags"
          :filename="previewItem.filename"
          :uuid="previewItem.uuid"
          @hide="() => (isPreviewing = false)"
          @update="updateAll"
        >
        </LargePreview>
      </q-dialog>
    </q-page-container>
  </q-layout>
</template>
