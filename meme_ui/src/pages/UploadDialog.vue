<script setup>
import { api } from 'src/boot/axios';
</script>

<script>
export default {
    props: ['token'],
    data() {
        return {
            value: false,
            tags: '',
        }
    },
    methods: {
        factory(files) {
            return {
                url: 'meme/?token=' + this.token,
                method: 'POST',
                formFields: [{ name: 'tags', value: this.tags }],
                fieldName: 'file',
            }
        }
    }
}
</script>

<template>
    <q-dialog v-model="value">
        <q-card>
            <q-uploader flat accept="image/*" :label="('meme ' + token)" bordered
                style="width: 100%; height: 100%; max-height: 100%;" :factory="factory">
            </q-uploader>
            <q-card-section>
                <q-input v-model="tags" label="tags" borderless>
                </q-input>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>