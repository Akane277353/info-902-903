<script setup lang="ts">
import AddAssistantComponent from '@/components/panel-left/AddAssistantComponent.vue'
import AssistantComponent from '@/components/panel-left/AssistantComponent.vue'
import { useUserStore } from '@/stores/user-store/user-store'

const userStore = useUserStore()
</script>

<template>
  <div>
    <AddAssistantComponent />
    <AssistantComponent
      v-for="assistant of userStore.getAssistants"
      :key="assistant.code"
      :code="assistant.code"
    />
  </div>
</template>

<style scoped></style>
