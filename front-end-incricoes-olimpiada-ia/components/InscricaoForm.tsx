'use client';

import React, { useState, useEffect } from 'react';
import { Input } from './ui/Input';
import { Select } from './ui/Select';
import { Button } from './ui/Button';
import { Alert } from './ui/Alert';
import { getActiveEscolas, createEscola } from '@/lib/api/escolas';
import { getEstudanteByCpf, createEstudante, updateEstudante } from '@/lib/api/estudantes';
import { createInscricao } from '@/lib/api/inscricoes';
import type { Escola, Estudante } from '@/types';
import { useRouter } from 'next/navigation';

interface FormErrors {
  [key: string]: string;
}

export function InscricaoForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [checkingCpf, setCheckingCpf] = useState(false);
  const [alert, setAlert] = useState<{ type: 'success' | 'error' | 'info' | 'warning'; message: string } | null>(null);
  const [errors, setErrors] = useState<FormErrors>({});
  const [estudanteExistente, setEstudanteExistente] = useState<Estudante | null>(null);
  const [cpfVerificado, setCpfVerificado] = useState(false);

  // Escolas
  const [escolas, setEscolas] = useState<Escola[]>([]);
  const [escolaId, setEscolaId] = useState<string>('');
  const [criarNovaEscola, setCriarNovaEscola] = useState(false);
  const [escolaForm, setEscolaForm] = useState({
    nome: '',
    cidade: '',
    estado: 'GO',
    endereco: '',
    cep: '',
    telefone: '',
    email: '',
  });

  // Dados do Participante
  const [participanteForm, setParticipanteForm] = useState({
    cpf: '',
    nome_completo: '',
    data_nascimento: '',
    email: '',
    telefone: '',
    serie_ano: '',
    turno: '',
  });

  // Ano da edição hard coded
  const ANO_EDICAO = new Date().getFullYear();

  // Load escolas on mount
  useEffect(() => {
    loadEscolas();
  }, []);

  const loadEscolas = async () => {
    try {
      const data = await getActiveEscolas();
      setEscolas(data);
    } catch (error) {
      console.error('Erro ao carregar escolas:', error);
    }
  };

  const formatCPF = (value: string) => {
    const numbers = value.replace(/\D/g, '');
    if (numbers.length <= 11) {
      return numbers.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    }
    return value;
  };

  const formatCEP = (value: string) => {
    const numbers = value.replace(/\D/g, '');
    if (numbers.length <= 8) {
      return numbers.replace(/(\d{5})(\d{3})/, '$1-$2');
    }
    return value;
  };

  const formatTelefone = (value: string) => {
    const numbers = value.replace(/\D/g, '');
    if (numbers.length <= 10) {
      // Telefone fixo: (00) 0000-0000
      return numbers.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    } else if (numbers.length <= 11) {
      // Celular: (00) 00000-0000
      return numbers.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    }
    return value;
  };

  const validateCPF = (cpf: string): boolean => {
    const numbers = cpf.replace(/\D/g, '');
    return numbers.length === 11;
  };

  // Verificação automática de CPF quando tiver 11 dígitos
  useEffect(() => {
    const cpfLimpo = participanteForm.cpf.replace(/\D/g, '');
    
    // Só verifica se tiver 11 dígitos e não tiver verificado ainda
    if (cpfLimpo.length === 11 && !cpfVerificado && !checkingCpf) {
      const checkCpf = async () => {
        setCheckingCpf(true);
        setCpfVerificado(true);

        try {
          const estudante = await getEstudanteByCpf(cpfLimpo);
          setEstudanteExistente(estudante);
          setParticipanteForm({
            cpf: estudante.cpf,
            nome_completo: estudante.nome_completo,
            data_nascimento: estudante.data_nascimento,
            email: estudante.email,
            telefone: estudante.telefone ? formatTelefone(estudante.telefone) : '',
            serie_ano: estudante.serie_ano,
            turno: estudante.turno || '',
          });
          setEscolaId(estudante.escola_id.toString());
          setAlert({ type: 'success', message: 'Participante encontrado! Os dados foram preenchidos automaticamente.' });
        } catch (error: any) {
          if (error.message.includes('not found')) {
            setEstudanteExistente(null);
            // Não mostra alerta se não encontrou, apenas permite preencher
          } else {
            setAlert({ type: 'error', message: error.message || 'Erro ao verificar CPF' });
          }
        } finally {
          setCheckingCpf(false);
        }
      };

      // Debounce de 500ms para evitar muitas requisições
      const timeoutId = setTimeout(checkCpf, 500);
      return () => clearTimeout(timeoutId);
    }
  }, [participanteForm.cpf, cpfVerificado, checkingCpf]);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Validação da Escola
    if (estudanteExistente) {
      // Para estudante existente, apenas validar se escola foi selecionada
      if (!escolaId) {
        newErrors.escola_id = 'Selecione uma escola para esta inscrição';
      }
    } else {
      // Para novo estudante, validar escola normalmente
      if (criarNovaEscola) {
        if (!escolaForm.nome.trim()) newErrors.escola_nome = 'Nome da escola é obrigatório';
        if (!escolaForm.cidade.trim()) newErrors.escola_cidade = 'Cidade é obrigatória';
      } else {
        if (!escolaId) newErrors.escola_id = 'Selecione uma escola';
      }
    }

    // Validação do Participante
    if (!participanteForm.nome_completo.trim()) {
      newErrors.nome_completo = 'Nome completo é obrigatório';
    }
    if (!participanteForm.cpf.trim()) {
      newErrors.cpf = 'CPF é obrigatório';
    } else if (!validateCPF(participanteForm.cpf)) {
      newErrors.cpf = 'CPF deve conter 11 dígitos';
    }
    if (!participanteForm.data_nascimento) {
      newErrors.data_nascimento = 'Data de nascimento é obrigatória';
    }
    if (!participanteForm.email.trim()) {
      newErrors.email = 'Email é obrigatório';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(participanteForm.email)) {
      newErrors.email = 'Email inválido';
    }
    if (!participanteForm.serie_ano.trim()) {
      newErrors.serie_ano = 'Série/Ano é obrigatório';
    }


    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setAlert(null);

    try {
      // 1. Processar Escola
      let finalEscolaId: number;
      if (criarNovaEscola) {
        const novaEscola = await createEscola({
          nome: escolaForm.nome.trim(),
          cidade: escolaForm.cidade.trim(),
          estado: escolaForm.estado?.trim() || 'GO',
          endereco: escolaForm.endereco?.trim() || undefined,
          cep: escolaForm.cep?.replace(/\D/g, '') || undefined,
          telefone: escolaForm.telefone?.trim() || undefined,
          email: escolaForm.email?.trim() || undefined,
        });
        finalEscolaId = novaEscola.id;
        await loadEscolas();
      } else {
        finalEscolaId = parseInt(escolaId);
      }

      // 2. Processar Estudante
      let finalEstudanteId: number;
      
      if (estudanteExistente) {
        // Se estudante já existe, atualizar a escola dele para a escola selecionada
        // A relação escola-estudante é estabelecida no momento da inscrição
        finalEstudanteId = estudanteExistente.id;
        
        // Atualizar escola_id do estudante para a escola selecionada
        if (estudanteExistente.escola_id !== finalEscolaId) {
          await updateEstudante(estudanteExistente.id, {
            escola_id: finalEscolaId,
          });
        }
      } else {
        // Criar novo estudante com a escola selecionada
        const cpfLimpo = participanteForm.cpf.replace(/\D/g, '');
        const novoEstudante = await createEstudante({
          nome_completo: participanteForm.nome_completo.trim(),
          cpf: cpfLimpo,
          data_nascimento: participanteForm.data_nascimento,
          email: participanteForm.email.trim(),
          escola_id: finalEscolaId,
          serie_ano: participanteForm.serie_ano.trim(),
          telefone: participanteForm.telefone?.replace(/\D/g, '') || undefined,
          turno: participanteForm.turno || undefined,
        });
        finalEstudanteId = novoEstudante.id;
      }

      // 3. Criar Inscrição (a relação escola-estudante já foi estabelecida acima)
      await createInscricao({
        estudante_id: finalEstudanteId,
        escola_id: finalEscolaId,
        ano_edicao: ANO_EDICAO,
      });

      setAlert({ type: 'success', message: 'Inscrição realizada com sucesso! Você receberá um email de confirmação em breve.' });
      
      // Reset form
      setTimeout(() => { router.push('https://olimpiadaia.ceia.ai');
        setParticipanteForm({
          cpf: '',
          nome_completo: '',
          data_nascimento: '',
          email: '',
          telefone: '',
          serie_ano: '',
          turno: '',
        });
        setEscolaId('');
        setCriarNovaEscola(false);
        setEstudanteExistente(null);
        setCpfVerificado(false);
        setEscolaForm({
          nome: '',
          cidade: '',
          estado: 'GO',
          endereco: '',
          cep: '',
          telefone: '',
          email: '',
        });
      }, 3000);
    } catch (error: any) {
      console.error('Erro ao realizar inscrição:', error);
      let errorMessage = 'Erro ao realizar inscrição. Por favor, tente novamente.';
      
      if (error.message) {
        errorMessage = error.message;
        // Mensagens mais amigáveis para erros comuns
        if (error.message.includes('already exists')) {
          errorMessage = 'Você já possui uma inscrição para este ano.';
        } else if (error.message.includes('not found')) {
          errorMessage = 'Dados não encontrados. Por favor, verifique as informações e tente novamente.';
        } else if (error.message.includes('does not belong')) {
          errorMessage = 'O participante não pertence à escola selecionada. Por favor, verifique os dados.';
        }
      }
      
      setAlert({ type: 'error', message: errorMessage });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="bg-slate-800/80 backdrop-blur-sm rounded-xl shadow-2xl shadow-slate-900/50 border border-slate-700/50 p-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-slate-100 mb-2">Inscrição - Olimpíadas de IA</h1>
          <p className="text-slate-300">Preencha seus dados para participar das Olimpíadas de Inteligência Artificial</p>
        </div>

        {alert && (
          <Alert
            type={alert.type}
            message={alert.message}
            onClose={() => setAlert(null)}
          />
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Seção: Dados do Participante */}
          <div className="border-b border-slate-700/50 pb-6">
            <h2 className="text-xl font-semibold text-slate-100 mb-4">Dados do Participante</h2>
            
            <div className="space-y-4">
              <Input
                label="CPF"
                id="cpf"
                value={participanteForm.cpf}
                onChange={(e) => {
                  setParticipanteForm({ ...participanteForm, cpf: formatCPF(e.target.value) });
                  // Reset verificação quando CPF mudar
                  const cpfLimpo = e.target.value.replace(/\D/g, '');
                  if (cpfLimpo.length !== 11) {
                    setCpfVerificado(false);
                    setEstudanteExistente(null);
                  }
                }}
                placeholder="000.000.000-00"
                maxLength={14}
                error={errors.cpf}
                required
              />

              {checkingCpf && (
                <div className="text-sm text-slate-300 flex items-center gap-2">
                  <svg className="animate-spin h-4 w-4 text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Verificando CPF...
                </div>
              )}

              {estudanteExistente && (
                <div className="bg-blue-400/20 border border-blue-400/40 rounded-lg p-3 text-sm text-blue-200 backdrop-blur-sm">
                  ✓ Participante encontrado no sistema. Os dados foram preenchidos automaticamente. Selecione a escola para esta inscrição.
                </div>
              )}

              <Input
                label="Nome Completo"
                id="nome_completo"
                value={participanteForm.nome_completo}
                onChange={(e) => setParticipanteForm({ ...participanteForm, nome_completo: e.target.value })}
                error={errors.nome_completo}
                required
              />

              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="Data de Nascimento"
                  id="data_nascimento"
                  type="date"
                  value={participanteForm.data_nascimento}
                  onChange={(e) => setParticipanteForm({ ...participanteForm, data_nascimento: e.target.value })}
                  error={errors.data_nascimento}
                  required
                />
                <Input
                  label="Email"
                  id="email"
                  type="email"
                  value={participanteForm.email}
                  onChange={(e) => setParticipanteForm({ ...participanteForm, email: e.target.value })}
                  error={errors.email}
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="Telefone"
                  id="telefone"
                  value={participanteForm.telefone}
                  onChange={(e) => setParticipanteForm({ ...participanteForm, telefone: formatTelefone(e.target.value) })}
                  placeholder="(00) 00000-0000"
                  maxLength={15}
                />
                <Select
                  label="Turno"
                  id="turno"
                  value={participanteForm.turno}
                  onChange={(e) => setParticipanteForm({ ...participanteForm, turno: e.target.value })}
                  options={[
                    { value: 'manha', label: 'Manhã' },
                    { value: 'tarde', label: 'Tarde' },
                    { value: 'noite', label: 'Noite' },
                    { value: 'integral', label: 'Integral' },
                  ]}
                />
              </div>

              <Select
                label="Série/Ano Escolar"
                id="serie_ano"
                value={participanteForm.serie_ano}
                onChange={(e) => setParticipanteForm({ ...participanteForm, serie_ano: e.target.value })}
                error={errors.serie_ano}
                required
                options={[
                  { value: '9° ano do ensino fundamental', label: '9° ano do ensino fundamental' },
                  { value: 'primeiro ano do ensino médio', label: 'Primeiro ano do ensino médio' },
                  { value: 'segundo ano do ensino médio', label: 'Segundo ano do ensino médio' },
                  { value: 'terceiro ano do ensino médio', label: 'Terceiro ano do ensino médio' },
                ]}
              />
            </div>
          </div>

          {/* Seção: Escola */}
          <div className="border-b border-slate-700/50 pb-6">
            <h2 className="text-xl font-semibold text-slate-100 mb-4">Escola</h2>
            
            {estudanteExistente ? (
              <div className="space-y-2">
                <div className="bg-blue-400/20 border border-blue-400/40 rounded-lg p-3 text-sm text-blue-200 backdrop-blur-sm">
                  <p className="font-medium mb-1">Participante encontrado</p>
                  <p className="text-xs text-blue-200/80">Você pode selecionar a escola para esta inscrição. A relação será estabelecida no momento da inscrição.</p>
                </div>
                <Select
                  label="Selecione a Escola para esta Inscrição"
                  id="escola_id"
                  value={escolaId}
                  onChange={(e) => setEscolaId(e.target.value)}
                  options={escolas.map((e) => ({ value: e.id.toString(), label: `${e.nome} - ${e.cidade}/${e.estado}` }))}
                  error={errors.escola_id}
                  required
                />
              </div>
            ) : (
              <>
                <div className="mb-4">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={!criarNovaEscola}
                      onChange={(e) => setCriarNovaEscola(!e.target.checked)}
                      className="rounded w-4 h-4 text-blue-400 bg-slate-700/50 border-slate-600 focus:ring-blue-400/50 focus:ring-2"
                    />
                    <span className="text-sm text-slate-200">Minha escola já está cadastrada</span>
                  </label>
                </div>

                {!criarNovaEscola ? (
                  <Select
                    label="Selecione sua Escola"
                    id="escola_id"
                    value={escolaId}
                    onChange={(e) => setEscolaId(e.target.value)}
                    options={escolas.map((e) => ({ value: e.id.toString(), label: `${e.nome} - ${e.cidade}/${e.estado}` }))}
                    error={errors.escola_id}
                    required
                  />
                ) : (
              <div className="space-y-4">
                <Input
                  label="Nome da Escola"
                  id="escola_nome"
                  value={escolaForm.nome}
                  onChange={(e) => setEscolaForm({ ...escolaForm, nome: e.target.value })}
                  error={errors.escola_nome}
                  required
                />
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="Cidade"
                    id="escola_cidade"
                    value={escolaForm.cidade}
                    onChange={(e) => setEscolaForm({ ...escolaForm, cidade: e.target.value })}
                    error={errors.escola_cidade}
                    required
                  />
                  <Input
                    label="Estado"
                    id="escola_estado"
                    value={escolaForm.estado}
                    onChange={(e) => setEscolaForm({ ...escolaForm, estado: e.target.value.toUpperCase() })}
                    maxLength={2}
                    placeholder="GO"
                  />
                </div>
                <Input
                  label="Endereço"
                  id="escola_endereco"
                  value={escolaForm.endereco}
                  onChange={(e) => setEscolaForm({ ...escolaForm, endereco: e.target.value })}
                />
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="CEP"
                    id="escola_cep"
                    value={escolaForm.cep}
                    onChange={(e) => setEscolaForm({ ...escolaForm, cep: formatCEP(e.target.value) })}
                    maxLength={9}
                    placeholder="00000-000"
                  />
                  <Input
                    label="Telefone da Escola"
                    id="escola_telefone"
                    value={escolaForm.telefone}
                    onChange={(e) => setEscolaForm({ ...escolaForm, telefone: e.target.value })}
                  />
                </div>
                <Input
                  label="Email da Escola"
                  id="escola_email"
                  type="email"
                  value={escolaForm.email}
                  onChange={(e) => setEscolaForm({ ...escolaForm, email: e.target.value })}
                />
              </div>
                )}
              </>
            )}
          </div>

          {/* Botão de Submit */}
          <div className="flex justify-end pt-4 border-t border-slate-700/50">
            <Button type="submit" isLoading={loading} className="min-w-[200px]">
              Finalizar Inscrição
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
