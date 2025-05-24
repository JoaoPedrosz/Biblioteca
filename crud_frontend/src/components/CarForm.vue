<template>
  <b-row class="vh-100 vw-100 no-gutters">
    <b-col sm="5" class="left-form d-flex justify-content-center align-items-center">
      <div class="form-container">
        <h2 class="text-center mb-4">
          {{ isEdit ? 'Editar Anúncio' : 'Novo Anúncio de Carro' }}
        </h2>
        <b-form @submit.prevent="submitForm">
          <b-form-group label="Modelo" label-for="modelo">
            <b-form-input
              id="modelo"
              v-model.trim="$v.form.modelo.$model"
              :state="validationState('modelo')"
              placeholder="Ex: Volkswagen Up"
              required
            />
            <b-form-invalid-feedback>Modelo é obrigatório</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Cidade" label-for="cidade">
            <b-form-input
              id="cidade"
              v-model.trim="$v.form.cidade.$model"
              :state="validationState('cidade')"
              placeholder="Ex: Belo Horizonte - MG"
              required
            />
            <b-form-invalid-feedback>Cidade é obrigatória</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Ano" label-for="ano">
            <b-form-input
              id="ano"
              v-model.trim="$v.form.ano.$model"
              :state="validationState('ano')"
              type="number"
              placeholder="Ex: 2020"
              required
            />
            <b-form-invalid-feedback>Ano é obrigatório</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="KM" label-for="km">
            <b-form-input
              id="km"
              v-model.trim="$v.form.km.$model"
              :state="validationState('km')"
              type="number"
              placeholder="Ex: 45000"
              required
            />
            <b-form-invalid-feedback>KM é obrigatório</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Preço (R$)" label-for="preco">
            <b-form-input
              id="preco"
              v-model.trim="$v.form.preco.$model"
              :state="validationState('preco')"
              type="number"
              placeholder="Ex: 65000"
              required
            />
            <b-form-invalid-feedback>Preço é obrigatório</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Câmbio" label-for="cambio">
            <b-form-select
              id="cambio"
              v-model="$v.form.cambio.$model"
              :options="optionsCambio"
              :state="validationState('cambio')"
              required
            />
            <b-form-invalid-feedback>Selecione o câmbio</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Carroceria" label-for="carroceria">
            <b-form-select
              id="carroceria"
              v-model="$v.form.carroceria.$model"
              :options="optionsCarroceria"
              :state="validationState('carroceria')"
              required
            />
            <b-form-invalid-feedback>Selecione a carroceria</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Cor" label-for="cor">
            <b-form-select
              id="cor"
              v-model="$v.form.cor.$model"
              :options="optionsCor"
              :state="validationState('cor')"
              required
            />
            <b-form-invalid-feedback>Selecione a cor</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Combustível" label-for="combustivel">
            <b-form-select
              id="combustivel"
              v-model="$v.form.combustivel.$model"
              :options="optionsCombustivel"
              :state="validationState('combustivel')"
              required
            />
            <b-form-invalid-feedback>Selecione o combustível</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Imagem do Carro" label-for="imagem">
            <b-form-file
              id="imagem"
              accept="image/*"
              @change="onFileChange"
              :state="fileState"
            />
            <b-form-invalid-feedback>Selecione uma imagem válida</b-form-invalid-feedback>
            <b-img
              v-if="preview"
              :src="preview"
              fluid
              class="mt-2"
              alt="Preview da Imagem"
            />
          </b-form-group>

          <b-button type="submit" variant="primary" block>
            <i class="fas fa-save mr-2"></i> {{ isEdit ? 'Atualizar' : 'Cadastrar' }}
          </b-button>

          <hr />
          <b-button type="button" variant="outline-secondary" block @click="cancel">
            ← Voltar
          </b-button>
          <p v-if="erro" class="text-danger mt-2">{{ erro }}</p>
        </b-form>
      </div>
    </b-col>

    <b-col sm="7" class="side-form d-flex justify-content-center align-items-center">
      <img :src="illustration" class="img-illustration" alt="Ilustração" />
    </b-col>
  </b-row>
