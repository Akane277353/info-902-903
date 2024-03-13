<script setup lang="ts">
import AddAssistantComponent from '@/components/panel-left/AddAssistantComponent.vue'
import AssistantComponent from '@/components/panel-left/AssistantComponent.vue'
import { useUserStore } from '@/stores/user-store/user-store'

const userStore = useUserStore()

function setHistory(index: number) {
  userStore.setHistory(index)
}

function setSettings(index: number) {
  userStore.setSettings(index)
}

function refresh() {
  userStore.fetchAssistants()
}
</script>

<template>
  <div class="assistants">
    <div class="menu">
      <AddAssistantComponent />
      <v-card height="80" width="80">
        <v-card-actions class="justify-center w-100 h-100">
          <v-btn class="w-100 h-100" @click="refresh"
            ><v-icon
              color="green-darken-2"
              icon="mdi-cached"
              size="70px"
            ></v-icon></v-btn></v-card-actions
      ></v-card>
    </div>

    <AssistantComponent
      v-for="(assistant, index) of userStore.getAssistants"
      :key="index"
      :code="assistant.code"
      @click-assist="setHistory(index)"
      @click-settings="setSettings(index)"
    />
  </div>
</template>

<style scoped>
.assistants {
  gap: 20px;
  padding: 40px;
  margin-left: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.menu {
  display: flex;
  align-items: center;
  gap: 20px;
}
</style>
