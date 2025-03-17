import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
  input: 'http://127.0.0.1:5000/openapi.json',
  output: {
    path: 'src/sdk'
  },
  plugins: [
    {
      name: '@hey-api/client-fetch',
    }
  ]
})
