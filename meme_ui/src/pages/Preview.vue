<script>
export default {
    props: ['tags', 'src'],
    data() {
        return {
            isPreviewing: false,
        }
    },
}
</script>

<template>
    <q-dialog v-model="isPreviewing" auto-close full-height full-width class="shadow-10">
        <q-card>
            <q-bar>
                <div class="full-width row wrap justify-start items-start content-center">
                    <q-chip v-for="item in tags" outline class="text-caption">
                        {{ item }}
                    </q-chip>
                </div>
            </q-bar>
            <q-card-section>
                <div class="absolute-full flex flex-center">
                    <q-img :src="src" loading="lazy" fit="scale-down">
                        <template #error>
                            wtf
                        </template>
                    </q-img>
                </div>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>