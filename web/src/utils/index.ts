import { ref, watch, type Ref } from 'vue'

export function ref_localStorage<T>(
  key: string,
  defaultValue: T | null = null
): Ref<T | undefined> {
  const lv = localStorage.getItem(key) as string | null
  const data: T | null = lv ? (JSON.parse(lv) as T) : defaultValue
  const rv: Ref<T | undefined> = ref<T>()
  if (data) rv.value = data
  watch(rv, (v) => localStorage.setItem(key, JSON.stringify(v)))
  return rv
}
