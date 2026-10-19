'use strict';

const ESTADOS = ['REGISTRADO', 'EM_ANALISE', 'RESPONDIDO', 'AUTORIZADO', 'PUBLICADO'];
const RESPOSTA_PADRAO = 'Em resposta ao pedido, informamos que os dados demonstrativos estão disponíveis para consulta nesta simulação.';
const NOMES_ETAPAS = ['Registro', 'Análise', 'Resposta', 'Autorização', 'Publicação'];
const TITULOS_ESTADO = {
  REGISTRADO: 'Registrado', EM_ANALISE: 'Em análise', RESPONDIDO: 'Respondido',
  AUTORIZADO: 'Autorizado', PUBLICADO: 'Publicado',
};
const TITULOS_OBS = {busca: 'BuscaLAI', dados: 'Dados Abertos', painel: 'Painel LAI'};
const DESC_OBS = {
  busca: 'Indexação pública simulada',
  dados: 'Exportação de metadados',
  painel: 'Indicadores estatísticos',
};
const ICONES = {busca: '⌕', dados: '▥', painel: '▥'};
const ACOES = [
  {destino: 'EM_ANALISE', titulo: 'Iniciar análise'},
  {destino: 'RESPONDIDO', titulo: 'Registrar resposta'},
  {destino: 'AUTORIZADO', titulo: 'Autorizar publicação'},
  {destino: 'PUBLICADO', titulo: 'Publicar registros simulados'},
];
let estado = null;
let fontes = null;
let selecionada = 'SujeitoPedidoLAI';
let ocupado = false;
let replayId = 0;
let toastTimeout;
const $ = (seletor) => document.querySelector(seletor);
const $$ = (seletor) => [...document.querySelectorAll(seletor)];
const esc = (valor) => String(valor ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

async function api(rota, dados) {
  const opts = dados === undefined ? {} : {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(dados)};
  const res = await fetch(rota, opts);
  const json = await res.json();
  if (!res.ok) throw new Error(json.erro || 'Falha ao executar a operação.');
  return json;
}
function aviso(mensagem) {
  const toast = $('#toast');
  toast.textContent = mensagem;
  toast.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => toast.classList.remove('show'), 4600);
}
async function executar(rota, dados={}) {
  if (ocupado) return;
  ocupado = true;
  replayId++;
  try {
    estado = await api(rota, dados);
    renderTudo();
    if ($('#tab-fluxo').classList.contains('active')) reproduzir();
  } catch (e) { aviso(e.message); }
  finally { ocupado = false; if (fontes && estado) renderInspetor(); }
}
function indice() { return estado?.pedido ? ESTADOS.indexOf(estado.pedido.estado) + 1 : 0; }
function renderResumo() {
  const idx = indice();
  $('#stage-line').innerHTML = NOMES_ETAPAS.map((nome, i) => {
    const classe = i < idx ? 'done' : i === idx ? 'now' : '';
    return `<div class="stage-circle ${classe}"><b>${i < idx ? '✓' : i+1}</b><small>${nome}</small></div>`;
  }).join('');
}
function renderWorkflow() {
  const pedido = estado.pedido;
  $('#create-section').hidden = !!pedido;
  $('#advance-section').hidden = !pedido;
  if (!pedido) return;
  $('#request-subject').textContent = pedido.assunto;
  $('#request-orgao').textContent = pedido.orgao;
  $('#request-status').textContent = TITULOS_ESTADO[pedido.estado];
  const idx = indice();
  const container = $('#stage-actions');
  container.innerHTML = ACOES.map((acao, index) => {
    const alvo = index+2;
    const feito = idx >= alvo;
    const atual = idx === alvo-1;
    return `<div class="action-row ${feito?'complete':atual?'current':'pending'}">
      <span class="count">${feito?'✓':String(index+2).padStart(2,'0')}</span>
      <div class="action-text"><strong>${acao.titulo}</strong></div>
      <button type="button" data-avancar="${acao.destino}" ${!atual?'disabled':''}>${feito?'Feito':atual?'Executar →':'Aguardar'}</button>
      ${atual && acao.destino==='RESPONDIDO' ? '<div class="answer-input"><textarea id="resposta" rows="3" maxlength="500" placeholder="Resposta fictícia" aria-label="Resposta fictícia">${RESPOSTA_PADRAO}</textarea></div>' : ''}
    </div>`;
  }).join('');
  $$('[data-avancar]').forEach(button => button.addEventListener('click', () => {
    const resposta = $('#resposta')?.value || '';
    executar('/api/avancar', {etapa: button.dataset.avancar, resposta});
  }));
}
function obsResultado(chave, o) {
  if (!o.ativo) return {
    principal: 'Notificações desativadas',
    detalhe: 'A classe só consulta o pedido quando estiver inscrita e receber uma notificação.',
  };
  if (chave === 'busca') {
    if (o.registros.length) return {
      principal: 'Indexação concluída',
      detalhe: 'Após a publicação autorizada, consulta o pedido e indexa um registro público sintético.',
    };
    return {
      principal: 'Aguardando notificação (pedido autorizado e publicado)',
      detalhe: 'Consulta o pedido a cada aviso, mas só indexa registros após a publicação autorizada.',
    };
  }
  if (chave === 'dados') {
    if (o.registros.length) return {
      principal: 'Exportação concluída',
      detalhe: 'Após a publicação autorizada, consulta o pedido e exporta somente metadados públicos.',
    };
    return {
      principal: 'Aguardando notificação (pedido autorizado e publicado)',
      detalhe: 'Consulta o pedido a cada aviso, mas só exporta metadados após a publicação autorizada.',
    };
  }
  if (o.ultima_revisao > 0) return {
    principal: `Indicadores atualizados (${TITULOS_ESTADO[o.situacao] || 'Sem pedido'})`,
    detalhe: 'A cada notificação, consulta o pedido e atualiza os indicadores de registro, resposta e publicação.',
  };
  return {
    principal: 'Aguardando notificação (criação ou alteração do pedido)',
    detalhe: 'Quando o pedido for criado ou mudar de estado, consulta o sujeito e atualiza os indicadores.',
  };
}
function renderObservadores() {
  const el = $('#observer-cards');
  el.innerHTML = Object.entries(estado.observadores).map(([chave, o]) => {
    const resultado = obsResultado(chave, o);
    return `<article class="obs-card" data-obs="${chave}" data-class="${o.classe}">
      <div class="obs-card-top">
        <div class="obs-symbol">${ICONES[chave]}</div>
        <div class="obs-ident"><span class="obs-type">CLASSE · OBSERVADOR CONCRETO</span><h3>${TITULOS_OBS[chave]}</h3><small>${esc(o.classe)}</small></div>
        <button class="observer-toggle ${o.ativo ? 'is-active' : 'is-inactive'}" type="button" data-toggle="${chave}" aria-pressed="${o.ativo}" aria-label="${o.ativo ? 'Desativar' : 'Ativar'} ${TITULOS_OBS[chave]}" title="${o.ativo ? 'Cancelar inscrição' : 'Inscrever observador'}">
          <span class="toggle-track" aria-hidden="true"><span class="toggle-knob"></span></span><span class="toggle-text">${o.ativo ? 'ATIVO' : 'INATIVO'}</span>
        </button>
      </div>
      <div class="obs-card-main"><div class="obs-result"><div class="obs-result-label">CONDIÇÃO DE ATUALIZAÇÃO</div><strong>${esc(resultado.principal)}</strong><small>${esc(resultado.detalhe)}</small></div></div>
    </article>`;
  }).join('');
}
function renderEventos() {
  const lista = $('#trace-list');
  const chamadas = estado.ultima_execucao.filter(e =>
    e.categoria !== 'efeito' && e.metodo !== 'notificar() → atualizar()'
  );
  if (!chamadas.length) {
    lista.innerHTML = '<div class="trace-empty"><strong>Nenhuma chamada ainda</strong><small>Crie um pedido para visualizar a sequência.</small></div>';
    return;
  }
  let observadorAtual = '';
  lista.innerHTML = chamadas.map((e, i) => {
    if (e.categoria === 'observador') observadorAtual = e.classe;
    const relacionado = e.categoria === 'consulta' ? observadorAtual : e.classe;
    const nivel = e.categoria === 'consulta' ? 2 : e.categoria === 'observador' ? 1 : 0;
    return `<div class="call-row depth-${nivel}" data-seq="${i}" data-classe="${esc(relacionado)}" data-kind="${esc(e.categoria)}">
      <span class="call-index">${String(i + 1).padStart(2, '0')}</span>
      <span class="call-rail" aria-hidden="true">${nivel === 2 ? '↳' : nivel === 1 ? '→' : '●'}</span>
      <span class="call-code"><span class="call-class">${esc(e.classe)}</span><span class="call-method">.${esc(e.metodo)}</span></span>
    </div>`;
  }).join('');
}
function renderClasses() {
  if (!fontes) return;
  const ordemDesejada = ['Sujeito', 'SujeitoPedidoLAI', 'Observador', 'ObservadorBuscaLAI', 'ObservadorDadosAbertos', 'ObservadorPainelLAI', 'FonteEstadoPedido', 'PedidoLAI', 'Etapa'];
  const nomes = ordemDesejada.filter((nome) => nome in fontes && nome !== 'MotorSimulacao');
  if (!nomes.includes(selecionada)) selecionada = nomes[0] ?? 'SujeitoPedidoLAI';
  $('#class-count').textContent = nomes.length;
  $('#class-list').innerHTML = nomes.map(nome => `<button class="class-list-item ${nome===selecionada?'selected':''}" data-select-class="${nome}"><strong>${nome}</strong><small>${esc(fontes[nome].rotulo)}</small></button>`).join('');
  $$('[data-select-class]').forEach(el => el.addEventListener('click',()=>escolherClasse(el.dataset.selectClass)));
  $$('[data-class].arch-node').forEach(el => {
    el.classList.toggle('selected', el.dataset.class === selecionada);
    el.onclick=()=>escolherClasse(el.dataset.class);
  });
  const fonte = fontes[selecionada];
  $('#code-name').textContent = fonte.nome;
  $('#code-hierarchy').textContent = `${fonte.arquivo} · ${fonte.herda.length ? `Herda de ${fonte.herda.join(', ')}` : fonte.rotulo}`;
  $('#code-lines').replaceChildren();
  const linhas = fonte.codigo.replace(/\n$/, '').split('\n');
  linhas.forEach((codigo, idx)=>{
    const line=document.createElement('div'); line.className='code-line';
    const num=document.createElement('span'); num.className='code-lineno';num.textContent=String(idx+1).padStart(2,'0');
    const text=document.createElement('span');text.className='code-txt';text.textContent=codigo;
    line.append(num,text);$('#code-lines').append(line);
  });
  renderInspetor();
}
function escolherClasse(nome){selecionada=nome;renderClasses();}
function props(linhas){return linhas.map(([titulo,valor])=>`<div class="property"><span>${esc(titulo)}</span><strong>${esc(valor)}</strong></div>`).join('');}
function renderInspetor(){
  if(!fontes||!estado)return;
  const pedido=estado.pedido;
  const etapaAtual = indice();
  const etapaVisivel = pedido ? TITULOS_ESTADO[pedido.estado] : 'Pedido não criado';
  $('#audit-step').textContent = `Etapa ${etapaAtual} de ${ESTADOS.length} · ${etapaVisivel}`;
  const acaoSeguinte = !pedido
    ? {titulo: 'Criar pedido'}
    : ACOES.find(acao => ESTADOS.indexOf(acao.destino) === etapaAtual);
  const botaoAuditoria = $('#audit-next');
  const pedidoConcluido = pedido?.estado === 'PUBLICADO';
  botaoAuditoria.hidden = pedidoConcluido;
  botaoAuditoria.disabled = ocupado || !acaoSeguinte;
  botaoAuditoria.textContent = ocupado ? 'Executando…' : acaoSeguinte ? `${acaoSeguinte.titulo} →` : 'Pedido concluído';
  const botaoReiniciar = $('#audit-reset');
  $('#audit-control-label').textContent = pedidoConcluido ? 'PEDIDO CONCLUÍDO' : 'PRÓXIMA ETAPA';
  botaoReiniciar.hidden = !pedidoConcluido;
  botaoReiniciar.disabled = ocupado;
  $('#audit-next-hint').textContent = pedidoConcluido
    ? 'Pedido concluído. Reiniciar apagará o estado atual para uma nova execução.'
    : 'O próximo passo atualizará os objetos e os valores desta auditoria.';
  let linhas=[];
  let descricao='';
  switch(selecionada){
    case 'Sujeito':
      descricao='Classe abstrata: não possui instância própria. Os dados exibidos pertencem ao sujeito concreto em execução.';
      linhas=[['Métodos definidos','adicionar(), remover(), notificar()'],['Instância própria','Não: classe abstrata']];break;
    case 'SujeitoPedidoLAI':
      descricao='Instância de SujeitoPedidoLAI: mantém o pedido atual e avisa seus observadores quando ocorre uma mudança.';
      linhas=[['Protocolo',pedido?.protocolo||'Não criado'],['Estado',pedido?.estado||'Sem pedido'],['Revisão',pedido?.revisao||'—'],['Observadores inscritos',Object.values(estado.observadores).filter(observador=>observador.ativo).length],['Chamadas de getEstado()',estado.total_consultas]];break;
    case 'FonteEstadoPedido':
      descricao='Contrato de leitura: os observadores consultam uma fonte de estado por uma abstração, sem depender da classe concreta do sujeito.';
      linhas=[['Método definido','getEstado()'],['Instância própria','Não: contrato abstrato'],['Implementação em uso','SujeitoPedidoLAI']];break;
    case 'Observador':
      descricao='Classe abstrata: não possui instância própria. Os valores abaixo resumem o contrato usado pelos objetos observadores.';
      linhas=[['Método definido','atualizar()'],['Instância própria','Não: classe abstrata'],['Classes concretas','3']];break;
    case 'Etapa':
      descricao='Enumeração dos estados válidos de um pedido. Cada transição segue a ordem definida pelo sujeito concreto.';
      linhas=[['Estados possíveis',ESTADOS.join(', ')],['Estado atual',pedido?.estado||'Nenhum']];break;
    case 'MotorSimulacao':
      descricao='Orquestrador: mantém o sujeito, registra as chamadas e conecta as operações do pedido à interface.';
      linhas=[['Instâncias de observadores',Object.keys(estado.observadores).length],['Última etapa',pedido?.estado||'Sem pedido'],['Chamadas registradas',estado.eventos.length],['Observadores inscritos',Object.values(estado.observadores).filter(item=>item.ativo).length]];break;
    case 'PedidoLAI':
      descricao='Objeto de dados do pedido: os campos abaixo correspondem à revisão atual armazenada no sujeito.';
      linhas=[['Assunto',pedido?.assunto||'—'],['Órgão',pedido?.orgao||'—'],['Etapa',pedido?.estado||'—'],['Revisão',pedido?.revisao||'—'],['Publicação autorizada?',pedido?.autorizado?'Sim':'Não']];break;
    default:{
      const [chave, o] = Object.entries(estado.observadores).find(([_,o])=>o.classe===selecionada)||[];
      descricao='Instância concreta: recebe atualizar(), consulta getEstado() e reage de acordo com sua responsabilidade.';
      linhas=[['Inscrito nas notificações?',o?.ativo?'Sim':'Não'],['Total de consultas ao pedido',o?.consultas??0],['Última revisão consultada',o?.ultima_revisao||'—']];
      if (chave==='busca') linhas.push(['Registros indexados',o.registros.length],['Protocolo indexado',o.registros[0]?.protocolo||'—']);
      if (chave==='dados') linhas.push(['Registros exportados',o.registros.length],['Situação exportada',o.registros[0]?.situacao||'—']);
      if (chave==='painel') linhas.push(['Pedidos registrados',o.registrados],['Pedidos respondidos',o.respondidos],['Pedidos publicados',o.publicados],['Estado visualizado',o.situacao]);
      break;
    }
  }
  $('#inspector').innerHTML=`<div class="inspector-details"><p class="audit-class-name">${esc(selecionada)}</p><p class="inspector-lead">${esc(descricao)}</p>${props(linhas)}</div>`;
}
function renderTudo(){
  if(!estado)return;
  renderResumo(); renderWorkflow(); renderObservadores(); renderEventos(); renderClasses();
}
async function reproduzir(){
  const id=++replayId;
  const chamadas=$$('[data-seq]');
  if (!chamadas.length) return;
  for (const e of chamadas) {
    if (id!==replayId) return;
    $$('[data-seq]').forEach(el=>el.classList.remove('highlight'));
    $$('.obs-card').forEach(el=>el.classList.remove('active-call'));
    e.classList.add('highlight');
    e.scrollIntoView({block:'nearest',behavior:'smooth'});
    const classe=e.dataset.classe;
    $$('.obs-card').filter(el=>el.dataset.class===classe).forEach(el=>el.classList.add('active-call'));
    await new Promise(resolve=>setTimeout(resolve,420));
  }
  if(id===replayId){$$('[data-seq]').forEach(el=>el.classList.remove('highlight'));$$('.obs-card').forEach(el=>el.classList.remove('active-call'));}
}
async function avancarPelaAuditoria(){
  if (ocupado || !estado) return;
  const botao = $('#audit-next');
  botao.disabled = true;
  botao.textContent = 'Executando…';
  const etapaAtual = indice();
  if (!estado.pedido) {
    await executar('/api/criar', {
      assunto: $('#field-assunto').value,
      orgao: $('#field-orgao').value,
      descricao: $('#field-descricao').value,
    });
  } else {
    const proximaAcao = ACOES.find(acao => ESTADOS.indexOf(acao.destino) === etapaAtual);
    if (proximaAcao) {
      const resposta = $('#resposta')?.value || RESPOSTA_PADRAO;
      await executar('/api/avancar', {etapa: proximaAcao.destino, resposta});
    }
  }
  renderInspetor();
}
function mudarAba(aba){
  $$('[data-tab]').forEach(el=>{
    const active=el.dataset.tab===aba;
    if(el.classList.contains('nav-item')){el.classList.toggle('selected',active);if(active)el.setAttribute('aria-current','page');else el.removeAttribute('aria-current');}
    if(el.classList.contains('tab-button')){el.classList.toggle('active',active);el.setAttribute('aria-selected',String(active));}
  });
  $$('.tab-content').forEach(el=>el.classList.toggle('active',el.id===`tab-${aba}`));
  if (aba==='classes')renderClasses();
  $('#help-button-text').textContent = aba === 'classes' ? 'Como ler o código' : 'Entenda o fluxo';
}
let focoAntesModal = null;
function abrirFuncionamento() {
  const abaClasses = $('#tab-classes').classList.contains('active');
  $('#help-flow-content').hidden = abaClasses;
  $('#help-classes-content').hidden = !abaClasses;
  $('#help-kicker').textContent = abaClasses ? 'GUIA DAS CLASSES' : 'GUIA DA SIMULAÇÃO';
  $('#help-title').textContent = abaClasses ? 'Como ler o código' : 'Entenda o fluxo';
  focoAntesModal = document.activeElement;
  $('#help-modal').hidden = false;
  document.body.classList.add('modal-open');
  $('#close-help').focus();
}
function fecharFuncionamento() {
  $('#help-modal').hidden = true;
  document.body.classList.remove('modal-open');
  focoAntesModal?.focus();
}
async function iniciar(){
  $$('[data-tab]').forEach(el=>el.addEventListener('click',()=>mudarAba(el.dataset.tab)));
  $('#create-form').addEventListener('submit',(event)=>{
    event.preventDefault();
    executar('/api/criar',{
      assunto:$('#field-assunto').value,
      orgao:$('#field-orgao').value,
      descricao:$('#field-descricao').value,
    });
  });
  $('#observer-cards').addEventListener('click', async event => {
    const botao = event.target.closest('button[data-toggle]');
    if (!botao) return;
    if (ocupado) {
      aviso('Aguarde a conclusão da operação anterior.');
      return;
    }
    const chave = botao.dataset.toggle;
    const novoEstado = !estado.observadores[chave].ativo;
    botao.disabled = true;
    botao.classList.add('is-pending');
    botao.querySelector('.toggle-text').textContent = 'AGUARDE';
    await executar('/api/assinatura', {observador: chave, ativo: novoEstado});
    if (botao.isConnected) renderObservadores();
  });
  $('#reset').addEventListener('click',()=>executar('/api/resetar'));
  $('#replay').addEventListener('click',reproduzir);
  $('#audit-next').addEventListener('click', avancarPelaAuditoria);
  $('#audit-reset').addEventListener('click', () => executar('/api/resetar'));
  $('#open-help').addEventListener('click', abrirFuncionamento);
  $('#close-help').addEventListener('click', fecharFuncionamento);
  $('#help-modal').addEventListener('click', e => {if(e.target.id === 'help-modal') fecharFuncionamento();});
  document.addEventListener('keydown', e => {
    if ($('#help-modal').hidden) return;
    if (e.key === 'Escape') fecharFuncionamento();
    if (e.key === 'Tab') {
      const itens = $$('#help-modal button:not([disabled])');
      if (itens.length) {e.preventDefault(); itens[0].focus();}
    }
  });
  try {
    [fontes,estado]=await Promise.all([api('/api/classes'),api('/api/estado')]);
    renderTudo();
  }catch(e){aviso(`Não foi possível conectar ao backend Python: ${e.message}`);}
}
document.addEventListener('DOMContentLoaded',iniciar);
