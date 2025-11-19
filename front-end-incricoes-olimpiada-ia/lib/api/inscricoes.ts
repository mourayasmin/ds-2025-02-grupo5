import { apiRequest } from './config';
import type { Inscricao, InscricaoCreate } from '@/types';

export async function getInscricoes(): Promise<Inscricao[]> {
  return apiRequest<Inscricao[]>(`/inscricoes`);
}

export async function getInscricaoById(id: number): Promise<Inscricao> {
  return apiRequest<Inscricao>(`/inscricoes/${id}`);
}

export async function createInscricao(inscricao: InscricaoCreate): Promise<Inscricao> {
  // Remove campos vazios opcionais antes de enviar
  const payload = Object.fromEntries(
    Object.entries(inscricao).filter(([_, value]) => value !== '' && value !== undefined)
  ) as InscricaoCreate;
  
  return apiRequest<Inscricao>('/inscricoes', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

