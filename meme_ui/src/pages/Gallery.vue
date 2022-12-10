<script setup name="Gallery">
import { ref, reactive, computed, watch } from "vue";
import { storeToRefs } from "pinia";
import { useStore } from "src/stores/store";
import { api } from "src/boot/axios";
import LargePreview from "src/components/LargePreview.vue";
import TokenEdit from "src/components/TokenEdit.vue";
import UploadDialog from "src/components/UploadDialog.vue";

const store = useStore();

const emit = defineEmits(["setTag"]);

const tags = ref([]);
const query = ref("");
const records = ref([]);
const isPreviewing = ref(false);
const previewItem = reactive({ tags: [], uuid: "", filename: "" });
const isRightDrawerOpen = ref(false);

const allTags = computed(() => {
  if (Array.isArray(tags.value)) {
    return tags.value;
  } else {
    return tags.value
      .split(",")
      .map((x) => x.trim())
      .filter((x) => x != "");
  }
});

function toggleRightDrawer() {
  isRightDrawerOpen.value = !isRightDrawerOpen.value;
}

function toggleUploadDialog() {
  isUploading.value = !isUploading.value;
}

function preview(item) {
  isPreviewing.value = true;
  previewItem.filename = "raw/" + item.filename;
  previewItem.tags = item.tags;
  previewItem.uuid = item.uuid;
}

async function updateTags() {
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
}

async function updateMemes() {
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
}

async function updateAll() {
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
              <q-icon name="fa-solid fa-tags" />
            </template>
          </q-input>
        </q-toolbar-title>
        <q-btn dense flat round icon="fa-solid fa-rotate" @click="updateAll" />
        <q-btn
          dense
          flat
          round
          icon="fa-solid fa-bars"
          @click="toggleRightDrawer"
        />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page padding>
        <div
          class="full-width row wrap justify-start items-start content-center"
        >
          <q-chip
            v-for="item in allTags"
            clickable
            outline
            @click="setQuery(item)"
          >
            <q-avatar v-if="item.count > 1">{{ item.count }}</q-avatar>
            {{ item.tag }}
          </q-chip>
        </div>
        <div class="full-width row wrap justify-between items-center">
          <q-card v-for="item in records" bordered>
            <q-card-section horizontal>
              <img
                :src="'thumbnail/' + item.thumbnail"
                style="height: 256px; width: auto; cursor: pointer"
                @click="preview(item)"
              />
            </q-card-section>
          </q-card>
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
            <TokenEdit v-model="store.token" label="tags">
              <template #prepend>
                <q-icon name="fa-solid fa-tags" />
              </template>
            </TokenEdit>
          </q-card-section>
        </q-card>
        <q-separator spaced="lg"/>
        <UploadDialog :token="store.token" @success="updateAll"/>
      </q-drawer>

      <q-dialog v-model="isPreviewing" full-width full-height>
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
