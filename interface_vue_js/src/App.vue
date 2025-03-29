<template>
  <div class="hello">
    <h1>Buscar Operadoras</h1>
    <input v-model="termo" placeholder="Digite o termo de busca" />
    <button @click="buscar">Buscar</button>
    <table v-if="operadoras.length">
      <thead>
        <tr>
          <th>Registro ANS</th>
          <th>CNPJ</th>
          <th>Razão Social</th>
          <th>Nome Fantasia</th>
          <th>Endereço Eletrônico</th>
          <th>UF</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="operadora in operadoras" :key="operadora.Registro_ANS">
          <td>{{ operadora.Registro_ANS }}</td>
          <td>{{ operadora.CNPJ }}</td>
          <td>{{ operadora.Razao_Social }}</td>
          <td>{{ operadora.Nome_Fantasia }}</td>
          <td>{{ operadora.Endereco_Eletronico }}</td>
          <td>{{ operadora.UF }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Digite um termo e clique em "Buscar" para ver os resultados.</p>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  data() {
    return {
      termo: "", // Termo de busca fornecido pelo usuário
      operadoras: [] // Armazena os resultados retornados pela API
    };
  },
  methods: {
    async buscar() {
      try {
        // Faz a chamada à API Flask
        const response = await fetch(
          `http://127.0.0.1:5000/buscar_operadoras?termo=${this.termo}`
        );
        if (response.ok) {
          this.operadoras = await response.json(); // Armazena os dados no array 'operadoras'
        } else {
          console.error("Erro ao buscar operadoras:", await response.text());
        }
      } catch (error) {
        console.error("Erro de conexão:", error);
      }
    }
  }
};
</script>

<style scoped>
h1 {
  color: #42b983;
}
input {
  margin-bottom: 10px;
  padding: 5px;
}
button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
}
button:hover {
  background-color: #369f72;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  border: 1px solid #ddd;
  text-align: left;
  padding: 8px;
}
th {
  background-color: #42b983;
  color: white;
}
tr:nth-child(even) {
  background-color: #f2f2f2;
}
tr:hover {
  background-color: #ddd;
}
</style>
