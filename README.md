# API Principal - Gerenciamento de Restaurantes e Avaliações

API RESTful para gerenciamento completo de restaurantes, usuários e avaliações, com integração automática com OpenStreetMap para busca de locais próximos.

## 📋 Sobre

Esta é a API principal do sistema de recomendação de restaurantes. Ela oferece:

- **Gerenciamento de usuários**: Registro e autenticação de usuários.
- **Cadastro de restaurantes**: Criar, buscar, atualizar e deletar restaurantes.
- **Sistema de avaliações**: Usuários podem avaliar restaurantes com nota (1-5) e comentário.
- **Busca geoespacial**: Integração com API Secundária para buscar restaurantes próximos.
- **Sincronização automática**: Integra restaurantes encontrados no OpenStreetMap ao banco de dados.
- **Cálculo de distância**: Exibe distância do usuário até restaurantes (opcional).

## 🚀 Quick Start

### Pré-requisitos

- Docker (recomendado)
- Python 3.9+ (para desenvolvimento local)
- SQLite (incluído no Python)
- API Secundária rodando em `localhost:8000`

### Com Docker

```bash
docker build -t api-principal:v1 .
docker run -p 8000:8000 api-principal:v1
```

API estará disponível em `http://localhost:8000`

Documentação interativa: `http://localhost:8000/openapi/swagger` (Swagger)

### Desenvolvimento Local

```bash
# Clone o repositório
git clone
cd api-principal

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env

# Inicialize o banco de dados
python -c "from database import init_db; init_db()"

# Execute a aplicação
python app.py
```

## 📚 Principais Endpoints

### 👤 Usuários

#### Registrar novo usuário
```http
POST /usuarios/registrar
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "senha123"
}
```

**Response (201 Created):**
```json
{
  "usuario_id": "7a743fa4-57b5-4b0b-b97a-5da34a58bf62",
  "nome": "João Silva",
  "email": "joao@email.com",
  "data_criacao": "2025-12-21T23:00:00"
}
```

### 🍽️ Restaurantes

#### Criar restaurante (manual)
```http
POST /restaurantes/criar
Content-Type: application/json

{
  "nome": "Pizzaria Delluccio",
  "endereco": "Rua Batatais, 282",
  "cuisine": "pizza",
  "latitude": -23.5710717,
  "longitude": -46.6564156
}
```

**Response (201 Created):**
```json
{
  "restaurante_id": 1,
  "nome": "Pizzaria Delluccio",
  "endereco": "Rua Batatais, 282",
  "cuisine": "pizza",
  "latitude": -23.5710717,
  "longitude": -46.6564156,
  "data_criacao": "2025-12-21T23:00:00"
}
```

#### Buscar restaurante por ID (com distância opcional)
```http
GET /restaurantes/1?latitude_usuario=-23.55&longitude_usuario=-46.63
```

**Response (200 OK):**
```json
{
  "status": "success",
  "dados": {
    "restaurante_id": 1,
    "nome": "Pizzaria Delluccio",
    "endereco": "Rua Batatais, 282",
    "cuisine": "pizza",
    "latitude": -23.5710717,
    "longitude": -46.6564156,
    "distancia_km": 3.42,
    "data_criacao": "2025-12-21T23:00:00"
  }
}
```

#### Buscar restaurantes próximos (via OpenStreetMap)
```http
POST /restaurantes/buscar-proximidade
Content-Type: application/json

{
  "latitude": -23.5505,
  "longitude": -46.6333,
  "raio_km": 5,
  "tipo": "pizza"
}
```

**Response (200 OK):**
```json
{
  "sucesso": true,
  "total": 12,
  "bbox_utilizado": {
    "lat_max": -23.505,
    "lat_min": -23.596,
    "lng_max": -46.588,
    "lng_min": -46.678
  },
  "sincronizacao": {
    "sincronizados": 12,
    "duplicados": 0
  },
  "mensagem": "Sincronizou 12 restaurantes com sucesso"
}
```

#### Atualizar restaurante (PATCH)
```http
PATCH /restaurantes/1
Content-Type: application/json

{
  "nome": "Pizzaria Delluccio Premium",
  "telefone": "+55 11 3456-7890"
}
```

### ⭐ Avaliações

#### Criar avaliação
```http
POST /avaliacoes/criar
Content-Type: application/json

{
  "usuario_id": 1,
  "restaurante_id": 1,
  "nota": 5,
  "comentario": "Excelente! Recomendo!"
}
```

**Response (201 Created):**
```json
{
  "usuario_id": "7a743fa4-57b5-4b0b-b97a-5da34a58bf62",
  "restaurante_id": 1,
  "nota": 5,
  "comentario": "Excelente! Recomendo!",
  "data_avaliacao": "2025-12-21T23:00:00"
}
```

