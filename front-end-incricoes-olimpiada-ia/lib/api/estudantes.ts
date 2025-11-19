import { apiRequest } from './config';
import type { Estudante, EstudanteCreate } from '@/types';

export async function getEstudantes(): Promise<Estudante[]> {
  return apiRequest<Estudante[]>(`/estudantes`);
}

export async function getEstudanteById(id: number): Promise<Estudante> {
  return apiRequest<Estudante>(`/estudantes/${id}`);
}

export async function getEstudanteByCpf(cpf: string): Promise<Estudante> {
  return apiRequest<Estudante>(`/estudantes/cpf/${cpf}`);
}

export async function getEstudantesByEscola(escolaId: number): Promise<Estudante[]> {
  return apiRequest<Estudante[]>(`/estudantes/escola/${escolaId}`);
}

export async function createEstudante(estudante: EstudanteCreate): Promise<Estudante> {
  // Remove campos vazios opcionais antes de enviar
  const payload = Object.fromEntries(
    Object.entries(estudante).filter(([_, value]) => value !== '' && value !== undefined)
  ) as EstudanteCreate;
  
  return apiRequest<Estudante>('/estudantes', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateEstudante(
  id: number,
  updates: Partial<EstudanteCreate>
): Promise<Estudante> {
  // Remove campos vazios opcionais antes de enviar
  const payload = Object.fromEntries(
    Object.entries(updates).filter(([_, value]) => value !== '' && value !== undefined)
  );
  
  return apiRequest<Estudante>(`/estudantes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

