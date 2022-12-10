<script>
export default {
    props: {
        label: {
            type: String,
            default: "",
        },
        debounce: {},
    },
    data() {
        return {
            value: "",
        }
    },
    emits: ['input'],
    methods: {
    },
    watch: {
    }
}
</script>

<template>
    <q-input v-model="value" :label="label" :debounce="debounce">
        <template #prepend>
            <slot name="prepend"></slot>
        </template>
    </q-input>
</template>