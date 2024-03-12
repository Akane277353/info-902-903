<script setup lang="ts">
import { useUserStore } from '@/stores/user-store/user-store'

const userStore = useUserStore()
</script>

<template>
  <div class="history">
    <div class="histo" v-for="(history, index) in userStore.getHistory" :key="index">
      <p>{{ history.request }}</p>
      <p>{{ history.response }}</p>
    </div>
  </div>
</template>

<style scoped>
.history {
  background-color: beige;
  width: 100%;
  height: 100%;
}
</style>
