<!-- src/components/Login.vue -->
<template>
  <div class="login-page">
    <!-- Cabeçalho -->
    <header>
      <div class="header-title">JL Library</div>
      <button class="login-button" @click="showLogin = true">Login</button>
    </header>

    <!-- Seção principal (Hero) -->
    <section class="hero">
      <!-- Card de Login -->
      <div class="login-card" v-if="showLogin">
        <h2>Bem Vindo a JL!</h2>

        <label for="email">Insira seu e-mail</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="E-mail"
        />

        <label for="password">Insira sua senha</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Senha"
        />

        <router-link to="/forgot" class="forgot-password">
          Esqueceu sua senha?
        </router-link>

        <button class="btn-submit" @click="fazerLogin">Fazer login</button>

        <p class="register-p">
          Não tem uma conta?
          <router-link to="/register">Registre-se</router-link>
        </p>
      </div>
    </section>

    <!-- Rodapé -->
    <footer>
      <div class="footer-section">
        <h4>Sobre a JL Library</h4>
        <ul>
          <li><router-link to="/terms">Termos de uso</router-link></li>
          <li><router-link to="/login">Fazer login</router-link></li>
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
      password: ''
    }
  },
  methods: {
    fazerLogin() {
      alert(`Tentando fazer login com:\nE-mail: ${this.email}\nSenha: ${this.password}`)
      // aqui você chamaria o endpoint de login e, em caso de sucesso:
      // this.$router.push({ name: 'Home' })
    }
  }
}
</script>

<style>
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
  background-color: #fff;
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
  font-size: 1rem;
  transition: background-color 0.2s ease;
}
.login-button:hover {
  background-color: #343a40;
}

/* Hero full-screen */
.hero {
  width: 100%;
  height: 100vh; /* ocupa toda altura da viewport */
  background: url('~@/assets/papel-de-parede.jpg') no-repeat center center;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

/* Card de Login */
.login-card {
  position: absolute;
  top: 50%;
  right: 5%;
  transform: translateY(-50%);
  width: 300px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  padding: 1.5rem;
}
.login-card h2 {
  margin-bottom: 1rem;
  font-size: 1.3rem;
  color: #333;
}
.login-card label {
  display: block;
  margin-top: 0.8rem;
  font-weight: 600;
  font-size: 0.9rem;
}
.login-card input {
  width: 100%;
  padding: 0.4rem;
  margin-top: 0.3rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
}
.forgot-password {
  display: block;
  margin: 0.5rem 0;
  text-align: right;
  font-size: 0.8rem;
  color: #007bff;
  text-decoration: none;
}
.forgot-password:hover {
  text-decoration: underline;
}
.btn-submit {
  display: block;
  width: 100%;
  margin-top: 1rem;
  padding: 0.6rem;
  background-color: #212529;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}
.btn-submit:hover {
  background-color: #343a40;
}
.register-p {
  margin-top: 1rem;
  font-size: 0.85rem;
  text-align: center;
}
.register-p a {
  color: #007bff;
  text-decoration: none;
}
.register-p a:hover {
  text-decoration: underline;
}

/* Rodapé */
footer {
  background-color: #212529;
  color: #fff;
  padding: 1rem 2rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
}
.footer-section {
  margin: 0.5rem 0;
}
.footer-section h4 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}
.footer-section ul {
  list-style: none;
}
.footer-section ul li a {
  color: #fff;
  text-decoration: none;
  font-size: 0.9rem;
  display: block;
  margin: 0.2rem 0;
}
.footer-section ul li a:hover {
  text-decoration: underline;
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
    right: 0;
  }
  footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
