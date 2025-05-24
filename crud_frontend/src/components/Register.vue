<template>
  <b-row class="vh-100 vw-100 no-gutters">
    <!-- Coluna da ilustração (fundo cinza) -->
    <b-col
      sm="7"
      class="side-register d-flex justify-content-center align-items-center"
    >
      <img
        :src="registerIllustration"
        class="img-register"
        alt="Register Illustration"
      />
    </b-col>

    <!-- Coluna do formulário -->
    <b-col
      sm="5"
      class="d-flex justify-content-center align-items-center"
    >
      <div class="form-container">
        <h2 class="text-center mb-4 title-login">
          Faça o seu cadastro
        </h2>
        <b-form @submit.prevent="register">
          <!-- Nome -->
          <b-form-group label="Nome" label-for="name">
            <b-form-input
              id="name"
              v-model.trim="$v.form.name.$model"
              :state="getValidation('name')"
              placeholder="João Silva"
            />
            <b-form-invalid-feedback>
              Nome obrigatório (mínimo 3 caracteres)
            </b-form-invalid-feedback>
          </b-form-group>

          <!-- E-mail -->
          <b-form-group label="E-mail" label-for="email">
            <b-form-input
              id="email"
              type="email"
              v-model.trim="$v.form.email.$model"
              :state="getValidation('email')"
              placeholder="joaosilva@email.com"
              autocomplete="off"
            />
            <b-form-invalid-feedback>
              E-mail obrigatório
            </b-form-invalid-feedback>
          </b-form-group>

          <!-- CPF (com máscara e estado de validação) -->
          <b-form-group label="CPF" label-for="cpf">
            <b-form-input
              id="cpf"
              v-model.trim="$v.form.cpf.$model"
              v-mask="'###.###.###-##'"
              :state="getValidation('cpf')"
              placeholder="000.000.000-00"
            />
            <b-form-invalid-feedback>
              CPF obrigatório
            </b-form-invalid-feedback>
          </b-form-group>

          <!-- Telefone (com máscara e estado de validação) -->
          <b-form-group label="Telefone" label-for="telefone">
            <b-form-input
              id="telefone"
              v-model.trim="$v.form.telefone.$model"
              v-mask="'(##)#####-####'"
              :state="getValidation('telefone')"
              placeholder="(XX)XXXXX-XXXX"
            />
            <b-form-invalid-feedback>
              Telefone obrigatório
            </b-form-invalid-feedback>
          </b-form-group>

          <!-- Data de Nascimento -->
          <b-form-group label="Data de Nascimento" label-for="dataNascimento">
            <b-form-input
              id="dataNascimento"
              type="date"
              v-model="$v.form.dataNascimento.$model"
              :state="getValidation('dataNascimento')"
            />
            <b-form-invalid-feedback>
              Data de nascimento obrigatória
            </b-form-invalid-feedback>
          </b-form-group>

          <!-- Senha -->
          <b-form-group label="Senha" label-for="password">
            <b-form-input
              id="password"
              type="password"
              v-model.trim="$v.form.password.$model"
              :state="getValidation('password')"
              placeholder="Digite uma senha"
            />
            <b-form-invalid-feedback>
              Senha obrigatória (mínimo 6 caracteres)
            </b-form-invalid-feedback>
          </b-form-group>

          <!-- Confirmação de Senha -->
          <b-form-group
            label="Confirme a senha"
            label-for="confirmPassword"
          >
            <b-form-input
              id="confirmPassword"
              type="password"
              v-model.trim="$v.form.confirmPassword.$model"
              :state="getValidation('confirmPassword')"
              placeholder="Repita a senha"
            />
            <b-form-invalid-feedback>
              As senhas devem coincidir
            </b-form-invalid-feedback>
          </b-form-group>

          <!-- Botões -->
          <b-button type="submit" variant="primary" block>
            Cadastrar
          </b-button>
          <hr />
          <b-button
            type="button"
            variant="outline-secondary"
            block
            @click="goToLogin"
          >
            ← Voltar
          </b-button>

          <!-- Mensagem de erro geral -->
          <p v-if="erro" class="text-danger mt-2">{{ erro }}</p>
        </b-form>
      </div>
    </b-col>
  </b-row>
</template>

<script>
import { required, minLength, sameAs } from 'vuelidate/lib/validators'
import UserService from '@/services/UserService'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        name: '',
        email: '',
        cpf: '',
        telefone: '',
        dataNascimento: '',
        password: '',
        confirmPassword: ''
      },
      registerIllustration: require('@/assets/register.svg'),
      erro: null
    }
  },
  validations: {
    form: {
      name: { required, minLength: minLength(3) },
      email: { required },
      cpf: { required },
      telefone: { required },
      dataNascimento: { required },
      password: { required, minLength: minLength(6) },
      confirmPassword: { required, sameAsPassword: sameAs('password') }
    }
  },
  methods: {
    async register() {
      this.$v.$touch()
      if (this.$v.$error) return

      try {
        await UserService.register(this.form)
        this.$router.push('/login')
      } catch (err) {
        this.erro = 'Erro ao cadastrar usuário'
      }
    },
    getValidation(field) {
      return this.$v.form.$dirty
        ? !this.$v.form[field].$error
        : null
    },
    goToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.side-register {
  background-color: #f2f2f2;
}
.img-register {
  width: 80%;
  max-width: 600px;
}
.form-container {
  width: 80%;
  max-width: 360px;
}
.title-login {
  font-weight: bold;
}
</style>
