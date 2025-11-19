// Types for API entities

export interface Escola {
  id: number;
  nome: string;
  cidade: string;
  estado: string;
  endereco?: string;
  cep?: string;
  telefone?: string;
  email?: string;
  diretor_nome?: string;
  ativo: boolean;
  created_at: string;
  updated_at: string;
}

export interface EscolaCreate {
  nome: string;
  cidade: string;
  estado?: string;
  endereco?: string;
  cep?: string;
  telefone?: string;
  email?: string;
  diretor_nome?: string;
  ativo?: boolean;
}

export interface Estudante {
  id: number;
  nome_completo: string;
  cpf: string;
  data_nascimento: string;
  email: string;
  escola_id: number;
  serie_ano: string;
  telefone?: string;
  turno?: string;
  created_at: string;
  updated_at: string;
}

export interface EstudanteCreate {
  nome_completo: string;
  cpf: string;
  data_nascimento: string;
  email: string;
  escola_id: number;
  serie_ano: string;
  telefone?: string;
  turno?: string;
}

export interface Inscricao {
  id: number;
  estudante_id: number;
  escola_id: number;
  ano_edicao: number;
  status: string;
  categoria?: string;
  equipe_nome?: string;
  observacoes?: string;
  data_inscricao: string;
  data_confirmacao?: string;
  created_at: string;
  updated_at: string;
}

export interface InscricaoCreate {
  estudante_id: number;
  escola_id: number;
  ano_edicao: number;
  categoria?: string;
  equipe_nome?: string;
  observacoes?: string;
}

