<script setup lang="ts">
import { useUserStore } from '@/stores/user-store/user-store'
import { ref, watchEffect } from 'vue'
import settings from '../../../assets/settings.png'

const userStore = useUserStore()
const histolist = ref<HTMLDivElement | null>(null)

const scrollToBottom = () => {
  if (histolist.value) {
    histolist.value.scrollTo({
      top: histolist.value.scrollHeight
    })
  }
}

watchEffect(() => {
  scrollToBottom()
})
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
    <div v-if="userStore.getHistory.length > 0" class="histolist" ref="histolist">
      <div class="histo" v-for="(history, index) in userStore.getHistory" :key="index">
        <v-card class="request">{{ history.request }}</v-card>
        <v-card class="response" color="success">{{ history.response }}</v-card>
      </div>
    </div>
    <div v-else class="nohistory">
      <p>Il n'y a pas d'historique</p>
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

.nohistory {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
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
