import type { InjectionKey, Ref } from 'vue'
import type { User } from '@/api_interface'

export const user_key = Symbol() as InjectionKey<Ref<User | null>>
