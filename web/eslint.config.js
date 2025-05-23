import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'
import typescriptEslint from 'typescript-eslint'

export default [
  { ignores: ['*.d.ts', '**/coverage', '**/dist'] },
  ...typescriptEslint.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    // extends: [],
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'vue/max-attributes-per-line': 'off',
      'vue/first-attribute-linebreak': [
        'warn',
        {
          singleline: 'ignore',
          multiline: 'ignore'
        }
      ],
      'vue/html-closing-bracket-newline': [
        'warn',
        {
          singleline: 'never',
          multiline: 'always',
          selfClosingTag: {
            singleline: 'never',
            multiline: 'always'
          }
        }
      ],
      'vue/html-indent': [
        'warn',
        2,
        {
          attribute: 1,
          baseIndent: 1,
          closeBracket: 0,
          alignAttributesVertically: true,
          ignores: [],
          alignAttributesVertically: false
        }
      ],
      'vue/prop-name-casing': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      'vue/html-self-closing': 'off'
    },
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
