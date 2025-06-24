<template>
  <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden">
      <div class="p-6">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">Password Generator</h1>
        
        <div class="mb-6">
          <div class="flex items-center bg-gray-50 p-4 rounded-lg">
            <input
              type="text"
              :value="generatedPassword"
              readonly
              class="w-full bg-transparent text-gray-900 text-lg font-mono focus:outline-none"
            />
            <button
              @click="copyToClipboard"
              class="ml-4 p-2 text-gray-600 hover:text-gray-900"
              :class="{ 'text-green-600': copied }"
            >
              <span v-if="copied">Copied!</span>
              <span v-else>Copy</span>
            </button>
          </div>
        </div>

        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <label class="text-gray-700">Password Length</label>
            <div class="flex items-center">
              <input
                v-model="length"
                type="range"
                min="8"
                max="32"
                class="w-32 mr-4"
              />
              <span class="w-12 text-center">{{ length }}</span>
            </div>
          </div>

          <div class="space-y-2">
            <div class="flex items-center">
              <input
                v-model="includeUppercase"
                type="checkbox"
                class="h-4 w-4 text-blue-600"
              />
              <label class="ml-2 text-gray-700">Include Uppercase</label>
            </div>
            <div class="flex items-center">
              <input
                v-model="includeNumbers"
                type="checkbox"
                class="h-4 w-4 text-blue-600"
              />
              <label class="ml-2 text-gray-700">Include Numbers</label>
            </div>
            <div class="flex items-center">
              <input
                v-model="includeSymbols"
                type="checkbox"
                class="h-4 w-4 text-blue-600"
              />
              <label class="ml-2 text-gray-700">Include Symbols</label>
            </div>
          </div>

          <button
            @click="generatePassword"
            class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Generate Password
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const length = ref(16)
const includeUppercase = ref(true)
const includeNumbers = ref(true)
const includeSymbols = ref(true)
const generatedPassword = ref('')
const copied = ref(false)

const generatePassword = () => {
  const lowercase = 'abcdefghijklmnopqrstuvwxyz'
  const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  const numbers = '0123456789'
  const symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'

  let chars = lowercase
  if (includeUppercase.value) chars += uppercase
  if (includeNumbers.value) chars += numbers
  if (includeSymbols.value) chars += symbols

  let password = ''
  for (let i = 0; i < length.value; i++) {
    const randomIndex = Math.floor(Math.random() * chars.length)
    password += chars[randomIndex]
  }

  generatedPassword.value = password
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(generatedPassword.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy password:', err)
  }
}

// Generate initial password
generatePassword()
</script>
