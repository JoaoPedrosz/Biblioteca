<template>
  <div class="admin-acervo">
    <h1>Meus Livros Cadastrados</h1>
    <div v-if="livros.length" class="grid">
      <div v-for="l in livros" :key="l.isbn" class="card">
        <img :src="getCover(l)" alt="Capa" class="cover" />
        <p class="title">{{ l.nome }}</p>
      </div>
    </div>
    <p v-else>Você não cadastrou nenhum livro ainda.</p>
  </div>
</template>

<script>
export default {
  name: 'AdminAcervo',
  data() {
    return {
      livros: []
    }
  },
  async mounted() {
    await this.fetchMeusLivros()
  },
  methods: {
    async fetchMeusLivros() {
      try {
        // supondo que o backend filtre por usuário logado via token
        // aqui só simulamos pegando todos e filtrando por usuarioId=1
        const res = await this.$axios.get('/livros')
        // se o admin tiver id no localStorage, use ele:
        const user = JSON.parse(localStorage.getItem('usuario') || '{}')
        this.livros = res.data.filter(l => l.usuarioId === user.id)
      } catch (err) {
        console.error('Erro ao buscar meus livros', err)
      }
    },
    getCover(livro) {
      try {
        return require(`@/assets/${livro.nome}.png`)
      } catch (err) {
        return require('@/assets/IconeLivro.png')
      }
    }
  }
}
</script>

<style scoped>
.admin-acervo {
  max-width: 1000px;
  margin: 0 auto;
}
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}
.card {
  width: 150px;
  text-align: center;
}
.cover {
  width: 100%;
  border-radius: 8px;
}
.title {
  margin-top: 8px;
  font-size: 0.95rem;
  color: #222;
}
</style>
