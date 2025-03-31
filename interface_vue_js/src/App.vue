<template>
  <!-- Layout principal do componente para buscar, adicionar/editar e listar operadoras -->
  <div class="hello">
    <h1>Buscar Operadoras</h1>
    <div class="search-container">
      <!-- Campo de busca vinculado à variável 'termo' -->
      <input v-model="termo" placeholder="Digite o termo de busca" />
      <button @click="buscar">Buscar</button>
    </div>

    <!-- Formulário para adicionar ou editar uma operadora -->
    <form @submit.prevent="adicionarOperadora">
      <h2 v-if="!editando">Adicionar Operadora</h2>
      <h2 v-else>Editar Operadora</h2>
      <div class="form-grid">
        <!-- Cada input representa um atributo da nova operadora -->
        <input
          v-model="novaOperadora.Registro_ANS"
          placeholder="Registro ANS (máx. 10 caracteres)"
          required
          maxlength="10"
        />
        <input
          v-model="novaOperadora.CNPJ"
          placeholder="CNPJ (máx. 18 caracteres)"
          required
          maxlength="18"
        />
        <input
          v-model="novaOperadora.Razao_Social"
          placeholder="Razão Social"
          required
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Nome_Fantasia"
          placeholder="Nome Fantasia"
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Modalidade"
          placeholder="Modalidade"
          required
          maxlength="50"
        />
        <input
          v-model="novaOperadora.Logradouro"
          placeholder="Logradouro"
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Numero"
          placeholder="Número"
          maxlength="15"
        />
        <input
          v-model="novaOperadora.Complemento"
          placeholder="Complemento"
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Bairro"
          placeholder="Bairro"
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Cidade"
          placeholder="Cidade"
          required
          maxlength="255"
        />
        <!-- Campo select para UF com opções pré-definidas -->
        <select v-model="novaOperadora.UF" required>
          <option disabled value="">Selecione o UF</option>
          <option value="AC">AC</option>
          <option value="AL">AL</option>
          <option value="AP">AP</option>
          <option value="AM">AM</option>
          <option value="BA">BA</option>
          <option value="CE">CE</option>
          <option value="DF">DF</option>
          <option value="ES">ES</option>
          <option value="GO">GO</option>
          <option value="MA">MA</option>
          <option value="MT">MT</option>
          <option value="MS">MS</option>
          <option value="MG">MG</option>
          <option value="PA">PA</option>
          <option value="PB">PB</option>
          <option value="PR">PR</option>
          <option value="PE">PE</option>
          <option value="PI">PI</option>
          <option value="RJ">RJ</option>
          <option value="RN">RN</option>
          <option value="RS">RS</option>
          <option value="RO">RO</option>
          <option value="RR">RR</option>
          <option value="SC">SC</option>
          <option value="SP">SP</option>
          <option value="SE">SE</option>
          <option value="TO">TO</option>
        </select>
        <input
          v-model="novaOperadora.CEP"
          placeholder="CEP (máx. 15 caracteres)"
          maxlength="15"
        />
        <input
          v-model="novaOperadora.DDD"
          placeholder="DDD (máx. 5 caracteres)"
          maxlength="5"
        />
        <input
          v-model="novaOperadora.Telefone"
          placeholder="Telefone (máx. 15 caracteres)"
          maxlength="15"
        />
        <input
          v-model="novaOperadora.Fax"
          placeholder="Fax (máx. 30 caracteres)"
          maxlength="30"
        />
        <input
          v-model="novaOperadora.Endereco_eletronico"
          placeholder="E-mail"
          required
          type="email"
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Representante"
          placeholder="Representante"
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Cargo_Representante"
          placeholder="Cargo do Representante"
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Regiao_de_Comercializacao"
          placeholder="Região de Comercialização"
          maxlength="255"
        />
        <input
          v-model="novaOperadora.Data_Registro_ANS"
          type="date"
          placeholder="Data Registro ANS"
        />
      </div>
      <button type="submit">{{ editando ? "Atualizar" : "Adicionar" }}</button>
    </form>

    <!-- Tabela exibindo as operadoras cadastradas -->
    <table v-if="operadoras.length">
      <thead>
        <tr>
          <th>Registro ANS</th>
          <th>CNPJ</th>
          <th>Razão Social</th>
          <th>Nome Fantasia</th>
          <th>Endereço Eletrônico</th>
          <th>UF</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="operadora in operadoras" :key="operadora.id">
          <td>{{ operadora.Registro_ANS }}</td>
          <td>{{ operadora.CNPJ }}</td>
          <td>{{ operadora.Razao_Social }}</td>
          <td>{{ operadora.Nome_Fantasia }}</td>
          <td>{{ operadora.Endereco_eletronico }}</td>
          <td>{{ operadora.UF }}</td>
          <td>
            <button @click="prepararEdicao(operadora)">Editar</button>
            <button @click="deletarOperadora(operadora.id)">Excluir</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      termo: "",            // Termo de busca inserido pelo usuário
      operadoras: [],       // Lista de operadoras obtidas do backend
      novaOperadora: {      // Dados para criar ou atualizar uma operadora
        Registro_ANS: "",
        CNPJ: "",
        Razao_Social: "",
        Nome_Fantasia: "",
        Modalidade: "",
        Logradouro: "",
        Numero: "",
        Complemento: "",
        Bairro: "",
        Cidade: "",
        UF: "",
        CEP: "",
        DDD: "",
        Telefone: "",
        Fax: "",
        Endereco_eletronico: "",
        Representante: "",
        Cargo_Representante: "",
        Regiao_de_Comercializacao: "",
        Data_Registro_ANS: "",
      },
      editando: false,         // Flag que indica se estamos editando uma operadora
      operadoraEditando: null  // Armazena a operadora em processo de edição
    };
  },
  methods: {
    // Busca operadoras no backend com base no termo de busca
    async buscar() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/buscar_operadoras?termo=${this.termo}`);
        if (response.ok) {
          this.operadoras = await response.json();
        } else {
          console.error("Erro ao buscar operadoras:", await response.text());
        }
      } catch (error) {
        console.error("Erro de conexão:", error);
      }
    },
    // Adiciona uma nova operadora ou atualiza uma existente, conforme o modo de edição
    async adicionarOperadora() {
      try {
        if (this.editando) {
          // Prepara os dados que foram efetivamente alterados
          const dadosAtualizados = {};
          for (const chave in this.novaOperadora) {
            if (this.novaOperadora[chave] && this.novaOperadora[chave] !== this.operadoraEditando[chave]) {
              dadosAtualizados[chave] = this.novaOperadora[chave];
            }
          }
          if (Object.keys(dadosAtualizados).length === 0) {
            console.warn("Nenhuma alteração detectada.");
            return;
          }
          const response = await fetch(`http://127.0.0.1:5000/operadoras/${this.operadoraEditando.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dadosAtualizados),
          });
          if (response.ok) {
            this.buscar();
            this.resetFormulario();
            this.editando = false;
          }
        } else {
          const response = await fetch("http://127.0.0.1:5000/operadoras", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.novaOperadora),
          });
          if (response.ok) {
            this.buscar();
            this.resetFormulario();
          }
        }
      } catch (error) {
        console.error("Erro ao adicionar/editar operadora:", error);
      }
    },
    // Prepara o formulário de edição preenchendo com os dados da operadora selecionada
    prepararEdicao(operadora) {
      this.novaOperadora = { ...operadora };
      this.operadoraEditando = { ...operadora };
      this.editando = true;
    },
    // Deleta a operadora com base no seu ID
    async deletarOperadora(id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/operadoras/${id}`, {
          method: "DELETE",
        });
        if (response.ok) {
          this.buscar();
        }
      } catch (error) {
        console.error("Erro ao deletar operadora:", error);
      }
    },
    // Reseta o formulário para seu estado inicial
    resetFormulario() {
      this.novaOperadora = {
        Registro_ANS: "",
        CNPJ: "",
        Razao_Social: "",
        Nome_Fantasia: "",
        Modalidade: "",
        Logradouro: "",
        Numero: "",
        Complemento: "",
        Bairro: "",
        Cidade: "",
        UF: "",
        CEP: "",
        DDD: "",
        Telefone: "",
        Fax: "",
        Endereco_eletronico: "",
        Representante: "",
        Cargo_Representante: "",
        Regiao_de_Comercializacao: "",
        Data_Registro_ANS: "",
      };
      this.operadoraEditando = null;
    }
  },
  mounted() {
    // Busca as operadoras assim que o componente é montado
    this.buscar();
  }
};
</script>

<style scoped>
.hello {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.hello h1,
.hello h2 {
  color: #333;
  text-align: center;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

/* Inputs padrão */
input,
select {
  padding: 8px 10px;
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Grid para formulários */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 10px;
}

button {
  margin: 10px 5px;
  padding: 10px 16px;
  background-color: #3498db;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table th, table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

table th {
  background-color: #f2f2f2;
}
</style>
