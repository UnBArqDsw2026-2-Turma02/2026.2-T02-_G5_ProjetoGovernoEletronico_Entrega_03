import PedidoDetalhes from './components/PedidoDetalhes'

export default function App() {
  return (
    <div className="min-h-screen">
      {/* Barra colorida superior */}
      <div className="h-1.5 bg-[linear-gradient(90deg,#1351b4_0_70%,#f2b705_70%_85%,#168821_85%)]" />
      
      {/* Cabeçalho do Informa.BR */}
      <header className="border-b border-gov-line bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <a href="#" onClick={(e) => e.preventDefault()} className="font-serif text-2xl font-bold text-gov-blue">
            Informa<span className="text-gov-ink">.BR</span>
          </a>
          <span className="text-sm text-gov-muted">Portal da Transparência e Acesso à Informação</span>
        </div>
      </header>

      {/* Conteúdo Principal (Onde o padrão State vai rodar) */}
      <main className="mx-auto max-w-5xl px-6 py-10">
        <PedidoDetalhes />
      </main>
    </div>
  )
}