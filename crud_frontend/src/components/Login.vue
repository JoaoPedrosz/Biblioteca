<!-- src/components/Login.vue -->
<template>
  <b-row class="vh-100 vw-100 no-gutters">
    <!-- Coluna do formulário -->
    <b-col sm="5" class="left-login d-flex justify-content-center align-items-center">
      <div class="form-container">
        <h2 class="text-center mb-4 title-login">Faça o login</h2>
        <b-form @submit.prevent="login">
          <b-form-group label="E-mail" label-for="email">
            <b-form-input
              id="email"
              type="email"
              v-model.trim="$v.form.email.$model"
              :state="getValidation('email')"
              placeholder="joaosilva@email.com"
              autocomplete="off"
            />
          </b-form-group>

          <b-form-group label="Senha" label-for="password">
            <b-form-input
              id="password"
              type="password"
              v-model.trim="$v.form.password.$model"
              :state="getValidation('password')"
              placeholder="Digite sua senha"
            />
          </b-form-group>

          <b-button type="submit" variant="primary" block>
            <i class="fas fa-sign-in-alt mr-2"></i>Entrar
          </b-button>

          <hr />

          <b-button type="button" variant="outline-secondary" block @click="goToRegister">
            <i class="fas fa-user-plus mr-2"></i>Não tenho conta
          </b-button>
        </b-form>

        <p v-if="erro" class="text-danger mt-2">{{ erro }}</p>
      </div>
    </b-col>

    <!-- Coluna da ilustração -->
    <b-col sm="7" class="side-login d-flex justify-content-center align-items-center">
      <img :src="loginIllustration" class="img-login" alt="Login Illustration" />
    </b-col>
  </b-row>
</template>

<script>
import { required, minLength } from 'vuelidate/lib/validators'
import UserService from '@/services/UserService'

export default {
  name: 'Login',

  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loginIllustration: require('@/assets/car.svg'),
      erro: null
    }
  },

  validations: {
    form: {
      email: { required },
      password: { required, minLength: minLength(6) }
    }
  },

  methods: {
    async login() {
      this.$v.$touch()
      if (this.$v.$error) return

      try {
        const res = await UserService.login(this.form.email, this.form.password)

        // ✅ Salva token e tipo do usuário no localStorage
        localStorage.setItem('token', res.data.access_token)
        localStorage.setItem('tipo', res.data.user.tipo) // ← campo aninhado corretamente
        localStorage.setItem('email', res.data.user.email)

        this.$router.push('/carros')
      } catch (err) {
        this.erro = 'Usuário ou senha inválidos'
      }
    },

    getValidation(field) {
      return this.$v.form.$dirty ? !this.$v.form[field].$error : null
    },

    goToRegister() {
      this.$router.push('/register')
    }
  }
}
</script>

<style scoped>
.left-login {
  background-color: #f2f2f2;
}

.form-container {
  width: 80%;
  max-width: 360px;
}

.title-login {
  font-weight: bold;
}

.img-login {
  width: 80%;
  max-width: 600px;
}
</style>
