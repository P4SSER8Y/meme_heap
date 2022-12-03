<script setup>
import Tags from './Tags.vue'
import { debounce } from 'lodash-es'
import axios from 'axios'
import Preview from './Preview.vue';
import { useCookies } from 'vue3-cookies';
import BigImg from './BigImg.vue';
</script>

<script>
export default {
  data() {
    return {
      token: 't0ken4tr0y',
      tags: "",
      records: () => [],
      allTags: [],
      update: null,
      updateCookies: null,
      largeVisible: false,
      largeUrl: "",
    }
  },
  mounted() {
    this.cookies = useCookies().cookies;
    this.client = axios.create({ timeout: 500, });
    this.update = debounce(this.doUpdate, 100, { trailing: true, });
    this.updateCookies = debounce(this.doUpdateCookies, 1000, { trailing: true, });
    this.token = this.cookies.isKey('token') ? this.cookies.get('token') : "";
    this.update();
  },
  methods: {
    doUpdate() {
      this.client.get('meme/', { params: { token: this.token, tag: this.tags } }).then(res => this.records = res.data);
      this.client.get("tag/", { params: { token: this.token } }).then(res => this.allTags = res.data.map(x => x.tag));
    },
    doUpdateCookies() {
      this.cookies.set('token', this.token);
    },
    doShowLargeImage(rawUrl) {
      this.largeUrl = rawUrl;
      this.largeVisible = true;
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
  }
}
</script>

<template>
  <input v-model="token" placeholder="token" />
  <input v-model="tags" placeholder="tags" />
  <button @click="update">Update</button>
  <div>
    <span>All Tags:</span>
    <Tags :tags="allTags" />
  </div>
  <div class="waterfall">
    <Preview class="drop" v-for="item in records" :filename="item.filename" :thumbnail="item.thumbnail" @click="doShowLargeImage('raw/' + item.filename)"/>
  </div>
  <BigImg :visible="largeVisible" :url="largeUrl" @hide="largeVisible = false" />
</template>

<style scoped>
.waterfall {
  column-width: 256px;
  column-count: auto;
  column-gap: 1rem;
  align-items: center;
}

.drop a img {
  align-items:center;
  width: 100%;
  height: auto;
  padding: 1px;
}
</style>
