<script setup lang="ts">
import { useUserStore } from '@/stores/user-store/user-store'
import settings from '../../../assets/settings.png'

const userStore = useUserStore()
</script>

<template>
  <div class="history">
    <div class="header">
      <h1>Historique</h1>
      <img
        width="30"
        height="30"
        :src="settings"
        alt="settings"
        @click="userStore.setSettings(userStore.getSelectedAssistant)"
      />
    </div>
    <div class="histolist">
      <div class="histo" v-for="(history, index) in userStore.getHistory" :key="index">
        <v-card class="request">{{ history.request }}</v-card>
        <v-card class="response" color="success">{{ history.response }}</v-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.history {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 40px;
}

.histolist {
  overflow: auto;
  scrollbar-width: none;
}

.histo {
  display: flex;
  flex-direction: column;
}

.request {
  margin-top: 20px;
  margin-right: 10px;
  margin-left: auto;
  max-width: 80%;
  padding: 5px;
}

.response {
  margin-top: 20px;
  margin-right: auto;
  max-width: 80%;
  padding: 5px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

img {
  cursor: pointer;
}
</style>
