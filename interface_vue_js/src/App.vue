<template>
  <div class="hello">
    <h1>Buscar Operadoras</h1>
    <div class="search-container">
      <input v-model="termo" placeholder="Digite o termo de busca" />
      <button @click="buscar">Buscar</button>
    </div>

    <form @submit.prevent="adicionarOperadora">
      <h2 v-if="!editando">Adicionar Operadora</h2>
      <h2 v-else>Editar Operadora</h2>
      <div class="form-grid">
        <!-- Registro ANS: varchar(10) -->
        <input
          v-model="novaOperadora.Registro_ANS"
          placeholder="Registro ANS (máx. 10 caracteres)"
          required
          maxlength="10"
        />

        <!-- CNPJ: varchar(18) -->
        <input
          v-model="novaOperadora.CNPJ"
          placeholder="CNPJ (máx. 18 caracteres)"
          required
          maxlength="18"
        />

        <!-- Razão Social: varchar(255) -->
        <input
          v-model="novaOperadora.Razao_Social"
          placeholder="Razão Social"
          required
          maxlength="255"
        />

        <!-- Nome Fantasia: varchar(255) -->
        <input
          v-model="novaOperadora.Nome_Fantasia"
          placeholder="Nome Fantasia"
          maxlength="255"
        />

        <!-- Modalidade: varchar(50) -->
        <input
          v-model="novaOperadora.Modalidade"
          placeholder="Modalidade"
          required
          maxlength="50"
        />

        <!-- Logradouro: varchar(255) -->
        <input
          v-model="novaOperadora.Logradouro"
          placeholder="Logradouro"
          maxlength="255"
        />

        <!-- Número: varchar(15) -->
        <input
          v-model="novaOperadora.Numero"
          placeholder="Número"
          maxlength="15"
        />

        <!-- Complemento: varchar(255) -->
        <input
          v-model="novaOperadora.Complemento"
          placeholder="Complemento"
          maxlength="255"
        />

        <!-- Bairro: varchar(255) -->
        <input
          v-model="novaOperadora.Bairro"
          placeholder="Bairro"
          maxlength="255"
        />

        <!-- Cidade: varchar(255) -->
        <input
          v-model="novaOperadora.Cidade"
          placeholder="Cidade"
          required
          maxlength="255"
        />

        <!-- UF: varchar(2); Usando select para reduzir erros -->
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

        <!-- CEP: varchar(15) -->
        <input
          v-model="novaOperadora.CEP"
          placeholder="CEP (máx. 15 caracteres)"
          maxlength="15"
        />

        <!-- DDD: varchar(5) -->
        <input
          v-model="novaOperadora.DDD"
          placeholder="DDD (máx. 5 caracteres)"
          maxlength="5"
        />

        <!-- Telefone: varchar(15) -->
        <input
          v-model="novaOperadora.Telefone"
          placeholder="Telefone (máx. 15 caracteres)"
          maxlength="15"
        />

        <!-- Fax: varchar(30) -->
        <input
          v-model="novaOperadora.Fax"
          placeholder="Fax (máx. 30 caracteres)"
          maxlength="30"
        />

        <!-- Endereço Eletrônico: varchar(255); usando type=email -->
        <input
          v-model="novaOperadora.Endereco_eletronico"
          placeholder="E-mail"
          required
          type="email"
          maxlength="255"
        />

        <!-- Representante: varchar(255) -->
        <input
          v-model="novaOperadora.Representante"
          placeholder="Representante"
          maxlength="255"
        />

        <!-- Cargo do Representante: varchar(255) -->
        <input
          v-model="novaOperadora.Cargo_Representante"
          placeholder="Cargo do Representante"
          maxlength="255"
        />

        <!-- Região de Comercialização: varchar(255) -->
        <input
          v-model="novaOperadora.Regiao_de_Comercializacao"
          placeholder="Região de Comercialização"
          maxlength="255"
        />

        <!-- Data Registro ANS: date -->
        <input
          v-model="novaOperadora.Data_Registro_ANS"
          type="date"
          placeholder="Data Registro ANS"
        />
      </div>
      <button type="submit">{{ editando ? "Atualizar" : "Adicionar" }}</button>
    </form>

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
      termo: "",
      operadoras: [],
      novaOperadora: {
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
      editando: false,
      operadoraEditando: null
    };
  },
  methods: {
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
    async adicionarOperadora() {
      try {
        if (this.editando) {
          // Cria objeto apenas com os campos modificados
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
    prepararEdicao(operadora) {
      this.novaOperadora = { ...operadora };
      this.operadoraEditando = { ...operadora };
      this.editando = true;
    },
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
