<script setup lang="ts">
const props = defineProps({
  code: { type: Number, required: true },
  isactivated: { type: Boolean, required: true }
})
</script>

<template>
  <div>
    <v-card class="d-flex" height="130" width="200" :color="isactivated ? 'success' : ''">
      <v-card-actions>
        <h1>{{ props.code }}</h1>
      </v-card-actions>
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
