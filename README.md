# Sistema de Gerenciamento de Tarefas - Teste para Desenvolvedor Júnior

## 🎯 Objetivo
Desenvolver um sistema completo de gerenciamento de tarefas que demonstre conhecimentos em desenvolvimento full-stack com as tecnologias especificadas.

## 🛠 Tecnologias Requeridas

### Backend
- **Framework**: Java Spring Boot, Python FastAPI ou Ruby on Rails (fica a seu critério)
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Documentação**: Swagger/OpenAPI + README.md
- **Containerização**: Docker e Docker Compose

### Frontend
- **Framework**: Next.js (React)
- **Validação**: Zod para validação de formulários
- **TypeScript**: Obrigatório

## 🚀 Funcionalidades Esperadas

### Autenticação
- [ ] Registro de usuário
- [ ] Login com email e senha
- [ ] Proteção de rotas com JWT
- [ ] Logout

### Gerenciamento de Tarefas
- [ ] Listar todas as tarefas do usuário logado
- [ ] Criar nova tarefa
- [ ] Visualizar detalhes de uma tarefa
- [ ] Editar tarefa existente
- [ ] Excluir tarefa
- [ ] Marcar tarefa como concluída/pendente

## 📊 Estrutura de Dados (sugerida)

### Usuário
```json
{
  "id": "Long",
  "nome": "String",
  "email": "String (único)",
  "senha": "String",
  "data_criacao": "DateTime",
  "data_atualizacao": "DateTime"
}
```

### Tarefa
```json
{
  "id": "Long",
  "titulo": "String",
  "descricao": "String",
  "status": "PENDENTE | CONCLUIDA",
  "prioridade": "BAIXA | MEDIA | ALTA",
  "data_vencimento": "Date",
  "data_criacao": "DateTime",
  "data_atualizacao": "DateTime",
  "usuario_id": "Long"
}
```

## 🔗 APIs Esperadas

### Autenticação
- `POST /api/auth/register` - Registrar usuário
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/userinfo` - Dados do usuário logado

### Tarefas
-  Listar tarefas do usuário
-  Criar nova tarefa
-  Buscar tarefa por ID
-  Atualizar tarefa
-  Excluir tarefa
-  Alterar status da tarefa

## 🏗 Estrutura do Projeto - Monorepo

```
fullstack-jr-2025-2/
├── backend/                 # Spring Boot API
├── frontend/               # Next.js App
├── docker-compose.yml      # Orquestração dos containers
└── README.md              # Este arquivo
```

## ⚡ Execução Local

```bash
# Clone o repositório
git clone https://github.com/heynet-solutions/fullstack-jr-2025-2.git
cd fullstack-jr-2025-2

# Executar com Docker Compose
docker-compose up -d

# Acessar aplicação
Frontend: http://localhost:3000
Backend API: http://localhost:8080 ou http://localhost:8000
Swagger: http://localhost:8080/swagger-ui.html ou http://localhost:8000/docs
```
## 📦 Entregáveis

1. **Repositório GitHub** com código fonte completo
2. **README.md** com instruções de instalação e execução
3. **Deploy** em servidor público (Heroku, Vercel, Railway, etc.)
4. **Documentação Swagger** acessível
5. **Collection Postman** ou arquivo com exemplos de requisições
6. **Testes Automatizados** para o projeto, cobrindo as principais funcionalidades do backend (autenticação e gerenciamento de tarefas).

## ✅ Recursos Permitidos
- Documentação oficial das tecnologias
- Stack Overflow
- GitHub Copilot
- ChatGPT para dúvidas pontuais

## ❌ Não Permitido
- Copiar código de projetos existentes
- Usar bibliotecas que façam o trabalho principal
- Pedir ajuda para outras pessoas

Boa sorte no teste! 🚀