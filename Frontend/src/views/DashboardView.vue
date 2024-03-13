<script setup lang="ts">
import AssistantListComponent from '@/components/panel-left/AssistantListComponent.vue'
import ConfigurationComponent from '@/components/panel-right/configuration/ConfigurationComponent.vue'
import HistoryListComponent from '@/components/panel-right/history/HistoryListComponent.vue'

import { useUserStore } from '@/stores/user-store/user-store'

const userStore = useUserStore()
</script>

<template>
  <div class="dashboard">
    <AssistantListComponent />
    <div class="center">
      <HistoryListComponent v-if="userStore.getIsHistories" />
      <ConfigurationComponent v-if="!userStore.getIsHistories" />
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  height: 100vh;
}

.center {
  scroll-behavior: smooth;
  width: 100%;
}
</style>
