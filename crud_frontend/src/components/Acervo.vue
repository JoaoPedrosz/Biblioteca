<template>
  <div class="acervo">
    <h1>Sugestões De Leitura</h1>
    <div v-if="livros.length" class="grid">
      <div v-for="l in livros" :key="l.isbn" class="card">
        <img :src="getCover(l)" alt="Capa" class="cover" />
        <p class="title">{{ l.nome }}</p>
      </div>
    </div>
    <p v-else>Carregando acervo...</p>
  </div>
</template>

<script>
export default {
  name: 'Acervo',
  data() {
    return {
      livros: []
    }
  },
  async mounted() {
    await this.fetchAcervo()
  },
  methods: {
    async fetchAcervo() {
      try {
        const res = await this.$axios.get('/livros')
        this.livros = res.data
      } catch (err) {
        console.error('Erro ao buscar acervo', err)
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
.acervo {
  max-width: 1200px;
  margin: 0 auto;
}
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.card {
  width: 120px;
  text-align: center;
}
.cover {
  width: 100%;
  border-radius: 6px;
}
.title {
  margin-top: 6px;
  font-size: 0.9rem;
  color: #222;
}
</style>
