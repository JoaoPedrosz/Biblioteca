<!-- src/components/Register.vue -->
<template>
  <div class="container">
    <!-- coluna esquerda -->
    <div class="left-section"></div>

    <!-- coluna direita -->
    <div class="right-section">
      <div class="form-container">
        <h1>Criar Nova Conta</h1>

        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">{{ success }}</div>

        <form @submit.prevent="criarConta">
          <label>Tipo de usuário</label>
          <div class="radio-group">
            <label>
              <input type="radio" value="usuario" v-model="tipo" /> Usuário
            </label>
            <label>
              <input type="radio" value="bibliotecario" v-model="tipo" /> Bibliotecário
            </label>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="nome">Nome</label>
              <input id="nome" type="text" v-model="nome" required />
            </div>
            <div class="form-group">
              <label for="sobrenome">Sobrenome</label>
              <input id="sobrenome" type="text" v-model="sobrenome" required />
            </div>
          </div>

          <label for="dataNasc">Data de nascimento</label>
          <input id="dataNasc" type="date" v-model="dataNasc" required />

          <label for="telefone">Telefone</label>
          <input
            id="telefone"
            type="tel"
            v-model="telefone"
            placeholder="(XX) XXXXX-XXXX"
            required
          />

          <label for="email">E-mail</label>
          <input
            id="email"
            type="email"
            v-model="email"
            placeholder="Digite seu e-mail"
            required
          />

          <label for="senha">Senha</label>
          <input
            id="senha"
            type="password"
            v-model="senha"
            placeholder="Crie sua senha"
            required
          />

          <label for="confirmaSenha">Confirmar senha</label>
          <input
            id="confirmaSenha"
            type="password"
            v-model="confirmaSenha"
            placeholder="Confirme sua senha"
            required
          />

          <button class="btn-submit" type="submit" :disabled="loading">
            {{ loading ? 'Cadastrando...' : 'Criar Conta' }}
          </button>
        </form>

        <p class="login-link">
          Já tem conta?
          <router-link to="/login">Login</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      tipo: 'usuario',
      nome: '',
      sobrenome: '',
      dataNasc: '',
      telefone: '',
      email: '',
      senha: '',
      confirmaSenha: '',
      error: '',
      success: '',
      loading: false
    }
  },
  methods: {
    async criarConta() {
      this.error = ''
      this.success = ''
      if (this.senha !== this.confirmaSenha) {
        this.error = 'As senhas não conferem.'
        return
      }
      this.loading = true
      try {
        const payload = {
          tipo: this.tipo,
          nome: this.nome,
          sobrenome: this.sobrenome,
          data_nascimento: this.dataNasc,
          telefone: this.telefone,
          email: this.email,
          senha: this.senha
        }
        await this.$axios.post('/register', payload)
        this.success = 'Conta criada com sucesso! Redirecionando…'
        // aguarda um pouquinho pra mostrar a mensagem
        setTimeout(() => {
          this.$router.push({ name: 'Login' })
        }, 1000)
      } catch (err) {
        this.error =
          (err.response && err.response.data && err.response.data.erro) ||
          'Falha ao criar conta.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body,
.container {
  font-family: Arial, sans-serif;
}

/* container duas colunas */
.container {
  display: flex;
  width: 100vw;
  height: 100vh;
}

/* imagem + overlay */
.left-section {
  flex: 1.2;
  background: url('~@/assets/papel-de-parede.jpg') no-repeat center center;
  background-size: cover;
  position: relative;
}
.left-section::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(0,0,0,0.7), rgba(0,0,0,0));
}

/* formulário */
.right-section {
  flex: 1;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
.form-container {
  max-width: 400px;
  width: 100%;
}

.form-container h1 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.error-message {
  color: #d70000;
  margin-bottom: 1rem;
}

.success-message {
  color: #007700;
  margin-bottom: 1rem;
}

.radio-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.radio-group label {
  font-weight: normal;
  position: relative;
  padding-left: 1.6rem;
}
.radio-group input[type="radio"] {
  position: absolute;
  left: 0;
  top: 0;
  margin-top: 3px;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: bold;
  color: #333;
}

input[type="text"],
input[type="date"],
input[type="tel"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.btn-submit {
  display: inline-block;
  width: 100%;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  background: #000;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-submit:hover:not(:disabled) {
  background: #333;
}

.login-link {
  margin-top: 1rem;
  text-align: center;
}
.login-link a {
  color: #007bff;
  text-decoration: none;
}
.login-link a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }
  .left-section,
  .right-section {
    flex: none;
    width: 100%;
    height: 50vh;
  }
}
</style>
