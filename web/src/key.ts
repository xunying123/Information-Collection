import type { InjectionKey, Ref } from 'vue'
import type { User } from '@/api_interface'

export const user_key = Symbol() as InjectionKey<Ref<User | null>>

export const filter_subscribe_key = Symbol() as InjectionKey<Ref<Boolean>>
export const filter_keyword_key = Symbol() as InjectionKey<Ref<Boolean>>