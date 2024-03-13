<script setup lang="ts">
import { useUserStore } from '@/stores/user-store/user-store'
import { ref } from 'vue'

const userStore = useUserStore()

const language = ref(userStore.getAssistants[userStore.getSelectedAssistant].language)
const voice = ref(userStore.getAssistants[userStore.getSelectedAssistant].voice)
const ssid = ref(userStore.getAssistants[userStore.getSelectedAssistant].wifiSSID)
const passwordWifi = ref(userStore.getAssistants[userStore.getSelectedAssistant].wifiPassword)

function setConfiguration() {
  userStore.setAssistantConfiguration(language.value, voice.value, ssid.value, passwordWifi.value)
}
</script>

<template>
  <div class="configuration">
    <div class="header">
      <h1>Historique</h1>
      <v-icon
        class="icon"
        icon="mdi-page-first"
        size="30px"
        @click="userStore.setHistory(userStore.getSelectedAssistant)"
      ></v-icon>
    </div>
    <v-text-field label="Langage" variant="outlined" v-model="language"></v-text-field>
    <v-text-field label="Voix" variant="outlined" v-model="voice"></v-text-field>
    <v-text-field label="SSID Wifi" variant="outlined" v-model="ssid"></v-text-field>
    <v-text-field
      label="Mot de passe Wifi"
      variant="outlined"
      v-model="passwordWifi"
    ></v-text-field>

    <v-btn color="success" @click="setConfiguration" dark>Enregistrer</v-btn>
  </div>
</template>

<style scoped>
.configuration {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 40px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.icon {
  cursor: pointer;
}
</style>
