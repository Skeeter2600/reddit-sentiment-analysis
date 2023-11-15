<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { TabStrip, type TabStripTabProperties } from '@progress/kendo-vue-layout';
import type { Topic } from '@/models/topic.model';

const props = defineProps<{
  topic: Topic;
}>();

// Simulate network request
</script>

<template>
  <Suspense> </Suspense>
</template>

<style scoped>
h2 {
  font-weight: 500;
  font-size: 2.6rem;
}
</style>
