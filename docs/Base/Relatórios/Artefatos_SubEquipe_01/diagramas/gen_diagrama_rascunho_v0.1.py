#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RASCUNHO (v0.1) do Diagrama de Classes do GoF Chain of Responsibility.

Propósito: registrar uma versão inicial e mais simples do diagrama, anterior
ao diagrama de classes completo (v1.0, com Recurso/Status/Client/dependências),
para compor um histórico de versões real (v0.1 -> v1.0), evitando o problema
de "única versão" já apontado pela professora em entregas anteriores.

Mostra apenas o essencial do padrão (o esqueleto da cadeia de handlers):
Handler abstrato + 5 ConcreteHandlers + a auto-associação "proximo" que
define a cadeia. Sem atributos, sem Request/Client, sem dependências —
deliberadamente reduzido, mas sem violar nenhuma regra de notação (mesmas
fontes já verificadas: uml-diagrams.org class-reference / generalization /
association).
"""
import html, math

W, H = 1500, 440
parts = []
def esc(s): return html.escape(str(s), quote=True)
def add(s): parts.append(s)

FONT = "Helvetica, Arial, sans-serif"

def text(x, y, s, size=12.5, anchor="start", italic=False, bold=False):
    style = f'font-family="{FONT}" font-size="{size}" text-anchor="{anchor}"'
    if italic: style += ' font-style="italic"'
    if bold: style += ' font-weight="bold"'
    add(f'<text x="{x}" y="{y}" {style}>{esc(s)}</text>')

def rect(x, y, w, h):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="black" stroke-width="1.3"/>')

def hline(x1, x2, y):
    add(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="black" stroke-width="1"/>')

def line(x1, y1, x2, y2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="1.3"{d}/>')

def polyline(pts):
    s = " ".join(f"{x},{y}" for x, y in pts)
    add(f'<polyline points="{s}" fill="none" stroke="black" stroke-width="1.3"/>')

def hollow_triangle(tip, src, size=15, angle_deg=16):
    tx, ty = tip; sx, sy = src
    dx, dy = tx - sx, ty - sy
    length = max(math.hypot(dx, dy), 0.001)
    ux, uy = dx/length, dy/length
    ang = math.radians(angle_deg)
    pts = [(tx, ty)]
    for sign in (1, -1):
        rx = ux*math.cos(ang) - uy*math.sin(ang)*sign
        ry = ux*math.sin(ang)*sign + uy*math.cos(ang)
        pts.append((tx - rx*size, ty - ry*size))
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    add(f'<polygon points="{s}" fill="white" stroke="black" stroke-width="1.3"/>')

def open_arrowhead(tip, src, size=10, angle_deg=22):
    tx, ty = tip; sx, sy = src
    dx, dy = tx - sx, ty - sy
    length = max(math.hypot(dx, dy), 0.001)
    ux, uy = dx/length, dy/length
    ang = math.radians(angle_deg)
    for sign in (1, -1):
        rx = ux*math.cos(ang) - uy*math.sin(ang)*sign
        ry = ux*math.sin(ang)*sign + uy*math.cos(ang)
        ex, ey = tx - rx*size, ty - ry*size
        add(f'<line x1="{tx}" y1="{ty}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="black" stroke-width="1.2"/>')

class Box:
    def __init__(self, x, y, w, name, stereotype, abstract=False, ops=None):
        self.x, self.y, self.w = x, y, w
        self.name, self.stereotype, self.abstract = name, stereotype, abstract
        self.ops = ops or []
        header = 12 + (34 if stereotype else 17) + 10
        self.header_h = header
        self.op_h = (len(self.ops) * 17 + 10) if self.ops else 0
        self.h = self.header_h + self.op_h

    def render(self):
        rect(self.x, self.y, self.w, self.h)
        cy = self.y + 16
        if self.stereotype:
            text(self.x + self.w/2, cy, f"«{self.stereotype}»", size=11, anchor="middle")
            cy += 17
        text(self.x + self.w/2, cy, self.name, size=13.5, anchor="middle", bold=True, italic=self.abstract)
        yb = self.y + self.header_h
        hline(self.x, self.x + self.w, yb)
        yy = yb + 14
        for op, it in self.ops:
            text(self.x + 8, yy, op, size=11, italic=it)
            yy += 17

    def top(self, f=0.5): return (self.x + self.w*f, self.y)
    def bottom(self, f=0.5): return (self.x + self.w*f, self.y + self.h)
    def right(self, f=0.5): return (self.x + self.w, self.y + self.h*f)

handler = Box(560, 30, 320, "InstanciaHandler", "Handler", abstract=True,
              ops=[("+ handle(recurso : Recurso) : void", False),
                   ("# tratar(recurso : Recurso) : boolean", True)])

names = ["ValidadorTempestividadeHandler", "AutoridadeHierarquicaSuperiorHandler",
         "AutoridadeMaximaOrgaoHandler", "CGUHandler", "CMRIHandler"]
xs = [20, 300, 580, 860, 1140]
concretos = [Box(xs[i], 330, 260, names[i], "ConcreteHandler") for i in range(5)]

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>')
add(f'<text x="{W/2}" y="20" font-size="15" font-weight="bold" text-anchor="middle" font-family="{FONT}">'
    'Chain of Responsibility — Rascunho v0.1 (esqueleto do padrão)</text>')

handler.render()
for c in concretos:
    c.render()

# auto-associação proximo
lx = handler.right()[0]
ytop = handler.y + handler.header_h + 8
ybot = handler.y + handler.h - 8
lout = lx + 55
polyline([(lx, ytop), (lout, ytop), (lout, ybot), (lx, ybot)])
open_arrowhead((lx, ybot), (lout, ybot), size=9)
text(lout + 5, (ytop+ybot)/2 - 4, "proximo", size=10.5)
text(lout + 5, (ytop+ybot)/2 + 11, "0..1", size=10.5)

# generalização com tronco compartilhado
trunk_y = handler.bottom()[1] + 40
hx = handler.bottom()[0]
line(hx, handler.bottom()[1], hx, trunk_y)
hline(concretos[0].top()[0], concretos[-1].top()[0], trunk_y)
hollow_triangle((hx, handler.bottom()[1]), (hx, trunk_y), size=14)
for c in concretos:
    tx, ty = c.top()
    line(tx, trunk_y, tx, ty)

text(20, 425, "Nota: rascunho inicial — ainda sem Recurso (Request), Client nem dependências; refinado na v1.0.", size=10.5, italic=True)

add('</svg>')

out = '/tmp/claude-0/-home-claude/881fe8f3-9f38-565b-97aa-e32d49d9aea1/scratchpad/entrega3/diagrama_classes_chain_of_responsibility_v0.1_rascunho.svg'
with open(out, 'w', encoding='utf-8') as f:
    f.write("\n".join(parts))
print("OK", out)
