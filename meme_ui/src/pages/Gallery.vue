<script setup name="Gallery">
import { ref, reactive, computed, watch, onMounted } from "vue";
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
  fasQuestion,
} from "@quasar/extras/fontawesome-v6";
import { useRoute, useRouter } from "vue-router";

const $router = useRouter();
const $route = useRoute();
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
const updateStackCount = ref(0);
let thumbnailWidth = new Map();
let thumbnailHeight = new Map();

$router.afterEach(async () => {
  if ($route.params.t) {
    store.token = $route.params.t;
  }
  await updateAll();
});

onMounted(async () => {
  await updateAll();
});

function toggleRightDrawer() {
  isRightDrawerOpen.value = !isRightDrawerOpen.value;
}

function preview(item) {
  isPreviewing.value = true;
  previewItem.filename = item.filename;
  previewItem.tags = item.tags;
  previewItem.uuid = item.uuid;
}

function getThumbnailWidth(uuid) {
  if (!thumbnailWidth.has(uuid)) {
    thumbnailWidth.set(uuid, ref("256px"));
  }
  return thumbnailWidth.get(uuid);
}

function getThumbnailHeight(uuid) {
  if (!thumbnailHeight.has(uuid)) {
    thumbnailHeight.set(uuid, ref("256px"));
  }
  return thumbnailHeight.get(uuid);
}

const computedThumbnailWidth = computed(
  () => (uuid) => getThumbnailWidth(uuid).value
);

const computedThumbnailHeight = computed(
  () => (uuid) => getThumbnailHeight(uuid).value
);

function resizeThumbnail(item) {
  let index = thumbnails.value.findIndex(
    (x) => x.$el.attributes.uuid.value == item.uuid
  );
  let img = thumbnails.value[index].$el.getElementsByTagName("img")[0];
  let width = (img.naturalWidth * 256) / img.naturalHeight;
  let height = 256;

  getThumbnailWidth(item.uuid).value = width + "px";
  getThumbnailHeight(item.uuid).value = height + "px";
}

async function checkToken() {
  updateStackCount.value++;
  await api
    .get("user/", {
      params: { token: store.token },
    })
    .then(() => (isTokenValid.value = true))
    .catch(() => (isTokenValid.value = false))
    .finally(() => updateStackCount.value--);
}

async function updateTags() {
  if (isTokenValid.value) {
    updateStackCount.value++;
    await api
      .get("tag/", {
        params: { token: store.token },
      })
      .then((response) => {
        tags.value = response.data;
      })
      .catch(() => {
        tags.value = [];
      })
      .finally(() => updateStackCount.value--);
    tags.value.sort((a, b) => b.count - a.count);
  } else {
    tags.value = [];
  }
}

function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

async function updateMemes() {
  if (isTokenValid.value) {
    updateStackCount.value++;
    await api
      .get("meme/", {
        params: { token: store.token, tag: query.value },
      })
      .then((response) => {
        records.value = shuffleArray(response.data);
      })
      .catch(() => {
        records.value = [];
      })
      .finally(() => updateStackCount.value--);
  } else {
    records.value = [];
  }
}

async function updateAll() {
  updateStackCount.value++;
  await checkToken();
  await updateTags();
  await updateMemes();
  updateStackCount.value--;
}

function setQuery(value) {
  query.value = value.tag;
}

function submitToken(event) {
  $router.push({ path: "/" + store.token });
}

watch(query, async (newQuery) => {
  await updateMemes();
});

store.$subscribe(async (mutation, state) => {
  await updateAll();
});

function removeTag(arg) {
  let index = records.value.findIndex((x) => x.uuid == arg.uuid);
  if (index < 0) {
    return;
  }
  records.value[index].tags = records.value[index].tags.filter(
    (x) => x != arg.tag
  );
  if (isPreviewing) {
    preview(records.value[index]);
  }

  index = tags.value.findIndex((x) => x.tag == arg.tag);
  if (index < 0) {
    return;
  }
  tags.value[index].count--;
  tags.value.sort((a, b) => b.count - a.count);
  while (tags.value.at(tags.value.length - 1).count <= 0) {
    tags.value.pop();
  }
}

function addTag(arg) {
  let index = records.value.findIndex((x) => x.uuid == arg.uuid);
  if (index < 0) {
    return;
  }
  records.value[index].tags.push(arg.tag);
  if (isPreviewing) {
    preview(records.value[index]);
  }

  console.log(tags);
  index = tags.value.findIndex((x) => x.tag == arg.tag);
  console.log(index);
  if (index >= 0) {
    tags.value[index].count++;
  } else {
    tags.value.push({ tag: arg.tag, count: 1 });
  }
  tags.value.sort((a, b) => b.count - a.count);
}
</script>

<template>
  <q-layout view="hHr LpR fFr">
    <q-header elevated>
      <q-toolbar class="bg-info">
        <q-avatar v-if="isTokenValid">{{ records.length }}</q-avatar>
        <q-avatar v-else :icon="fasQuestion"></q-avatar>
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
        <q-btn
          dense
          flat
          round
          :icon="fasRotate"
          @click="updateAll"
          :class="{ rotating: updateStackCount > 0 }"
        >
          <q-tooltip> sync </q-tooltip>
        </q-btn>
        <q-btn dense flat round :icon="fasBars" @click="toggleRightDrawer">
          <q-tooltip> more </q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page padding>
        <div
          class="full-width row wrap justify-start items-start content-center"
        >
          <span v-for="item in tags">
            <q-chip
              v-if="item.count > 1"
              clickable
              outline
              @click="setQuery(item)"
            >
              <q-avatar>{{ item.count }}</q-avatar>
              {{ item.tag }}
            </q-chip>
          </span>
        </div>
        <div
          class="full-width row wrap justify-around items-center content-center"
        >
          <transition-group
            appear
            enter-active-class="animated fadeInUp"
            leave-active-class="animated fadeOutDown"
          >
            <q-img
              v-for="item in records"
              :width="computedThumbnailWidth(item.uuid)"
              :height="computedThumbnailHeight(item.uuid)"
              loading="lazy"
              :src="item.thumbnail"
              fit="scale-down"
              @click="preview(item)"
              @load="resizeThumbnail(item)"
              :key="item.uuid"
              ref="thumbnails"
              :uuid="item.uuid"
            />
          </transition-group>
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
            <q-form @submit="submitToken">
              <q-input
                label="token"
                v-model="store.token"
                :error="!isTokenValid"
                debounce="200"
                clearable
              >
                <template #prepend>
                  <q-icon
                    :name="isTokenValid ? fasLockOpen : fasLock"
                    :color="isTokenValid ? '' : 'negative'"
                  />
                </template>
              </q-input>
            </q-form>
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
          @removeTag="removeTag"
          @addTag="addTag"
        >
        </LargePreview>
      </q-dialog>
    </q-page-container>
  </q-layout>
</template>

<style scoped>
.rotating {
  animation: wtf 1s linear 0.1s infinite;
}

@keyframes wtf {
  100% {
    transform: rotate(360deg);
  }
}
</style>
