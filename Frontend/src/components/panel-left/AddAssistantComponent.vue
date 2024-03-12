<script setup lang="ts">
import { useUserStore } from '@/stores/user-store/user-store'
import { ref } from 'vue'

const userStore = useUserStore()
var dialog = ref(false)
var code = ref('')

function addAssistant() {
  userStore.addAssistant(userStore.getUser?.id, code.value)
  dialog.value = false
}
</script>

<template>
  <div>
    <v-card height="200" width="300">
      <v-card-actions class="justify-center w-100 h-100">
        <v-btn class="w-100 h-100" @click="dialog = true"
          ><v-icon
            color="green-darken-2"
            icon="mdi-plus"
            size="80px"
          ></v-icon></v-btn></v-card-actions
    ></v-card>

    <v-dialog v-model="dialog" width="auto">
      <v-card max-width="400" title="Ajouter un Noodle Home">
        <v-text-field label="Code" variant="outlined" v-model="code"></v-text-field>
        <template v-slot:actions>
          <v-btn class="ms-auto" text="Ajouter" @click="addAssistant"></v-btn>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
v-text-field {
  width: 80%;
}
</style>