#### Buscar avaliação (com distância opcional)
```http
GET /avaliacoes/1/7a743fa4-57b5-4b0b-b97a-5da34a58bf62
```

**Response (200 OK):**
```json
{
  "status": "success",
  "dados": {
    "usuario_id": "7a743fa4-57b5-4b0b-b97a-5da34a58bf62",
    "restaurante_id": 1,
    "nota": 5,
    "comentario": "Excelente! Recomendo!",
    "data_avaliacao": "2025-12-21T23:00:00"
  }
}
```

#### Deletar avaliação
```http
DELETE /avaliacoes/1/7a743fa4-57b5-4b0b-b97a-5da34a58bf62
```

**Response (200 OK):**
```json
{
  "status": "success",
  "mensagem": "Avaliacao removida com sucesso."
}
```

## 🔧 Estrutura do Projeto

```
api-principal/
├── app.py                      # Aplicação principal (Flask)
├── config.py                   # Configurações
├── database.py                 # Conexão SQLAlchemy
├── requirements.txt            # Dependências
├── .env.example                # Template variáveis
├── Dockerfile                  # Containerização
├── README.md                   # Este arquivo
│
├── models/
│   ├── __init__.py
│   ├── usuario.py             # Modelo Usuario
│   ├── restaurante.py         # Modelo Restaurante
│   └── avaliacao.py           # Modelo Avaliacao
│
├── routes/
│   ├── __init__.py
│   ├── usuarios.py            # Endpoints /usuarios
│   ├── restaurantes.py        # Endpoints /restaurantes
│   └── avaliacoes.py          # Endpoints /avaliacoes
│
├── schemas/
│   ├── __init__.py
│   ├── usuario_schema.py      # Validação Usuario
│   ├── restaurante_schema.py  # Validação Restaurante
│   └── avaliacao_schema.py    # Validação Avaliacao
│
└── utils/
    ├── __init__.py
    ├── openstreetmap.py       # Integração API Secundária
    └── validations.py         # Funções de validação
```

## 🔌 Integrações Externas

### API Secundária (OpenStreetMap)

- **URL**: `http://localhost:8001`
- **Endpoints**:
  - `POST /contexto/restaurantes/buscar` - Busca por proximidade
  - `POST /contexto/restaurantes/distancia` - Cálculo de distância
  - `POST /contexto/restaurantes/endereco` - Reverse geocoding

### Banco de Dados

- **SQLite**: `restaurantes.db`
- **ORM**: SQLAlchemy 2.0
- **Tabelas**: usuarios, restaurantes, avaliacoes

## 📊 Tratamento de Erros

Todos os endpoints retornam status HTTP padrão:

| Status | Significado |
|--------|------------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 400 | Erro de validação |
| 404 | Recurso não encontrado |
| 409 | Conflito (ex: email duplicado) |
| 500 | Erro interno do servidor |

**Exemplo de erro:**
```json
{
  "status": "error",
  "erro": "Restaurante não encontrado"
}
```

## 🐳 Docker

### Build

```bash
docker build -t api-principal:v1 .
```

### Run

```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e API_SECUNDARIA_URL=http://api-secundaria:8000 \
  api-principal:v1
```

## 🔄 Fluxo de Funcionamento

```
1. Usuário se registra
   POST /usuarios/registrar

2. Usuário busca restaurantes próximos
   POST /restaurantes/buscar-proximidade
      ↓
   API Secundária (Overpass + Nominatim)
      ↓
   Restaurantes sincronizados ao banco

3. Usuário vê detalhes do restaurante
   GET /restaurantes/{id}?latitude_usuario=...

4. Usuário avalia o restaurante
   POST /avaliacoes/criar

5. Outros usuários veem a avaliação
   GET /avaliacoes/{restaurante_id}/{usuario_id}
```

## 🏗️ Arquitetura

**[📊 Ver diagrama completo da arquitetura](./docs/arquitetura-mvp.png)**

## 🤝 Contribuindo

1. Crie uma branch: `git checkout -b feature/minha-feature`
2. Commit: `git commit -m 'Adiciona feature'`
3. Push: `git push origin feature/minha-feature`
4. Pull Request

## 📄 Licença

Este projeto está sob licença MIT.

### v1.0.0 (2025-12-21)
- ✅ CRUD de usuários
- ✅ CRUD de restaurantes
- ✅ Sistema de avaliações
- ✅ Integração OpenStreetMap
- ✅ Sincronização automática
- ✅ Cálculo de distância
- ✅ Documentação Swagger
- ✅ SQLite com SQLAlchemy 2.0
