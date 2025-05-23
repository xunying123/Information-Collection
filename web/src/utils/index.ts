import { ref, watch } from 'vue'

export function ref_localStorage<T>(
  key: string,
  defaultValue?: T,
  parse: (x: string) => T | null = JSON.parse,
  stringify: (x: T) => string = JSON.stringify
) {
  const lv = localStorage.getItem(key)
  const data: T | undefined = (lv != null && parse(lv)) || defaultValue
  const rv = ref<T>()
  if (data != null) rv.value = data
  watch(rv, (v) =>
    v != null ? localStorage.setItem(key, stringify(v)) : localStorage.removeItem(key)
  )
  return rv
}
