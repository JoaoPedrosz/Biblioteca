<!-- src/components/ForgotPassword.vue -->
<template>
  <div class="container">
    <!-- coluna esquerda: imagem com overlay -->
    <div class="left-section"></div>

    <!-- coluna direita: formulário -->
    <div class="right-section">
      <button class="btn-voltar" @click="voltar">Voltar</button>

      <div class="form-container">
        <h1>Esqueci minha senha</h1>
        <p>Insira seu e-mail para receber um código de verificação para trocar a senha</p>

        <form @submit.prevent="enviarCodigo">
          <label for="email">E-mail</label>
          <input
            id="email"
            type="email"
            v-model="email"
            placeholder="Digite seu e-mail"
            required
          />

          <label for="codigo">Código</label>
          <div class="code-inputs">
            <input
              v-for="(d, i) in codigo"
              :key="i"
              type="text"
              maxlength="1"
              v-model="codigo[i]"
              required
            />
          </div>

          <button class="btn-enviar" type="submit">Enviar</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: '',
      codigo: ['', '', '', '', '']
    }
  },
  methods: {
    enviarCodigo() {
      alert(
        `E-mail: ${this.email}\n` +
        `Código: ${this.codigo.join('')}`
      )
    },
    voltar() {
      this.$router.back()
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
  position: relative;
}
.btn-voltar {
  position: absolute;
  top: 4rem;
  left: 3rem;
  background: #000;
  color: #fff;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-voltar:hover {
  background: #333;
}

.form-container {
  max-width: 350px;
  width: 100%;
}
.form-container h1 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}
.form-container p {
  margin-bottom: 2rem;
  color: #555;
  line-height: 1.4;
}
.form-container label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: bold;
  color: #333;
}
.form-container input[type="email"] {
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

/* inputs de código */
.code-inputs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}
.code-inputs input {
  width: 50px;
  padding: 0.6rem;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

/* botão enviar */
.btn-enviar {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #000;
  color: #fff;
  transition: background 0.2s;
}
.btn-enviar:hover {
  background: #333;
}

/* responsivo */
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
  .btn-voltar {
    top: 1rem;
    left: 1rem;
  }
}
</style>
