<script setup lang="ts">
import AddAssistantComponent from '@/components/panel-left/AddAssistantComponent.vue'
import AssistantComponent from '@/components/panel-left/AssistantComponent.vue'
import { useUserStore } from '@/stores/user-store/user-store'

const userStore = useUserStore()

function setHistory(index: number) {
  userStore.setHistory(index)
}
</script>

<template>
  <div>
    <AddAssistantComponent />
    <AssistantComponent
      v-for="(assistant, index) of userStore.getAssistants"
      :key="index"
      :code="assistant.code"
      @click="setHistory(index)"
    />
  </div>
</template>

<style scoped></style>
