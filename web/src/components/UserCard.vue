<script setup lang="ts">
import { user_key } from '@/key'
import { inject } from 'vue'
import { ElAvatar } from 'element-plus'

let user = inject(user_key)!
</script>

<!-- <div v-if="user" class="horizon-grid"> -->
<template>
  <div class="user-card" v-if="user">
    <ElAvatar :src="user.avatars!" class="avatar" />
    <div class="user-info">
      <h2>{{ user.name }}</h2>
      <p>{{ user.organization }}</p>
    </div>
  </div>
</template>
<!-- </div> -->

<style lang="css" scoped>
@media (max-width: 768px) {
  .avatar {
    width: 30px !important;
    height: 30px !important;
  }
}

.avatar {
  width: 50px;
  /* 调整为你需要的大小 */
  height: 50px;
  object-fit: cover;
  border-radius: 50%;
}

.horizon-grid {
  /* display: grid; */
  grid-template-columns: min-content 1fr;
  align-items: center;
  justify-items: start;
  grid-column-gap: 1em;
  padding: 0 1em;
}

.user-card {
  display: grid;
  grid-template-columns: auto 1fr;
  /* 调整为你需要的比例 */
  align-items: center;
  cursor: pointer;
  margin: 0.5em 1em;
  padding: 0.2em;
}

.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 2em;
  color: white;
}

.user-card {
  transition-duration: 0.3s;
}
.user-card:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 0.5em;
  transition: background-color 0.3s;
}
</style>
