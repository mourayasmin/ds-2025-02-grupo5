## Problemas relatados pelos stakeholders

- Falta de validações dos campos utilizados para realizar inscrições
- Retrabalho manual em fazer curadoria dos incritos para agrega-los por mentor e escola
- Falta de confirmação de que o email utilizado é válido
- Falta de controle para evitar inscrições duplicadas

## Solução Proposta

Como os stakeholders relataram mais dificuldades com relação a consistência geral dos dados das inscrições, tomamos como decisão focar nessa parte no decorrer da realização do trabalho e da disciplina. Uma vez que, também, os fornecedores desses requisitos possuem uma aplicação front-end já bem estruturada.

### Proposta inicial de arquitetura do sistema

```mermaid
graph TB
    subgraph "Interface do Estudante"
        A[Formulário de Registro]
        A1[Campo de Escola<br/>com Autocompletar]
        A2[Informações Pessoais]
        A3[Botão Enviar]
    end

    subgraph "Serviços da API"
        B[API de Autocompletar]
        C[API de Registro]
        D[API de Validação<br/>de Escola]
    end

    subgraph "Lógica de Validação"
        E{Gerenciador de<br/>Estratégia de Validação}
        F[Validador de<br/>Correspondência Exata]
        G[Validador de<br/>Correspondência Difusa]
        H[Sinalizar para<br/>Revisão Manual]
    end

    subgraph "Processamento de Dados"
        I[Repositório de Escolas]
        J[Processador de Registro]
        K[Verificador de Duplicatas]
        L[Correspondente de Escolas]
    end

    subgraph "Banco de Dados"
        M[(Registro de<br/>Escolas Válidas)]
        N[(Registros de<br/>Estudantes)]
    end

    subgraph "Notificações"
        O[E-mail de Sucesso]
        P[Alerta para Admin<br/>Revisão Manual]
    end

    A --> A1
    A --> A2
    A --> A3
    
    A1 -->|Digita Nome da Escola| B
    B --> I
    I -->|Consulta Escolas| M
    M -->|Retorna Correspondências| B
    B -->|Exibe Opções| A1
    
    A3 -->|Envia Formulário| C
    C -->|Valida Escola| D
    
    D --> E
    E -->|Verifica Escola| F
    E -->|Se Não Houver Correspondência Exata| G
    E -->|Se Incerto| H
    
    F -->|Escola Válida| I
    G -->|Escola Similar Encontrada| I
    G -->|Pontuação de Confiança| E
    H -->|Sinaliza Entrada| P
    
    I --> M
    
    C --> J
    J --> K
    K -->|Verifica Duplicata| N
    J --> L
    L -->|Corresponde com Escola| M
    
    J -->|Salva Registro| N
    N -->|Sucesso| O
    
    O -.->|E-mail Enviado| A
    P -.->|Admin Notificado| Admin[Painel do Administrador]
    
    style A fill:#e1f5ff
    style A1 fill:#b3e0ff
    style E fill:#fff4e1
    style F fill:#fff4e1
    style G fill:#fff4e1
    style H fill:#ffcccc
    style M fill:#d4edda
    style N fill:#d4edda
    style O fill:#d1ecf1
    style P fill:#f8d7da
```

### Diagrama de sequeência correspondente a tal arquitetura

```mermaid
sequenceDiagram
    actor E as Estudante
    participant F as Formulário Web
    participant API as API Gateway
    participant AC as Serviço de<br/>Autocompletar
    participant VS as Serviço de<br/>Validação
    participant VE as Estratégia de<br/>Validação
    participant R as Repositório<br/>de Escolas
    participant PR as Processador<br/>de Registro
    participant DB as Banco de Dados
    participant N as Serviço de<br/>Notificação
    participant A as Admin

    Note over E,F: Fase 1: Preenchimento do Formulário
    E->>F: Acessa formulário de registro
    F->>E: Exibe formulário vazio
    
    E->>F: Digita nome da escola (ex: "Colégio Dom...")
    F->>API: GET /schools/autocomplete?q="Colégio Dom..."
    API->>AC: Buscar escolas
    AC->>R: Consultar por prefixo
    R->>DB: SELECT * FROM schools WHERE name LIKE '%Colégio Dom%'
    DB-->>R: Lista de escolas correspondentes
    R-->>AC: Retorna lista
    AC-->>API: Lista de sugestões
    API-->>F: JSON com escolas
    F->>E: Exibe dropdown com opções

    E->>F: Seleciona "Colégio Dom Pedro II"
    E->>F: Preenche dados pessoais (nome, email, etc)
    
    Note over E,PR: Fase 2: Submissão e Validação
    E->>F: Clica em "Enviar"
    F->>API: POST /registrations (dados do estudante)
    
    API->>VS: Validar escola informada
    VS->>VE: Aplicar estratégia de validação
    
    alt Correspondência Exata
        VE->>R: Buscar escola exata
        R->>DB: SELECT * FROM schools WHERE name = 'Colégio Dom Pedro II'
        DB-->>R: Escola encontrada
        R-->>VE: Escola válida (100% confiança)
        VE-->>VS: Validação aprovada
        
    else Correspondência Difusa
        VE->>R: Buscar escolas similares
        R->>DB: SELECT * FROM schools
        DB-->>R: Lista de todas as escolas
        R-->>VE: Calcular similaridade
        VE->>VE: Algoritmo de fuzzy matching<br/>(Levenshtein, Token matching)
        
        alt Confiança > 85%
            VE-->>VS: Escola similar encontrada (85-99% confiança)
            Note over VS: "Colégio D. Pedro II" → "Colégio Dom Pedro II"
        else Confiança < 85%
            VE-->>VS: Sinalizar para revisão manual
            VS->>N: Notificar administrador
            N->>A: Email/Alerta: Nova entrada para revisar
        end
    end
    
    Note over PR,DB: Fase 3: Processamento do Registro
    VS-->>API: Resultado da validação
    API->>PR: Processar registro
    
    PR->>DB: Verificar duplicatas<br/>SELECT * FROM registrations<br/>WHERE email = 'estudante@email.com'
    DB-->>PR: Nenhuma duplicata encontrada
    
    PR->>DB: Inserir registro<br/>INSERT INTO registrations
    DB-->>PR: Registro salvo (ID: 12345)
    
    Note over PR,E: Fase 4: Confirmação
    PR->>N: Enviar confirmação
    N->>E: Email de confirmação enviado
    PR-->>API: Registro completo
    API-->>F: Status 201 Created
    F->>E: Exibe mensagem de sucesso
    
    Note over E,A: Fluxo Alternativo: Revisão Manual
    opt Se flagado para revisão manual
        A->>F: Acessa painel administrativo
        F->>API: GET /admin/pending-registrations
        API->>DB: SELECT * FROM registrations WHERE status = 'pending_review'
        DB-->>API: Lista de registros pendentes
        API-->>F: Dados para revisar
        F->>A: Exibe entrada do estudante
        A->>F: Aprova/Corrige escola manualmente
        F->>API: PUT /admin/registrations/12345
        API->>DB: UPDATE registrations SET school_id = X, status = 'approved'
        DB-->>API: Atualizado
        API->>N: Notificar estudante
        N->>E: Email: Registro aprovado
    end
```

[Link do primeiro protótipo](https://preview--olimpiada-ia-inscricao.lovable.app)
