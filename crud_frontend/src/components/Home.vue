<template>
  <div class="home">
    <h1>Meus Livros</h1>
    <div v-if="livros.length" class="grid">
      <div v-for="l in livros" :key="l.isbn" class="card">
        <img :src="getCover(l)" alt="Capa" class="cover" />
        <p class="title">{{ l.nome }}</p>
      </div>
    </div>
    <p v-else>Você não tem livros no momento.</p>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      livros: []
    }
  },
  async mounted() {
    await this.fetchLivros()
  },
  methods: {
    async fetchLivros() {
      try {
        const res = await this.$axios.get('/livros')
        this.livros = res.data.slice(0, 2) // exibe só os 2 primeiros
      } catch (err) {
        console.error('Erro ao buscar livros', err)
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
.home {
  max-width: 1000px;
  margin: 0 auto;
}
.grid {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
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
