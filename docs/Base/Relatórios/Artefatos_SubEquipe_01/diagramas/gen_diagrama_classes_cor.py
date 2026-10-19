#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o Diagrama de Classes UML 2.5 do GoF Comportamental Chain of
Responsibility aplicado ao módulo de Recursos da LAI (Entrega 03).

Notação verificada em uml-diagrams.org (class-reference.html,
generalization.html, association.html, dependency.html) antes de desenhar:
  - Classe abstrata: nome em itálico.
  - Operação abstrata: assinatura em itálico (convenção herdada da UML 1.4.2,
    citada na própria referência, já que a UML 2.4+ não define uma notação
    própria para "operação abstrata").
  - Visibilidade: '+' publico, '#' protegido, '-' privado, '~' pacote.
  - Generalização: linha sólida, seta triangular VAZADA apontando para a
    superclasse; generalizações para a mesma superclasse podem compartilhar
    um único tronco com uma só seta (citado na referência).
  - Associação: linha sólida; extremidade navegável = seta aberta (não
    triangular, não preenchida); nome de papel (role) e multiplicidade perto
    da extremidade a que se referem; auto-associação (reflexiva) é uma linha
    saindo e voltando para a mesma classe.
  - Dependência: linha tracejada com seta (aberta), do cliente para o
    fornecedor; estereótipo «use» quando o cliente só usa o fornecedor como
    tipo de parâmetro/atributo (não possui, não associa); «create» quando o
    cliente instancia o fornecedor.
  - Enumeração: retângulo com o estereótipo «enumeration» e os literais no
    compartimento inferior.
