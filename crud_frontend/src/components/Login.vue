<!-- src/components/Login.vue -->
<template>
  <div class="login-page">
    <!-- Cabeçalho -->
    <header>
      <div class="header-title">JL Library</div>
      <button class="login-button" @click="showLogin = !showLogin">
        {{ showLogin ? 'Fechar' : 'Login' }}
      </button>
    </header>

    <!-- Seção principal -->
    <section class="hero">
      <div v-if="showLogin" class="login-card">
        <h2>Bem-vindo(a) à JL!</h2>

        <div v-if="error" class="error-message">{{ error }}</div>

        <form @submit.prevent="fazerLogin">
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
            placeholder="Digite sua senha"
            required
          />

          <router-link to="/forgot" class="forgot-password">
            Esqueceu sua senha?
          </router-link>

          <button type="submit" class="btn-submit">Fazer login</button>

          <p class="register-p">
            Não tem uma conta?
            <router-link to="/register">Registre-se</router-link>
          </p>
        </form>
      </div>
    </section>

    <!-- Rodapé -->
    <footer>
      <div class="footer-section">
        <h4>Sobre a JL Library</h4>
        <ul>
          <li><router-link to="/terms">Termos de uso</router-link></li>
          <li><router-link to="/login">Login</router-link></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4>Siga nas redes sociais</h4>
        <ul>
          <li><a href="#">Instagram</a></li>
          <li><a href="#">Facebook</a></li>
          <li><a href="#">Twitter</a></li>
        </ul>
      </div>
      <div class="footer-section">
        <p>2024 | Feito por João Silva e Lucas Monteferrante</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      showLogin: true,
      email: '',
      senha: '',
      error: ''
    }
  },
  methods: {
    async fazerLogin() {
      this.error = ''
      try {
        const res = await this.$axios.post('/login', {
          email: this.email,
          senha: this.senha
        })

        // Captura token e dados do usuário
        const token = res.data.access_token
        const user = res.data.user

        // Salva no localStorage
        localStorage.setItem('access_token', token)
        localStorage.setItem('user', JSON.stringify(user))

        // Ajusta header padrão
        this.$axios.defaults.headers.common['Authorization'] = 'Bearer ' + token

        // Redireciona de acordo com o tipo
        if (user.tipo === 'bibliotecario') {
          this.$router.push({ name: 'AdminDashboard' })
        } else {
          this.$router.push({ name: 'Home' })
        }
      } catch (err) {
        this.error =
          (err.response && err.response.data && err.response.data.erro) ||
          'Falha ao fazer login.'
      }
    }
  }
}
</script>

<style scoped>
/* Reset básico */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.login-page,
body {
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
  color: #333;
  min-height: 100vh;
}

/* Cabeçalho */
header {
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  border-bottom: 1px solid #ccc;
}
.header-title {
  font-size: 1.5rem;
  font-weight: bold;
}
.login-button {
  background-color: #212529;
  color: #fff;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.login-button:hover {
  background-color: #343a40;
}

/* Hero full-screen */
.hero {
  position: relative;
  width: 100%;
  height: 100vh;
  background: url('~@/assets/papel-de-parede.jpg') no-repeat center center;
  background-size: cover;
}

/* Card de Login posicionado à direita */
.login-card {
  position: absolute;
  top: 50%;
  right: 5%;
  transform: translateY(-50%);
  background-color: #fff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  width: 320px;
}
.login-card h2 {
  margin-bottom: 1rem;
}

/* Mensagem de erro */
.error-message {
  color: #d70000;
  margin-bottom: 1rem;
}

/* Formulário */
.login-card label {
  display: block;
  margin-top: 0.8rem;
  font-weight: 600;
}
.login-card input {
  width: 100%;
  padding: 0.6rem;
  margin-top: 0.3rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.forgot-password {
  display: block;
  margin: 0.5rem 0 1rem;
  font-size: 0.85rem;
  text-align: right;
  color: #007bff;
}
.forgot-password:hover {
  text-decoration: underline;
}
.btn-submit {
  width: 100%;
  padding: 0.6rem;
  background: #212529;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn-submit:hover {
  background: #343a40;
}
.register-p {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.85rem;
}
.register-p a {
  color: #007bff;
  text-decoration: none;
}

/* Rodapé */
footer {
  background: #212529;
  color: #fff;
  padding: 1rem 2rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.footer-section {
  margin: 0.5rem 0;
}
.footer-section h4 {
  margin-bottom: 0.5rem;
}
.footer-section ul {
  list-style: none;
}
.footer-section ul li a {
  color: #fff;
}
.footer-section p {
  font-size: 0.9rem;
}

/* Responsivo */
@media (max-width: 768px) {
  .hero {
    height: 50vh;
  }
  .login-card {
    position: static;
    transform: none;
    margin: 1rem auto;
  }
  footer {
    flex-direction: column;
  }
}
</style>
