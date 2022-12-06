<script setup>
import { useQuasar } from 'quasar';
import axios from 'axios';
import { debounce } from 'lodash-es';

const $q = useQuasar();
$q.dark.set(true);
</script>

<script>
export default {
  data() {
    return {
      token: '',
      tags: "",
      records: () => [],
      allTags: [],
      valid: false,
      isLoading: false,
      isPreviewing: false,
      previewUrl: "",
      previewTags: [],
      update: () => undefined,
    }
  },
  mounted() {
    this.client = axios.create({ timeout: 500, });
    this.update = debounce(this.doUpdate, 100, { trailing: true, });
    this.updateCookies = debounce(this.doUpdateCookies, 1000, { trailing: true, });
    this.token = this.$q.cookies.has('token') ? this.$q.cookies.get('token') : "";
    this.update();
  },
  methods: {
    doUpdate() {
      this.isLoading = true;
      this.client.get('meme/', { params: { token: this.token, tag: this.tags } })
        .then(res => {
          this.records = res.data;
          this.valid = true;
        })
        .catch(() => {
          this.records = [];
          this.valid = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
      this.client.get("tag/", { params: { token: this.token } })
        .then(res => this.allTags = res.data)
        .catch(() => this.allTags = []);
    },
    doUpdateCookies() {
      this.$q.cookies.set('token', this.token);
    },
    doPreview(item) {
      this.previewUrl = 'raw/' + item.filename;
      this.previewTags = item.tags;
      this.isPreviewing = true;
    },
  },
  watch: {
    token(newToken) {
      this.update();
      this.updateCookies();
    },
    tags(newToken) {
      this.update();
    },
  },
  computed: {
    tagList() {
      if (Array.isArray(this.tags)) {
        return this.tags;
      }
      else {
        return this.tags.split(',').map(x => x.trim()).filter(x => x != '');
      }
    },
    memeCount() {
      return this.records.length;
    },
  },
  meta() {
    console.log("wt");
    return {
      title: 'Meta Heap' + (this.valid ? (' - ' + this.token) : ''),
    }
  },
}
</script>

<template>
  <q-layout view="hHh lpR fff">
    <q-header elevated>
      <q-toolbar class="bg-info">
        <q-input v-model="token" label="token" debounce="200">
          <template #prepend>
            <q-icon name="fa-solid fa-lock" />
          </template>
        </q-input>
        <q-toolbar-title>
          <q-input v-model="tags" label="tags" clearable debounce="200">
            <template #prepend>
              <q-icon name="fa-solid fa-tags" />
            </template>
          </q-input>
        </q-toolbar-title>
        <q-btn round flat icon="fa-solid fa-upload"/>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page padding>
        <div class="full-width row wrap justify-start items-start content-center">
          <q-chip v-for="item in allTags" @click="() => this.tags = item.tag" clickable outline>
            <q-avatar v-if="(item.count > 1)">{{ item.count }}</q-avatar>
            {{ item.tag }}</q-chip>
        </div>
        <div class="full-width row wrap justify-start items-start content-start">
          <q-img v-for="item in records" :src="('thumbnail/' + item.thumbnail)" @click="doPreview(item)" fit="contain"
            loading="lazy" width="256px" ratio="1">
            <template #error>
              hmmm
            </template>
          </q-img>
        </div>
      </q-page>

      <q-page-sticky position="bottom-right" :offset="[18, 18]">
        <q-btn @click="update" outline flat rounded icon="fa-solid fa-rotate" class="secondary"></q-btn>
      </q-page-sticky>

      <q-dialog v-model="isPreviewing" auto-close full-height full-width class="shadow-10">
        <q-card>
          <q-bar>
            <div class="full-width row wrap justify-start items-start content-center">
              <q-chip v-for="item in previewTags" outline class="text-caption">
                {{ item }}
              </q-chip>
            </div>
          </q-bar>
          <q-card-section>
            <div class="absolute-full flex flex-center">
              <q-img :src="previewUrl" loading="lazy" fit="scale-down">
                <template #error>
                  wtf
                </template>
              </q-img>
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>
    </q-page-container>

  </q-layout>
</template>

<style scoped>

</style>
