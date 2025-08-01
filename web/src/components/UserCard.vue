<script setup lang="ts">
import { user_key } from '@/key'
import { inject } from 'vue'
// import { ElAvatar } from 'element-plus'

let user = inject(user_key)!
</script>

<!-- <div v-if="user" class="horizon-grid"> -->
<template>
  <div v-if="user" class="user-card">
    <!-- <ElAvatar :src="user.avatars!" class="avatar" /> -->
    <div class="welcome-container">
      <!-- <h2>欢迎您，{{ user.name }}</h2> -->
      <h2>
        <span class="welcome-text">欢迎您，</span>
        <span class="username">{{ user.name }}</span>
      </h2>
      <div class="user-status" />
    </div>
    <!-- <p>{{ user.organization }}</p> -->
  </div>
</template>
<!-- </div> -->

<style lang="css" scoped>
@media (max-width: 768px) {
  .avatar {
    width: 30px !important;
    height: 30px !important;
  }
  .welcome-container h2 {
    display: flex;
    flex-direction: column;
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
  /* grid-template-columns: auto 1fr; */
  /* 调整为你需要的比例 */
  /* align-items: center; */
  /* cursor: pointer; */
  /* margin: 0.5em 1em; */
  /* padding: 0.2em; */
}

.user-info {
  display: grid;
  /* centering */
  /* flex-direction: column; */
  justify-content: center;
  margin-left: 0.5em;
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

.welcome-container {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  justify-items: start;
  grid-column-gap: 0.5em;
  padding: 0 1em;
  color: white;
  font-size: 1em;
  font-weight: bold;
  margin-left: 1.5em;
}

.user-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #2ecc71;
  margin-left: 5px;
}
</style>
