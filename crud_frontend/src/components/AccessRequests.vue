<!-- src/components/AccessRequests.vue -->
<template>
  <div class="access-requests">
    <h1>Requisição De Acesso</h1>
    <p class="subtitle">Solicitações Para Usuários:</p>
    <ul class="requests-list">
      <li
        v-for="req in requests"
        :key="req.id"
        class="request-item"
      >
        <span class="user-name">{{ req.nome }}</span>
        <div class="buttons">
          <button
            class="btn-authorize"
            @click="authorize(req.id)"
          >
            Autorizar
          </button>
          <button
            class="btn-reject"
            @click="reject(req.id)"
          >
            Recusar
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'AccessRequests',
  data() {
    return {
      // simulando dados vindos do backend
      requests: [
        { id: 1, nome: 'João Pedro De Paula Silva' },
        { id: 2, nome: 'Lucas Gonçalves Monteferrante' },
        { id: 3, nome: 'Aline Ferreira Matos' }
      ]
    }
  },
  methods: {
    authorize(id) {
      // aqui você chamaria this.$axios.post(`/solicitacoes/${id}/authorize`)
      this.requests = this.requests.filter(r => r.id !== id)
      alert(`Solicitação ${id} autorizada!`)
    },
    reject(id) {
      // ou this.$axios.post(`/solicitacoes/${id}/reject`)
      this.requests = this.requests.filter(r => r.id !== id)
      alert(`Solicitação ${id} recusada!`)
    }
  }
}
</script>

<style scoped>
.access-requests {
  max-width: 800px;
  margin: 0 auto;
}

.subtitle {
  font-size: 1.1rem;
  margin-bottom: 12px;
}

.requests-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.request-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #222d36;
  color: white;
  border-radius: 24px;
  padding: 12px 20px;
  margin-bottom: 16px;
}

.user-name {
  font-size: 1.05rem;
}

.buttons button {
  margin-left: 12px;
  padding: 6px 16px;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  font-weight: 600;
}

.btn-authorize {
  background: white;
  color: #222d36;
}

.btn-reject {
  background: #f57c00;
  color: white;
}
</style>
