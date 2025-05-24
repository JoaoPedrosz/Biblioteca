import axios from 'axios'
const api = axios.create({
  baseURL: 'http://localhost:5000'
})

export default {
  getAll () {
    return api.get('/carros')
  },

  getById (id) {
    return api.get(`/carros/${id}`)
  },

  create (data) {
    return api.post('/carros', data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  update (id, data) {
    return api.put(`/carros/${id}`, data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  delete (id) {
    return api.delete(`/carros/${id}`)
  }
}
