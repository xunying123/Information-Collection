<script setup lang="ts">
import { jaccount_client_id, jaccount_oauth, server } from '@/const'
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

let route = useRoute()
let router = useRouter()

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

onMounted(() => {
  window.location.href = auth_redirect_url.value
})
</script>