</template>

<script>
import { required, minLength, numeric } from 'vuelidate/lib/validators'
import { validationMixin } from 'vuelidate'
import CarService from '@/services/CarService'
import carIllustration from '@/assets/car.svg'

export default {
  name: 'CarForm',
  mixins: [validationMixin],
  data() {
    return {
      form: {
        modelo: '',
        cidade: '',
        ano: null,
        km: null,
        preco: null,
        cambio: '',
        carroceria: '',
        cor: '',
        combustivel: '',
        imagem: null
      },
      isEdit: false,
      erro: null,
      preview: null,
      illustration: carIllustration,
      optionsCambio: [
        { value: 'Manual', text: 'Manual' },
        { value: 'Automático', text: 'Automático' }
      ],
      optionsCarroceria: [
        { value: 'Hatchback', text: 'Hatchback' },
        { value: 'Sedan', text: 'Sedan' },
        { value: 'SUV', text: 'SUV' },
        { value: 'Picape', text: 'Picape' }
      ],
      optionsCor: [
        { value: 'Prata', text: 'Prata' },
        { value: 'Branco', text: 'Branco' },
        { value: 'Preto', text: 'Preto' },
        { value: 'Vermelho', text: 'Vermelho' }
      ],
      optionsCombustivel: [
        { value: 'Gasolina', text: 'Gasolina' },
        { value: 'Álcool', text: 'Álcool' },
        { value: 'Diesel', text: 'Diesel' },
        { value: 'Flex', text: 'Flex' }
      ]
    }
  },
  validations: {
    form: {
      modelo: { required, minLength: minLength(3) },
      cidade: { required, minLength: minLength(3) },
      ano: { required, numeric },
      km: { required, numeric },
      preco: { required, numeric },
      cambio: { required },
      carroceria: { required },
      cor: { required },
      combustivel: { required }
    }
  },
  async mounted() {
    const id = this.$route.params.id
    if (id) {
      this.isEdit = true
      try {
        const res = await CarService.getById(id)
        const carro = res.data
        this.form = {
          modelo: carro.modelo,
          cidade: carro.cidade,
          ano: carro.ano,
          km: carro.km,
          preco: carro.preco,
          cambio: carro.cambio,
          carroceria: carro.carroceria,
          cor: carro.cor,
          combustivel: carro.combustivel,
          imagem: null
        }
        this.preview = carro.imagem
      } catch (err) {
        console.error(err)
        this.erro = 'Erro ao carregar os dados para edição'
      }
    }
  },
  methods: {
    validationState(field) {
      const f = this.$v.form[field]
      return f.$dirty ? !f.$error : null
    },
    onFileChange(event) {
      const file = event.target.files[0]
      if (!file) {
        this.preview = null
        this.form.imagem = null
        return
      }
      this.form.imagem = file
      this.preview = URL.createObjectURL(file)
    },
    async submitForm() {
      this.$v.$touch()
      if (this.$v.$error) return

      const payload = new FormData()
      for (const [key, val] of Object.entries(this.form)) {
        if (val !== null) {
          payload.append(key, val)
        }
      }

      try {
        const id = this.$route.params.id
        if (this.isEdit) {
          await CarService.update(id, payload)
        } else {
          await CarService.create(payload)
        }
        this.$router.push('/carros')
      } catch (err) {
        console.error(err)
        this.erro = 'Erro ao salvar o anúncio'
      }
    },
    cancel() {
      this.$router.back()
    }
  },
  computed: {
    fileState() {
      return this.form.imagem ? true : null
    }
  }
}
</script>

<style scoped>
.left-form {
  background-color: #f8f9fa;
}
.side-form {
  background-color: #e9ecef;
}
.form-container {
  width: 80%;
  max-width: 360px;
}
.img-illustration {
  width: 80%;
  max-width: 600px;
}
</style>
