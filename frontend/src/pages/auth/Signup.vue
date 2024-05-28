<template>
  <VaForm ref="form" @submit.prevent="submit">
    <h1 class="font-semibold text-4xl mb-4">注册</h1>
    <p class="text-base mb-4 leading-5">
      已经有账号了？
      <RouterLink :to="{ name: 'login' }" class="font-semibold text-primary">登录</RouterLink>
    </p>
    <VaInput
      v-model="formData.email"
      :rules="[(v) => !!v || '邮箱不能为空', (v) => /.+@.+\..+/.test(v) || '无效邮箱']"
      class="mb-4"
      label="邮箱"
      type="email"
    />
    <VaValue v-slot="isPasswordVisible" :default-value="false">
      <VaInput
        ref="password1"
        v-model="formData.password"
        :rules="passwordRules"
        :type="isPasswordVisible.value ? 'text' : 'password'"
        class="mb-4"
        label="密码"
        messages="为了您的安全：密码应为8个以上字符：字母、数字和特殊字符。"
        @clickAppendInner.stop="isPasswordVisible.value = !isPasswordVisible.value"
      >
        <template #appendInner>
          <VaIcon
            :name="isPasswordVisible.value ? 'mso-visibility_off' : 'mso-visibility'"
            class="cursor-pointer"
            color="secondary"
          />
        </template>
      </VaInput>
      <VaInput
        ref="password2"
        v-model="formData.repeatPassword"
        :rules="[
          (v) => !!v || '重复密码不能为空',
          (v) => v === formData.password || '两次密码不一致',
        ]"
        :type="isPasswordVisible.value ? 'text' : 'password'"
        class="mb-4"
        label="重复密码"
        @clickAppendInner.stop="isPasswordVisible.value = !isPasswordVisible.value"
      >
        <template #appendInner>
          <VaIcon
            :name="isPasswordVisible.value ? 'mso-visibility_off' : 'mso-visibility'"
            class="cursor-pointer"
            color="secondary"
          />
        </template>
      </VaInput>
    </VaValue>

    <div class="flex justify-center mt-4">
      <VaButton class="w-full" @click="submit">创建账号</VaButton>
    </div>
  </VaForm>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useToast } from 'vuestic-ui'

const { validate } = useForm('form')
const { push } = useRouter()
const { init } = useToast()

const formData = reactive({
  email: '',
  password: '',
  repeatPassword: '',
})

const submit = () => {
  if (validate()) {
    init({
      message: "注册成功 :)",
      color: 'success',
    })
    push({ name: 'dashboard' })
  }
}

const passwordRules: ((v: string) => boolean | string)[] = [
  (v) => !!v || '密码不能为空',
  (v) => (v && v.length >= 8) || '密码至少需要8个字符',
  (v) => (v && /[A-Za-z]/.test(v)) || '密码至少需要一个字母',
  (v) => (v && /\d/.test(v)) || '密码至少需要一个数字',
  (v) => (v && /[!@#$%^&*(),.?":{}|<>]/.test(v)) || '密码至少需要一个特殊符号，如!@#$%^&*(),.?":{}|<>',
]
</script>
