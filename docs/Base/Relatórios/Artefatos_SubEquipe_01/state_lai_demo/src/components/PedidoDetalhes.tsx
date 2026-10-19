import { useState } from 'react';
import { PedidoContext, RascunhoState, RespondidoState } from './motor_state';

const ORGAOS = [
  'Controladoria-Geral da União (CGU)',
  'Ministério da Saúde',
  'Ministério da Educação',
  'Instituto Nacional do Seguro Social (INSS)',
  'Receita Federal do Brasil',
];

const PROTOCOLO = '00075.004218/2026-31';

const fieldBase =
  'w-full rounded-md border px-3.5 py-2.5 text-base transition focus:outline-none focus-visible:ring-4 focus-visible:ring-gov-blue/25';
const fieldEnabled = 'border-gov-muted bg-white text-gov-ink hover:border-gov-blue focus:border-gov-blue';
const fieldLocked = 'cursor-not-allowed border-gov-line bg-slate-100 text-gov-muted opacity-80';

export default function PedidoDetalhes() {
  // 1. INICIANDO OS BASTIDORES (O Motor GoF State)
  const [pedido] = useState(() => new PedidoContext(new RascunhoState()));
  const [faseAtual, setFaseAtual] = useState(pedido.getStatus());

  // 2. ESTADOS VISUAIS DA TELA
  const [orgao, setOrgao] = useState(ORGAOS[1]);
  const [descricao, setDescricao] = useState(
    'Solicito a relação de contratos firmados para aquisição de insumos hospitalares entre janeiro de 2024 e dezembro de 2025, com valores, fornecedores e datas de vigência.',
  );
  const [arquivos, setArquivos] = useState<string[]>([]);
  const [dragging, setDragging] = useState(false);

  // 3. REGRAS DE EXIBIÇÃO BASEADAS NO MOTOR
  const isDraft = faseAtual === 'draft';
  const isAnalysis = faseAtual === 'analysis';
  const isAnswered = faseAtual === 'answered';
  const locked = !isDraft;

  // 4. AÇÕES QUE ACIONAM O PADRÃO STATE
  const handleEnviar = (e: React.FormEvent) => {
    e.preventDefault();
    pedido.enviar(); // Motor valida a transição para Em Análise
    setFaseAtual(pedido.getStatus()); // Tela se atualiza automaticamente
  };

  const handleCancelar = () => {
    pedido.cancelar(); // Executa o cancelamento dentro da classe de estado
    alert("Protocolo cancelado pelo cidadão.");
  };

  const handleRecorrer = () => {
    pedido.recorrer(); // Motor valida o recurso e volta para Análise
    setFaseAtual(pedido.getStatus());
  };

  // Atalho oculto apenas para demonstração (simula o órgão respondendo)
  const simularRespostaGoverno = () => {
    pedido.setEstado(new RespondidoState());
    setFaseAtual(pedido.getStatus());
  };

  const addFiles = (list: FileList | null) => {
    if (!list) return;
    setArquivos((prev) => [...prev, ...Array.from(list).map((f) => f.name)]);
  };

  return (
    <article
      className="mx-auto w-full max-w-3xl p-6"
      aria-labelledby="pedido-titulo"
      data-state={faseAtual}
    >
      {/* Cabeçalho do protocolo */}
      <header className="mb-6 flex justify-between items-center">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wider text-gov-blue text-blue-600">
            Lei de Acesso à Informação · Pedido
          </p>
          <h1 id="pedido-titulo" className="mt-1 font-serif text-3xl font-bold text-gov-ink text-slate-800">
            {isDraft ? 'Novo pedido de informação' : `Protocolo ${PROTOCOLO}`}
          </h1>
        </div>
        {/* Botão de Demonstração (Para mostrar o estado final na apresentação) */}
        {isAnalysis && (
          <button onClick={simularRespostaGoverno} className="text-xs bg-slate-200 hover:bg-slate-300 text-slate-700 py-1 px-3 rounded">
            Simular Resposta (Demo)
          </button>
        )}
      </header>

      {/* Banner de status: Em Análise */}
      {isAnalysis && (
        <section
          role="status"
          className="mb-6 rounded-lg border border-amber-400 border-l-8 bg-amber-50 p-5"
        >
          <div className="flex items-center gap-3">
            <h2 className="text-lg font-bold text-amber-950">Status: Em Análise</h2>
          </div>
          <div className="mt-4">
            <div className="mb-1.5 flex justify-between text-sm font-medium text-amber-950">
              <span>Prazo legal: Faltam 18 dias</span>
              <span>12 de 30 dias</span>
            </div>
            <div className="h-3 overflow-hidden rounded-full bg-amber-200">
              <div className="h-full w-[40%] rounded-full bg-amber-600" />
            </div>
          </div>
        </section>
      )}

      {/* Banner de status: Respondido */}
      {isAnswered && (
        <section
          role="status"
          className="mb-6 flex items-center gap-3 rounded-lg border border-emerald-500 border-l-8 bg-emerald-50 p-5"
        >
          <h2 className="text-lg font-bold text-emerald-950">Status: Pedido Respondido</h2>
        </section>
      )}

      {/* Formulário */}
      <form
        onSubmit={handleEnviar}
        className="rounded-lg border border-slate-200 bg-white shadow-sm"
      >
        <div className="space-y-6 p-6 sm:p-8">
          <div>
            <label htmlFor="orgao" className="mb-1.5 block text-sm font-semibold">
              Órgão Destinatário
            </label>
            <select
              id="orgao"
              value={orgao}
              disabled={locked}
              onChange={(e) => setOrgao(e.target.value)}
              className={`${fieldBase} ${locked ? fieldLocked : fieldEnabled}`}
            >
              {ORGAOS.map((o) => (
                <option key={o}>{o}</option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="descricao" className="mb-1.5 block text-sm font-semibold">
              Descrição da Solicitação
            </label>
            <textarea
              id="descricao"
              rows={7}
              value={descricao}
              disabled={locked}
              onChange={(e) => setDescricao(e.target.value)}
              className={`${fieldBase} resize-y ${locked ? fieldLocked : fieldEnabled}`}
            />
          </div>
        </div>

        {/* Rodapé de ação */}
        <footer className="flex justify-end border-t border-slate-200 bg-slate-50 px-6 py-4 sm:px-8">
          {isDraft && (
            <button
              type="submit"
              className="rounded-full bg-blue-600 px-8 py-2.5 font-semibold text-white transition hover:bg-blue-700"
            >
              Enviar Pedido
            </button>
          )}
          {isAnalysis && (
            <button
              type="button"
              onClick={handleCancelar}
              className="rounded-full border-2 border-blue-600 bg-white px-8 py-2 font-semibold text-blue-600 transition hover:bg-blue-50"
            >
              Cancelar Pedido
            </button>
          )}
          {isAnswered && (
            <button
              type="button"
              onClick={handleRecorrer}
              className="rounded-full bg-blue-600 px-8 py-2.5 font-semibold text-white transition hover:bg-blue-700"
            >
              Entrar com Recurso
            </button>
          )}
        </footer>
      </form>

      {/* Card de leitura: resposta do órgão */}
      {isAnswered && (
        <section className="mt-6 rounded-lg border border-slate-200 border-t-4 border-t-blue-600 bg-white p-6 shadow-sm sm:p-8">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h2 className="font-serif text-xl font-bold">Resposta do Órgão</h2>
            <p className="text-sm text-slate-500">{orgao} · respondido em 14/10/2026</p>
          </div>
          <div className="mt-4 space-y-3 text-base leading-relaxed text-slate-700">
            <p>Prezado(a) solicitante,</p>
            <p>
              Em atenção ao pedido registrado sob o protocolo {PROTOCOLO}, informamos que foram
              localizados contratos totalizando R$ 128,4 milhões. A relação completa
              segue na planilha anexa.
            </p>
            <p>Caso discorde da resposta, é possível apresentar recurso em até 10 dias.</p>
          </div>
        </section>
      )}
    </article>
  );
}