<script setup lang="ts">
import { jaccount_client_id, jaccount_oauth, server } from '@/const'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

let route = useRoute()
const next = computed(() => {
  return typeof route.query.next === 'string' ? route.query.next : '/err'
})

let auth_redirect_url = computed(() => {
  let url = new URL(jaccount_oauth)
  url.searchParams.append('client_id', jaccount_client_id)
  url.searchParams.append('response_type', 'code')
  url.searchParams.append('redirect_uri', `${server}/auth`)
  // url.searchParams.append('scope', 'openid')
  url.searchParams.append('state', `${location.origin}${next.value}`)
  return url.toString()
})
console.log(route)
</script>

<template>
  {{ next }}
  <hr />
  {{ auth_redirect_url }}
  <div
    style="width: 10em; height: 7em; display: flex; align-items: center; justify-content: center"
  >
    <a :href="auth_redirect_url" target="_self"><button>使用 JAccount 登陆</button></a>
  </div>
</template>
