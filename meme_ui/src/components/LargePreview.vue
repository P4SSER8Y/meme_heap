<script setup name="Preview">
import { ref } from "vue";
import { api } from "src/boot/axios";

const props = defineProps({
  token: String,
  tags: Array,
  filename: String,
  uuid: String,
});

const emit = defineEmits(["hide", "update"]);

const isConfirming = ref(false);

function toggleDeleteConfirm() {
  isConfirming.value = !isConfirming.value;
}

async function deleteMe() {
  await api.delete("meme/", {
    params: {
      uuid: props.uuid,
      token: props.token,
    },
  });
  emit("hide");
  emit("update");
}
</script>

<template>
  <q-card>
    <q-bar>
      <div class="full-width row wrap justify-start items-start content-center">
        <q-chip v-for="item in props.tags" outline class="text-caption">
          {{ item }}
        </q-chip>
      </div>
      <q-space />
      <q-btn
        dense
        flat
        icon="fa-solid fa-trash-can"
        @click="toggleDeleteConfirm"
      />
    </q-bar>
    <q-card-section @click="$emit('hide')">
      <div
        class="full-width column wrap justify-start items-start content-center"
      >
        <q-space />
        <div class="full-width row justify-around items-center content-around">
          <img :src="props.filename" />
        </div>
        <q-space />
      </div>
      <!-- <div class="full-height flex flex-center">
          <q-img :src="props.filename" loading="lazy" fit="scale-down"> </q-img>
        </div> -->
    </q-card-section>
    <q-dialog v-model="isConfirming">
      <q-card>
        <q-card-section class="text-h6 text-weight-bolder">
          <q-avatar
            icon="fa-solid fa-biohazard"
            text-color="primary"
            size="xl"
          />
          <span class="text-primary text-uppercase text-weight-bolder text-h6">Delete this?</span>
        </q-card-section>
        <q-separator />
        <q-card-actions align="right">
          <q-btn outline label="no" class="text-positive text-weight-bold" v-close-popup />
          <q-btn outline label="YES" class="text-negative text-weight-bold" v-close-popup @click="deleteMe" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-card>
</template>
