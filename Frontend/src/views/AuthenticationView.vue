<script setup lang="ts">
import { useUserStore } from '@/stores/user-store/user-store'
import { ref } from 'vue'

const userStore = useUserStore()

const pseudo = ref('')
const password = ref('')
const confirmPassword = ref('')
const tab = ref('one')
var error = ref('')

function register() {
  if (pseudo.value && password.value && confirmPassword.value === password.value) {
    userStore.register(pseudo.value, password.value)
  }
}

async function login() {
  error.value = ''
  if (pseudo.value && password.value) {
    const isLogin = await userStore.login(pseudo.value, password.value)
    if (isLogin == false) {
      error.value = 'Connexion échouée'
    } else {
      error.value = ''
    }
  }
}

const samePassword = [
  (value: string) => value == password.value || 'les mots de passe ne sont pas identiques.'
]
</script>

<template>
  <div class="authentication">
    <v-card class="mx-auto my-auto px-6 py-8 w-100" max-width="344">
      <v-tabs v-model="tab" align-tabs="center">
        <v-tab value="one">Connexion</v-tab>
        <v-tab value="two">S'enregistrer</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window v-model="tab">
          <v-window-item class="mt-1" value="one">
            <v-text-field
              v-model="pseudo"
              label="Pseudo"
              variant="outlined"
              color="success"
              type="text"
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Mot de passe"
              variant="outlined"
              color="success"
              type="password"
              :error-messages="error"
            ></v-text-field>

            <v-btn @click="login" color="success" :loading="userStore.getIsLoading"
              >Se connecter</v-btn
            >
          </v-window-item>
          <v-window-item class="mt-1" value="two">
            <v-text-field
              v-model="pseudo"
              label="Pseudo"
              variant="outlined"
              color="success"
              type="text"
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Mot de passe"
              variant="outlined"
              color="success"
              type="password"
            ></v-text-field>
            <v-text-field
              v-model="confirmPassword"
              label="Confirmation du mot de passe"
              variant="outlined"
              color="success"
              :rules="samePassword"
              type="password"
            ></v-text-field>

            <v-btn @click="register" color="success" :loading="userStore.getIsLoading"
              >S'enregistrer</v-btn
            >
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </div>
</template>

<style scoped>
.authentication {
  display: flex;
  height: 100vh;
}
</style>
