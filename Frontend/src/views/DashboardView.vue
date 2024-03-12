<script setup lang="ts">
import AssistantListComponent from '@/components/panel-left/AssistantListComponent.vue'
import HistoryListComponent from '@/components/panel-right/history/HistoryListComponent.vue'
</script>

<template>
  <div class="dashboard">
    <AssistantListComponent />
    <HistoryListComponent />
    <div></div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
}
</style>
