import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000'
})

export default {
  register(form) {
    return api.post('/register', {
      nome: form.name,
      email: form.email,
      cpf: form.cpf,
      telefone: form.telefone,
      data_nascimento: form.dataNascimento,
      password: form.password,
      tipo: 'usuario'
    })
  },

  login(email, password) {
    return api.post('/login', { email, password })
  }
}
