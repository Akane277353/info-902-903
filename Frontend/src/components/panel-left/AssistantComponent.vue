<script setup lang="ts">
import settings from '../../assets/settings.png'
const props = defineProps({
  code: { type: Number, required: true }
})
</script>

<template>
  <div>
    <v-card class="d-flex" height="200" width="300">
      <h1>{{ props.code }}</h1>
      <img width="30" height="30" :src="settings" alt="settings" />
    </v-card>
  </div>
</template>

<style scoped>
img {
  margin-top: 10px;
  margin-right: 10px;
  margin-left: auto;
  cursor: pointer;
}

h1 {
  margin-top: auto;
  margin-bottom: auto;
  margin-left: auto;
  margin-right: auto;
  font-size: 30px;
  font-weight: 500;
  color: #4a4a4a;
}
</style>