Nenhuma notação fora dessas fontes foi usada.
"""

import html

W, H = 2150, 1400
svg_parts = []

def esc(s):
    return html.escape(str(s), quote=True)

def add(s):
    svg_parts.append(s)

# ---------------------------------------------------------------------------
# Primitivas
# ---------------------------------------------------------------------------

FONT = "Helvetica, Arial, sans-serif"
FS_TITLE = 14
FS_BODY = 12.5
FS_STEREO = 11.5
LINE_H = 17

def text(x, y, s, size=FS_BODY, anchor="start", italic=False, bold=False,
          underline=False, style_extra=""):
    style = f'font-family="{FONT}" font-size="{size}" text-anchor="{anchor}"'
    if italic:
        style += ' font-style="italic"'
    if bold:
        style += ' font-weight="bold"'
    deco = ' text-decoration="underline"' if underline else ""
    add(f'<text x="{x}" y="{y}" {style}{deco} {style_extra}>{esc(s)}</text>')

def rect(x, y, w, h, fill="white", stroke="black", sw=1.3, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

def hline(x1, x2, y, sw=1.0):
    add(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="black" stroke-width="{sw}"/>')

def line(x1, y1, x2, y2, dash=None, sw=1.3):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="{sw}"{d}/>')

def polyline(points, dash=None, sw=1.3):
    pts = " ".join(f"{x},{y}" for x, y in points)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<polyline points="{pts}" fill="none" stroke="black" stroke-width="{sw}"{d}/>')

def open_arrowhead(tip, src, size=11, angle_deg=22):
    """Seta aberta (duas linhas), usada em associação navegável e em dependência."""
    import math
    tx, ty = tip
    sx, sy = src
    dx, dy = tx - sx, ty - sy
    length = max(math.hypot(dx, dy), 0.001)
    ux, uy = dx / length, dy / length
    ang = math.radians(angle_deg)
    for sign in (1, -1):
        rx = ux * math.cos(ang) - uy * math.sin(ang) * sign
        ry = ux * math.sin(ang) * sign + uy * math.cos(ang)
        ex = tx - rx * size
        ey = ty - ry * size
        add(f'<line x1="{tx}" y1="{ty}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="black" stroke-width="1.3"/>')

def hollow_triangle(tip, src, size=15, angle_deg=16):
    """Triangulo vazado (generalizacao), apontando para 'tip'."""
    import math
    tx, ty = tip
    sx, sy = src
    dx, dy = tx - sx, ty - sy
    length = max(math.hypot(dx, dy), 0.001)
    ux, uy = dx / length, dy / length
    ang = math.radians(angle_deg)
    pts = [(tx, ty)]
    for sign in (1, -1):
        rx = ux * math.cos(ang) - uy * math.sin(ang) * sign
        ry = ux * math.sin(ang) * sign + uy * math.cos(ang)
        ex = tx - rx * size
        ey = ty - ry * size
        pts.append((ex, ey))
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    add(f'<polygon points="{pts_str}" fill="white" stroke="black" stroke-width="1.3"/>')


class ClassBox:
    """Desenha uma classe/enumeração UML com compartimentos nome/atributos/operações."""

    def __init__(self, x, y, w, name, stereotype=None, abstract=False,
                 attrs=None, ops=None, is_enum=False, literals=None):
        self.x, self.y, self.w = x, y, w
        self.name = name
        self.stereotype = stereotype
        self.abstract = abstract
        self.attrs = attrs or []          # list[str] already formatted
        self.ops = ops or []              # list[(text, italic, underline)]
        self.is_enum = is_enum
        self.literals = literals or []
        self._compute_height()

    def _compute_height(self):
        header_lines = 1 + (1 if self.stereotype else 0)
        h = 12 + header_lines * LINE_H + 10
        self.header_h = h
        attr_h = (len(self.attrs) * LINE_H + 10) if (self.attrs or not self.is_enum) else 10
        if self.is_enum:
            attr_h = 0
        self.attr_h = attr_h if (self.attrs) else (0 if not self.is_enum else 0)
        if self.is_enum:
            lit_h = len(self.literals) * LINE_H + 10
            self.lit_h = lit_h
            self.op_h = 0
        else:
            self.lit_h = 0
            op_h = (len(self.ops) * LINE_H + 10) if self.ops else 0
            self.op_h = op_h
        self.total_h = self.header_h + self.attr_h + self.lit_h + self.op_h

    def render(self):
        x, y, w = self.x, self.y, self.w
        h = self.total_h
        rect(x, y, w, h)
        cy = y + 16
        if self.stereotype:
            text(x + w / 2, cy, f"«{self.stereotype}»", size=FS_STEREO, anchor="middle")
            cy += LINE_H
        text(x + w / 2, cy, self.name, size=FS_TITLE, anchor="middle",
             italic=self.abstract, bold=True)
        y_cursor = y + self.header_h

        if self.is_enum:
            hline(x, x + w, y_cursor)
            yy = y_cursor + 14
            for lit in self.literals:
                text(x + 10, yy, lit, size=FS_BODY)
                yy += LINE_H
        else:
            if self.attrs:
                hline(x, x + w, y_cursor)
                yy = y_cursor + 14
                for a in self.attrs:
                    text(x + 10, yy, a, size=FS_BODY)
                    yy += LINE_H
                y_cursor += self.attr_h
            else:
                hline(x, x + w, y_cursor)
                y_cursor += 0

            if self.ops:
                hline(x, x + w, y_cursor)
                yy = y_cursor + 14
                for (op_text, it, ul) in self.ops:
                    text(x + 10, yy, op_text, size=FS_BODY, italic=it, underline=ul)
                    yy += LINE_H

    # pontos de ancoragem
    def top(self, frac=0.5):
        return (self.x + self.w * frac, self.y)

    def bottom(self, frac=0.5):
        return (self.x + self.w * frac, self.y + self.total_h)

    def left(self, frac=0.5):
        return (self.x, self.y + self.total_h * frac)

    def right(self, frac=0.5):
        return (self.x + self.w, self.y + self.total_h * frac)


# ---------------------------------------------------------------------------
# Definição das classes (conteúdo fiel ao código-fonte Java entregue)
# ---------------------------------------------------------------------------

handler_ops = [
    ("+ encadear(proximo : InstanciaHandler) : InstanciaHandler", False, False),
    ("+ handle(recurso : Recurso) : void", False, False),
    ("# tratar(recurso : Recurso) : boolean", True, False),
    ("# nomeInstancia() : String", True, False),
]
handler = ClassBox(820, 100, 420, "InstanciaHandler", stereotype="Handler",
                    abstract=True, attrs=[], ops=handler_ops)

def concrete_ops(ctor_sig):
    return [
        (ctor_sig, False, False) if ctor_sig else None,
        ("# tratar(recurso : Recurso) : boolean", False, False),
        ("# nomeInstancia() : String", False, False),
    ]

validador = ClassBox(70, 400, 340, "ValidadorTempestividadeHandler",
                      stereotype="ConcreteHandler",
                      attrs=[],
                      ops=[op for op in concrete_ops(None) if op])

autoridade1 = ClassBox(450, 400, 340, "AutoridadeHierarquicaSuperiorHandler",
                        stereotype="ConcreteHandler",
                        attrs=["- vaiDeferir : boolean"],
                        ops=[op for op in concrete_ops(
                            "+ AutoridadeHierarquicaSuperiorHandler(vaiDeferir : boolean)") if op])

autoridade2 = ClassBox(830, 400, 340, "AutoridadeMaximaOrgaoHandler",
                        stereotype="ConcreteHandler",
                        attrs=["- vaiDeferir : boolean"],
                        ops=[op for op in concrete_ops(
                            "+ AutoridadeMaximaOrgaoHandler(vaiDeferir : boolean)") if op])

cgu = ClassBox(1210, 400, 340, "CGUHandler",
               stereotype="ConcreteHandler",
               attrs=["- vaiDeferir : boolean"],
               ops=[op for op in concrete_ops("+ CGUHandler(vaiDeferir : boolean)") if op])

cmri = ClassBox(1590, 400, 340, "CMRIHandler",
                stereotype="ConcreteHandler",
                attrs=["- vaiDeferir : boolean"],
                ops=[op for op in concrete_ops("+ CMRIHandler(vaiDeferir : boolean)") if op])

recurso_attrs = [
    "- protocolo : String",
    "- cidadao : String",
    "- tempestivo : boolean",
    "- orgaoDoPoderExecutivoFederal : boolean",
    "- status : Status",
    "- instanciaResponsavelPelaDecisao : String",
    "- motivoDaDecisao : String",
]
recurso_ops = [
    ("+ Recurso(protocolo : String, cidadao : String, tempestivo : boolean, orgaoDoPoderExecutivoFederal : boolean)", False, False),
    ("+ getProtocolo() : String", False, False),
    ("+ getCidadao() : String", False, False),
    ("+ isTempestivo() : boolean", False, False),
    ("+ isOrgaoDoPoderExecutivoFederal() : boolean", False, False),
    ("+ getStatus() : Status", False, False),
    ("+ getInstanciaResponsavelPelaDecisao() : String", False, False),
    ("+ getMotivoDaDecisao() : String", False, False),
    ("+ isDecidido() : boolean", False, False),
    ("+ decidir(status : Status, instancia : String, motivo : String) : void", False, False),
    ("+ toString() : String", False, False),
]
recurso = ClassBox(1230, 720, 900, "Recurso", stereotype="Request",
                    attrs=recurso_attrs, ops=recurso_ops)

status_literals = [
    "AGUARDANDO_ANALISE", "INTEMPESTIVO", "DEFERIDO",
    "INDEFERIDO", "NAO_CONHECIDO", "ESGOTADA_VIA_RECURSAL",
]
status_box = ClassBox(1230, 1180, 300, "Status", stereotype="enumeration",
                       is_enum=True, literals=status_literals)

cliente = ClassBox(70, 100, 380, "ChainOfResponsibilityDemo", stereotype="Client",
                    attrs=[], ops=[("+ main(args : String[]) : void", False, True)])

boxes = [handler, validador, autoridade1, autoridade2, cgu, cmri, recurso, status_box, cliente]

# ---------------------------------------------------------------------------
# Render: caixas
# ---------------------------------------------------------------------------

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>')

add(f'<text x="{W/2}" y="26" font-size="19" font-weight="bold" text-anchor="middle" font-family="{FONT}">'
    'Diagrama de Classes UML — GoF Comportamental: Chain of Responsibility</text>')
add(f'<text x="{W/2}" y="46" font-size="13" text-anchor="middle" font-family="{FONT}">'
    'Aplicado ao Módulo de Tramitação de Recursos da LAI (Informa.BR) — Entrega 03</text>')

for b in boxes:
    b.render()

# ---------------------------------------------------------------------------
# Relacionamentos
# ---------------------------------------------------------------------------

# 1) Generalização (tronco compartilhado, UML permite unir setas para a mesma superclasse)
trunk_y = handler.bottom()[1] + 46
hx = handler.bottom()[0]
line(hx, handler.bottom()[1], hx, trunk_y)  # tronco vertical descendo da superclasse
concretos = [validador, autoridade1, autoridade2, cgu, cmri]
branch_y = trunk_y
left_x = concretos[0].top()[0]
right_x = concretos[-1].top()[0]
hline(left_x, right_x, branch_y)  # barra horizontal comum
hollow_triangle(tip=(hx, handler.bottom()[1]), src=(hx, trunk_y), size=16)
for c in concretos:
    tx, ty = c.top()
    line(tx, branch_y, tx, ty)

# 2) Auto-associação (reflexiva) em InstanciaHandler, representando "proximo"
loop_x = handler.right()[0]
loop_y_top = handler.y + handler.header_h + 10
loop_y_bot = handler.y + handler.total_h - 10
loop_out = loop_x + 70
polyline([(loop_x, loop_y_top), (loop_out, loop_y_top),
          (loop_out, loop_y_bot), (loop_x, loop_y_bot)])
open_arrowhead(tip=(loop_x, loop_y_bot), src=(loop_out, loop_y_bot), size=10)
text(loop_out + 6, (loop_y_top + loop_y_bot) / 2 - 6, "proximo", size=11)
text(loop_out + 6, (loop_y_top + loop_y_bot) / 2 + 10, "0..1", size=11)

# 3) Dependência InstanciaHandler ..> Recurso («use»: Recurso só aparece como
#    tipo de parâmetro em handle()/tratar(), nunca como atributo).
# Rota desviando por fora (acima da auto-associação e à direita de CMRIHandler)
# para não cruzar nenhuma outra caixa do diagrama.
hx2 = handler.x + handler.w
hy2 = handler.y + 40
rx2, ry2 = recurso.top(0.9)
polyline([(hx2, hy2), (rx2, hy2), (rx2, ry2)], dash="6,4")
open_arrowhead(tip=(rx2, ry2), src=(rx2, hy2), size=10)
text(hx2 + 20, hy2 - 8, "«use»", size=11, italic=True)

# 4) Dependência Recurso ..> Status («use»: status é atributo cujo tipo é a
#    própria enumeração — o cliente/Recurso requer Status para sua definição)
rsx, rsy = recurso.bottom(0.35)
stx, sty = status_box.top(0.5)
line(rsx, rsy, stx, sty, dash="6,4")
open_arrowhead(tip=(stx, sty), src=(rsx, rsy), size=10)
text((rsx + stx) / 2 + 14, (rsy + sty) / 2, "«use»", size=11, italic=True)

# 5) Dependência ChainOfResponsibilityDemo ..> InstanciaHandler («use»)
cdx, cdy = cliente.right(0.25)
hlx, hly = handler.left(0.12)
line(cdx, cdy, hlx, hly, dash="6,4")
open_arrowhead(tip=(hlx, hly), src=(cdx, cdy), size=10)
text((cdx + hlx) / 2, (cdy + hly) / 2 - 10, "«use»", size=11, italic=True)

# 6) Dependência ChainOfResponsibilityDemo ..> Recurso («create»)
cdx2, cdy2 = cliente.bottom(0.9)
rlx, rly = recurso.left(0.08)
polyline([(cdx2, cdy2), (cdx2, 860), (recurso.x - 60, 860), (recurso.x - 60, rly), (rlx, rly)], dash="6,4")
open_arrowhead(tip=(rlx, rly), src=(recurso.x - 60, rly), size=10)
text(recurso.x - 115, rly - 8, "«create»", size=11, italic=True)

# ---------------------------------------------------------------------------
# Legenda
# ---------------------------------------------------------------------------
lx, ly = 70, 1180
add(f'<rect x="{lx}" y="{ly}" width="950" height="220" fill="white" stroke="black" stroke-width="1"/>')
text(lx + 12, ly + 20, "Legenda (notação UML 2.5 — uml-diagrams.org)", size=13, bold=True)

ly2 = ly + 40
line(lx + 12, ly2, lx + 70, ly2); hollow_triangle(tip=(lx+70, ly2), src=(lx+12, ly2), size=13)
text(lx + 82, ly2 + 4, "Generalização (herança): seta triangular vazada aponta para a superclasse", size=11.5)

ly2 += 26
line(lx + 12, ly2, lx + 70, ly2); open_arrowhead(tip=(lx+70, ly2), src=(lx+12, ly2), size=9)
text(lx + 82, ly2 + 4, "Associação navegável: linha sólida + seta aberta; papel e multiplicidade perto da extremidade", size=11.5)

ly2 += 26
line(lx + 12, ly2, lx + 70, ly2, dash="6,4"); open_arrowhead(tip=(lx+70, ly2), src=(lx+12, ly2), size=9)
text(lx + 82, ly2 + 4, "Dependência: linha tracejada + seta aberta, do cliente para o fornecedor («use» / «create»)", size=11.5)

ly2 += 26
text(lx + 12, ly2 + 4, "Classe / operação em itálico = abstrata.  +público  #protegido  -privado", size=11.5)

ly2 += 24
text(lx + 12, ly2 + 4, "«enumeration» = estereótipo UML para tipos enumerados (literais no compartimento inferior)", size=11.5)

ly2 += 24
text(lx + 12, ly2 + 4, "«Handler» / «ConcreteHandler» / «Client» / «Request» = estereótipos indicando o papel de cada", size=11.5)
text(lx + 12, ly2 + 20, "classe no padrão GoF (uso do mecanismo de extensibilidade por estereótipos da própria UML)", size=11.5)

add('</svg>')

with open('/tmp/claude-0/-home-claude/881fe8f3-9f38-565b-97aa-e32d49d9aea1/scratchpad/entrega3/diagrama_classes_chain_of_responsibility.svg', 'w', encoding='utf-8') as f:
    f.write("\n".join(svg_parts))

print("SVG gerado.")
