<script setup>
import {useQuasar} from 'quasar';
import { useStore } from './stores/store';

const $q = useQuasar();

$q.dark.set(true);

const store = useStore();
store.token = $q.cookies.has('token') ? $q.cookies.get('token') : "";

store.$subscribe((mutation, state) => {
    $q.cookies.set('token', store.token);
})
</script>

<template>
  <router-view />
</template>
