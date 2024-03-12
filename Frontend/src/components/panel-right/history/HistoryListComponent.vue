<script setup lang="ts">
import { useUserStore } from '@/stores/user-store/user-store'

const userStore = useUserStore()
</script>

<template>
  <div class="history">
    <div class="histo" v-for="(history, index) in userStore.getHistory" :key="index">
      <p class="request">{{ history.request }}</p>
      <p class="response">{{ history.response }}</p>
    </div>
  </div>
</template>

<style scoped>
.history {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.histo {
  display: flex;
  flex-direction: column;
}

.request {
  margin-right: 10px;
  margin-left: auto;
}

.response {
  margin-left: 10px;
  margin-right: auto;
}
</style>
