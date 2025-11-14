-- Migration: 001_initial_schema.sql

CREATE TABLE IF NOT EXISTS escolas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    endereco TEXT,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL DEFAULT 'GO',
    cep VARCHAR(10),
    telefone VARCHAR(20),
    email VARCHAR(255),
    diretor_nome VARCHAR(255),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS estudantes (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    escola_id INTEGER NOT NULL REFERENCES escolas(id) ON DELETE RESTRICT,
    serie_ano VARCHAR(20) NOT NULL,
    turno VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inscricoes (
    id SERIAL PRIMARY KEY,
    estudante_id INTEGER NOT NULL REFERENCES estudantes(id) ON DELETE CASCADE,
    escola_id INTEGER NOT NULL REFERENCES escolas(id) ON DELETE RESTRICT,
    ano_edicao INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'pendente',
    categoria VARCHAR(100),
    equipe_nome VARCHAR(255),
    observacoes TEXT,
    data_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_confirmacao TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(estudante_id, ano_edicao)
);

CREATE TABLE IF NOT EXISTS equipes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    escola_id INTEGER NOT NULL REFERENCES escolas(id) ON DELETE RESTRICT,
    ano_edicao INTEGER NOT NULL,
    categoria VARCHAR(100),
    lider_id INTEGER REFERENCES estudantes(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'formando',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS equipe_membros (
    id SERIAL PRIMARY KEY,
    equipe_id INTEGER NOT NULL REFERENCES equipes(id) ON DELETE CASCADE,
    estudante_id INTEGER NOT NULL REFERENCES estudantes(id) ON DELETE CASCADE,
    papel VARCHAR(50) DEFAULT 'membro',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(equipe_id, estudante_id)
);
