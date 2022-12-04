<script setup>
import Tags from './Tags.vue'
import { debounce } from 'lodash-es'
import axios from 'axios'
import Preview from './Preview.vue';
import { useCookies } from 'vue3-cookies';
import { NInput, NIcon, NConfigProvider, darkTheme, NGlobalStyle, NButton, NDivider, NEmpty, NResult, NScrollbar, NLayout, NLayoutHeader, NLayoutContent, NLayoutFooter } from 'naive-ui';
import { Password16Filled, Tag16Filled, ArrowSyncCircle16Filled } from '@vicons/fluent';
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
        .finally(() => this.isLoading = false);
      this.client.get("tag/", { params: { token: this.token } })
        .then(res => this.allTags = res.data.map(x => x.tag))
        .catch(() => this.allTags = []);
    },
    doUpdateCookies() {
      this.cookies.set('token', this.token);
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
  }
}
</script>

<template>
  <n-config-provider :theme="darkTheme">
    <n-global-style />
    <div style="position: relative">
      <n-layout :position="absolute" :native-scroller="false">
        <n-layout-header bordered class="headline" :position="absolute">
          <n-input v-model:value="token" placeholder="token" :status="isLoading ? 'warning' : (valid ? 'success' : 'error'
          )" autosize size="small" style="min-width: 10em">
            <template #prefix>
              <n-icon :component="Password16Filled" />
            </template>
          </n-input>
          <n-input v-model:value="tags" placeholder="tags, separated by &quot;,&quot;" size="small" clearable>
            <template #prefix>
              <n-icon :component="Tag16Filled" />
            </template>
          </n-input>
          <n-button @click="update" tertiary size="small" :type="valid ? 'success' : 'error'">
            <template #icon>
              <n-icon :component="ArrowSyncCircle16Filled" />
            </template>
          </n-button>
        </n-layout-header>

        <n-layout :position="absolute" :native-scrollbar="true">
          <Tags :tags="allTags" @tagClicked="(tag) => tags = tag" />
          <div v-if="valid && (memeCount > 0)" class="waterfall">
            <Preview class="waterdrop" v-for="item in records" :filename="item.filename" :thumbnail="item.thumbnail" />
          </div>
          <n-result v-else status="404" size="huge"></n-result>
        </n-layout>
      </n-layout>
    </div>
  </n-config-provider>
</template>
<style scoped>
.waterfall {
  align-self: center;
  column-width: 256px;
  column-count: auto;
  column-gap: 1rem;
  align-items: center;
}

.waterdrop>* {
  align-items: center;
  width: 100%;
  height: auto;
  padding: 1px;
}

.headline {
  width: 100%;
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-around;
  align-items: stretch;
  gap: 0.5rem;
}
</style>
