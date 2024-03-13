<script setup lang="ts">
import { useUserStore } from '@/stores/user-store/user-store'
import { ref } from 'vue'

const userStore = useUserStore()
var dialog = ref(false)
var code = ref()
var error = ref('')

async function addAssistant() {
  error.value = 'false'
  var response = await userStore.addAssistant(userStore.getUser.id, code.value)
  if (response == false) {
    error.value = 'Code invalide'
  } else {
    error.value = 'false'
    dialog.value = false
  }
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
        <v-text-field
          label="Code"
          variant="outlined"
          v-model="code"
          type="number"
          :error-messages="error"
        ></v-text-field>
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
