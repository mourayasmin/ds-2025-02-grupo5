import { apiRequest } from './config';
import type { Escola, EscolaCreate } from '@/types';

export async function getEscolas(): Promise<Escola[]> {
  return apiRequest<Escola[]>(`/escolas`);
}

export async function getEscolaById(id: number): Promise<Escola> {
  return apiRequest<Escola>(`/escolas/${id}`);
}

export async function getEscolasByCidade(cidade: string): Promise<Escola[]> {
  return apiRequest<Escola[]>(`/escolas/cidade/${encodeURIComponent(cidade)}`);
}

export async function getActiveEscolas(): Promise<Escola[]> {
  return apiRequest<Escola[]>(`/escolas/status/active`);
}

export async function createEscola(escola: EscolaCreate): Promise<Escola> {
  // Remove campos vazios opcionais antes de enviar
  const payload = Object.fromEntries(
    Object.entries(escola).filter(([_, value]) => value !== '' && value !== undefined)
  ) as EscolaCreate;
  
  return apiRequest<Escola>('/escolas', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

