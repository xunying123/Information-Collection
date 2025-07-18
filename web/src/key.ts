import type { InjectionKey, Ref } from 'vue'
import type { User } from '@/sdk'
import type { CategoryReadable as Category, Subject } from '@/sdk'

export type ViewMode = 'card' | 'site' | 'list' | 'excerpt'
export type SideBarMode = 'category' | 'subject' | 'both'
export type SideBarColor = 'blue' | 'yellow' | 'red' | 'green' | 'orange'

export const user_key = Symbol() as InjectionKey<Ref<User | null>>
export const all_categories_key = Symbol() as InjectionKey<Ref<Category[]>>
export const all_subjects_key = Symbol() as InjectionKey<Ref<Subject[]>>

export const filter_subscribe_key = Symbol() as InjectionKey<Ref<boolean>>
export const filter_keyword_key = Symbol() as InjectionKey<Ref<boolean>>

export const sidebar_show_mode_key = Symbol() as InjectionKey<Ref<SideBarMode | undefined>>
export const sidebar_color_key = Symbol() as InjectionKey<Ref<SideBarColor | undefined>>
export const bg_url_key = Symbol() as InjectionKey<Ref<string | undefined>>
