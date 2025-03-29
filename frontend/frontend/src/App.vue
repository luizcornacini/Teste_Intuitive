<script setup>
import { ref } from "vue";
import axios from "axios";

const termo = ref("");
const resultados = ref([]);

const buscar = async () => {
  const { data } = await axios.get(`http://localhost:8000/buscar/?termo=${termo.value}`);
  resultados.value = data;
};
</script>

<template>
  <div>
    <h1>Buscar Procedimentos</h1>
    <input v-model="termo" placeholder="Digite um termo..." />
    <button @click="buscar">Buscar</button>
    
    <ul>
      <li v-for="item in resultados" :key="item.id">{{ item.Nome }}</li>
    </ul>
  </div>
</template>
