<!-- src/components/LibrarianDashboard.vue -->
<template>
  <div class="dashboard">
    <h1>Cadastro/Descadastro De Livros E Usuários</h1>

    <!-- Ações de Livro -->
    <section class="section-book">
      <p>
        Clique Aqui se Deseja
        <router-link to="/livros/new" class="link-register">Cadastrar</router-link>
        um Novo Livro
      </p>
      <button @click="$router.push({ name: 'BookForm' })" class="btn-primary">
        Cadastrar
      </button>

      <p>
        Clique Aqui se Deseja
        <router-link to="/livros/new" class="link-remove">Remover</router-link>
        um Livro
      </p>
      <button @click="$router.push({ name: 'BookForm' })" class="btn-danger">
        Remover
      </button>
    </section>

    <!-- Controle de Usuários -->
    <section class="section-user">
      <h2>Controle De Usuários</h2>

      <!-- Suspender -->
      <form @submit.prevent="suspenderUsuario" class="user-form">
        <div class="form-group">
          <label>Nome do Usuário</label>
          <input
            v-model="suspender.nome"
            type="text"
            placeholder="Nome"
            required
          />
        </div>
        <div class="form-group">
          <label>Tempo (dias)</label>
          <input
            v-model.number="suspender.dias"
            type="number"
            placeholder="Dias"
            required
          />
        </div>
        <button type="submit" class="btn-warning">Suspender</button>
      </form>

      <!-- Reativar -->
      <form @submit.prevent="reativarUsuario" class="user-form">
        <div class="form-group">
          <label>Nome do Usuário</label>
          <input
            v-model="reativar.nome"
            type="text"
            placeholder="Nome"
            required
          />
        </div>
        <button type="submit" class="btn-success">Reativar</button>
      </form>
    </section>
  </div>
</template>

<script>
export default {
  name: 'LibrarianDashboard',
  data() {
    return {
      suspender: { nome: '', dias: 1 },
      reativar: { nome: '' }
    }
  },
  methods: {
    async suspenderUsuario() {
      try {
        const payload = {
          id_usuario: this.suspender.nome,
          motivo: 'Suspensão manual',
          data_inicio: new Date().toISOString(),
          data_fim: new Date(Date.now() + 86400e3 * this.suspender.dias).toISOString()
        }
        await this.$axios.post('/suspensoes', payload)
        alert('Usuário suspenso com sucesso!')
        this.suspender.nome = ''
        this.suspender.dias = 1
      } catch (err) {
        alert('Erro ao suspender usuário.')
      }
    },
    async reativarUsuario() {
      try {
        await this.$axios.post('/suspensoes/reactivate', { nome: this.reativar.nome })
        alert('Usuário reativado com sucesso!')
        this.reativar.nome = ''
      } catch (err) {
        alert('Erro ao reativar usuário.')
      }
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}
.section-book,
.section-user {
  margin-bottom: 40px;
}
.section-book p {
  margin: 10px 0;
}
.link-register {
  color: green;
  text-decoration: none;
  font-weight: 600;
}
.link-remove {
  color: red;
  text-decoration: none;
  font-weight: 600;
}
.user-form {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: flex-end;
  margin-bottom: 20px;
}
.form-group {
  display: flex;
  flex-direction: column;
}
.form-group label {
  font-weight: 600;
  margin-bottom: 4px;
}
.form-group input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.btn-primary,
.btn-danger,
.btn-warning,
.btn-success {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
}
.btn-primary { background: #222; }
.btn-danger  { background: #c62828; }
.btn-warning { background: #f9a825; }
.btn-success { background: #2e7d32; }
</style>
