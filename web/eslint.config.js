import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'
import typescriptEslint from 'typescript-eslint'

export default [
  { ignores: ['*.d.ts', '**/coverage', '**/dist'] },
  ...typescriptEslint.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    // extends: [],
    rules: {},
    files: ['**/*.{ts,vue}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: globals.browser,
      parserOptions: {
        parser: typescriptEslint.parser
      }
    }
  }
]
