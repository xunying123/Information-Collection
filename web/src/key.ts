import type { InjectionKey, Ref } from 'vue'
import type { User } from '@/api_interface'
import type { Category } from '@/sdk'

export const user_key = Symbol() as InjectionKey<Ref<User | null>>
export const all_categories_key = Symbol() as InjectionKey<Ref<Category[]>>

export const filter_subscribe_key = Symbol() as InjectionKey<Ref<boolean>>
export const filter_keyword_key = Symbol() as InjectionKey<Ref<boolean>>
export const search_keyword_key = Symbol() as InjectionKey<Ref<string>>
