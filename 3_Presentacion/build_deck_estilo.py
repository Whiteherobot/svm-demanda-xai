# -*- coding: utf-8 -*-
"""
Deck SVM en el ESTILO del compañero (no idéntico):
- Carátula con gradiente navy->teal + formas onduladas
- Tarjetas con cabecera de color + badges circulares numerados
- Iconos vectoriales, líneas divisorias, mini-etiquetas de color
- Banner inferior full-width con bombilla y palabra resaltada
Contenido = nuestro trabajo (proceso, ejemplo Cable USB-C, técnico).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Circle, FancyArrowPatch,
                                Rectangle, Polygon, PathPatch)
from matplotlib.path import Path
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------- fuentes ----------------
FD = "/usr/share/fonts/TTF/"
f_display = FontProperties(fname=FD+"OpenSans-CondensedExtraBold.ttf")   # títulos pesados
f_head    = FontProperties(fname=FD+"OpenSans-CondensedBold.ttf")        # cabeceras tarjeta
f_semib   = FontProperties(fname=FD+"OpenSans-CondensedSemiBold.ttf")
f_body    = FontProperties(fname=FD+"DejaVuSans.ttf")                    # cuerpo legible
f_bodyb   = FontProperties(fname=FD+"DejaVuSans-Bold.ttf")
f_mono    = FontProperties(fname=FD+"DejaVuSansMono.ttf")

# ---------------- paleta (estilo amigo) ----------------
NAVY   = "#14315e"
NAVYD  = "#0e2547"
MORADO = "#5b2fd0"
AZUL   = "#1f6fc0"
TEAL   = "#13a59b"
NARANJA= "#e08a1e"
VERDE  = "#2e9e4f"
ROJO   = "#d24b4b"
AMAR   = "#ffd23f"
GRIS   = "#5b6472"
GRISL  = "#8b94a3"
LINEA  = "#dfe5ee"
CARD   = "#ffffff"
BG     = "#eef2f8"
TXT    = "#1f2733"

W, H = 160.0, 90.0   # unidades de lienzo (16:9)

def new_fig(bg=BG):
    fig = plt.figure(figsize=(13.333, 7.5), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, facecolor=bg, edgecolor="none", zorder=-10))
    return fig, ax

def rcard(ax, x, y, w, h, fc=CARD, ec=LINEA, lw=1.2, rad=2.2, z=2, shadow=True):
    if shadow:
        ax.add_patch(FancyBboxPatch((x+0.5, y-0.6), w, h,
                     boxstyle=f"round,pad=0,rounding_size={rad}",
                     fc="#c7d0de", ec="none", alpha=0.45, zorder=z-1))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0,rounding_size={rad}",
                 fc=fc, ec=ec, lw=lw, zorder=z))

def chip(ax, x, y, text, fc, tc="#ffffff", fs=10, pad=0.5, fp=None):
    fp = fp or f_head
    t = ax.text(x, y, text, fontproperties=fp, fontsize=fs, color=tc,
                ha="left", va="center", zorder=6)
    return t

# medir ancho de texto en coords de datos
def text_w(ax, fig, s, fp, fs):
    t = ax.text(0, 0, s, fontproperties=fp, fontsize=fs, alpha=0)
    fig.canvas.draw()
    bb = t.get_window_extent()
    inv = ax.transData.inverted()
    (x0, _), (x1, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y0)])
    t.remove()
    return abs(x1 - x0)

def rich_center(ax, fig, cx, y, parts, fs, default_color=TXT):
    """parts: list of (text, color, fp, highlight_color_or_None)."""
    widths = [text_w(ax, fig, p[0], p[2], fs) for p in parts]
    total = sum(widths)
    x = cx - total / 2
    for (txt, col, fp, hl), wseg in zip(parts, widths):
        if hl:
            ax.add_patch(FancyBboxPatch((x-0.5, y-1.6), wseg+1.0, 3.2,
                         boxstyle="round,pad=0,rounding_size=0.8",
                         fc=hl, ec="none", zorder=5))
        ax.text(x, y, txt, fontproperties=fp, fontsize=fs, color=col,
                ha="left", va="center", zorder=6)
        x += wseg

# ---------------- iconos vectoriales ----------------
def ic_bars(ax, cx, cy, s, col):
    hs = [0.5, 0.8, 1.0, 0.45, 0.7]
    bw = s*0.16
    x0 = cx - s*0.45
    for i, hh in enumerate(hs):
        ax.add_patch(Rectangle((x0+i*s*0.22, cy-s*0.5), bw, s*hh,
                     fc=col, ec="none", zorder=6))

def ic_signals(ax, cx, cy, s, col):
    for i, yy in enumerate([0.42, 0.0, -0.42]):
        ax.plot([cx-s*0.5, cx+s*0.5], [cy+s*yy, cy+s*yy], color="#c9d3e2",
                lw=2.4, zorder=5, solid_capstyle="round")
        px = cx + s*(0.25 - i*0.28)
        ax.add_patch(Circle((px, cy+s*yy), s*0.10, fc=col, ec="white",
                     lw=1.2, zorder=6))

def ic_curve(ax, cx, cy, s, col):
    xs = np.linspace(cx-s*0.5, cx+s*0.5, 40)
    ys = cy - s*0.45 + s*0.95*((xs-(cx-s*0.5))/s)**1.8
    ax.plot(xs, ys, color=col, lw=3.2, zorder=6, solid_capstyle="round")
    ax.add_patch(Circle((xs[-1], ys[-1]), s*0.12, fc=VERDE, ec="white",
                 lw=1.4, zorder=7))

def ic_check(ax, cx, cy, s, col):
    ax.add_patch(FancyBboxPatch((cx-s*0.5, cy-s*0.45), s, s*0.9,
                 boxstyle="round,pad=0,rounding_size=0.6", fc="none",
                 ec=col, lw=2.6, zorder=6))
    ax.plot([cx-s*0.22, cx-s*0.02, cx+s*0.3],
            [cy-s*0.02, cy-s*0.24, cy+s*0.26],
            color=VERDE, lw=3.4, zorder=7, solid_capstyle="round",
            solid_joinstyle="round")

def ic_bulb(ax, cx, cy, s):
    ax.add_patch(Circle((cx, cy+s*0.12), s*0.5, fc=AMAR, ec="#caa400",
                 lw=1.2, zorder=6))
    ax.add_patch(Rectangle((cx-s*0.22, cy-s*0.55), s*0.44, s*0.3,
                 fc="#caa400", ec="none", zorder=6))
    for ang in range(0, 360, 45):
        a = np.radians(ang)
        ax.plot([cx+np.cos(a)*s*0.62, cx+np.cos(a)*s*0.82],
                [cy+s*0.12+np.sin(a)*s*0.62, cy+s*0.12+np.sin(a)*s*0.82],
                color=AMAR, lw=2.2, zorder=5, solid_capstyle="round")

# ---------------- componentes tarjeta ----------------
def step_card(ax, x, y, w, h, color, num, title):
    rcard(ax, x, y, w, h, z=3)
    # cabecera de color
    ax.add_patch(FancyBboxPatch((x+1.0, y+h-8.5), w-2.0, 7.0,
                 boxstyle="round,pad=0,rounding_size=1.4",
                 fc=color, ec="none", zorder=4))
    ax.text(x+w/2, y+h-5.0, title, fontproperties=f_head, fontsize=12.5,
            color="white", ha="center", va="center", zorder=6)
    # badge
    bcx, bcy = x+w/2, y+h
    ax.add_patch(Circle((bcx, bcy), 3.4, fc="white", ec="none", zorder=6))
    ax.add_patch(Circle((bcx, bcy), 2.9, fc=color, ec="none", zorder=7))
    ax.text(bcx, bcy-0.05, str(num), fontproperties=f_display, fontsize=15,
            color="white", ha="center", va="center", zorder=8)
    return x+w/2  # centro x para el contenido

def bottom_banner(ax, fig, parts, fc="#eaf0fb", ec="#cdd9ef"):
    by, bh = 3.5, 8.0
    ax.add_patch(FancyBboxPatch((6, by), W-12, bh,
                 boxstyle="round,pad=0,rounding_size=1.6",
                 fc=fc, ec=ec, lw=1.2, zorder=3))
    ic_bulb(ax, 13, by+bh/2, 3.0)
    rich_center(ax, fig, W/2+4, by+bh/2, parts, 13)

def title_block(ax, title, subtitle, accent=NARANJA):
    ax.add_patch(Rectangle((0, H-13.5), W, 13.5, fc=NAVY, ec="none", zorder=1))
    ax.add_patch(Rectangle((0, H-13.5), W, 0.7, fc=accent, ec="none", zorder=2))
    ax.text(8, H-6.0, title, fontproperties=f_display, fontsize=27,
            color="white", ha="left", va="center", zorder=3)
    ax.text(8, H-10.6, subtitle, fontproperties=f_semib, fontsize=12.5,
            color="#b9c6dc", ha="left", va="center", zorder=3)

# =================================================================
# 1) CARÁTULA
# =================================================================
def slide_caratula():
    fig, ax = new_fig(bg=NAVYD)
    # gradiente navy -> teal
    cmap = LinearSegmentedColormap.from_list("nt", [NAVYD, NAVY, "#175a8a", TEAL])
    grad = np.linspace(0, 1, 400).reshape(1, -1)
    ax.imshow(grad, extent=[0, W, 0, H], aspect="auto", cmap=cmap,
              zorder=-5, alpha=1.0)
    # formas onduladas a la derecha
    rng = np.random.default_rng(7)
    ys = np.linspace(0, H, 120)
    for k, base in enumerate([108, 124, 140]):
        amp = 6 + k*1.5
        xs = base + amp*np.sin(ys/12.0 + k*1.1)
        verts = list(zip(xs, ys)) + [(W, H), (W, 0)]
        ax.add_patch(Polygon(verts, closed=True,
                     fc="white", ec="none", alpha=0.06+0.03*k, zorder=-3))
    # texto
    ax.text(10, 64, "Endify  ·  Técnicas de ML Supervisado  —  presenta",
            fontproperties=f_semib, fontsize=14, color="#cfe0f2",
            ha="left", va="center")
    ax.text(9.4, 49, "PRÁCTICA SVM", fontproperties=f_display, fontsize=66,
            color="white", ha="left", va="center")
    ax.text(10, 40, "Pronóstico de demanda explicable con SVR",
            fontproperties=f_head, fontsize=18, color=AMAR,
            ha="left", va="center")
    ax.text(10, 18.5, "INTEGRANTES:", fontproperties=f_head, fontsize=15,
            color="#cfe0f2", ha="left", va="center")
    ax.text(10, 13.0, "Michael Lata", fontproperties=f_display, fontsize=22,
            color="white", ha="left", va="center")
    ax.text(10, 8.0, "Jordy Romero", fontproperties=f_display, fontsize=22,
            color="white", ha="left", va="center")
    fig.savefig(OUT+"/cara_estilo.png", dpi=200)
    plt.close(fig)

# =================================================================
# 2) PROCESO (4 pasos)
# =================================================================
def slide_proceso():
    fig, ax = new_fig()
    title_block(ax, "¿CÓMO PRONOSTICAMOS LA DEMANDA?",
                "Del historial de ventas a la decisión de cuánto reabastecer  ·  4 pasos",
                accent=NARANJA)
    cols = [MORADO, AZUL, TEAL, NAVY]
    titles = ["HISTORIAL DE VENTAS", "SEÑALES CLAVE",
              "LA SVM PRONOSTICA", "DECISIÓN DE INVENTARIO"]
    descs = [
        "Tomamos las ventas\nrecientes de cada\nproducto.",
        "Las resumimos en pistas:\npromedio de la semana,\ndía, fin de semana, stock.",
        "El modelo predice la\ndemanda de mañana,\nproducto por producto.",
        "Traducimos el pronóstico\nen cuánto reabastecer:\nsin quebrar ni sobrar.",
    ]
    tags = [("Histórico", MORADO), ("Características", AZUL),
            ("SVR (RBF)", TEAL), ("Acción", NAVY)]
    icons = [ic_bars, ic_signals, ic_curve, ic_check]
    x0, w, gap = 6.0, 34.0, 4.0
    ytop, ch = 14.0, 47.0
    for i in range(4):
        x = x0 + i*(w+gap)
        cx = step_card(ax, x, ytop, w, ch, cols[i], i+1, titles[i])
        icons[i](ax, cx, ytop+ch-15.5, 7.5, cols[i])
        ax.text(cx, ytop+ch-24.5, descs[i], fontproperties=f_body, fontsize=10.5,
                color=TXT, ha="center", va="center", linespacing=1.5, zorder=6)
        ax.plot([x+4, x+w-4], [ytop+13.5, ytop+13.5], color=LINEA, lw=1.2, zorder=5)
        # tag de color
        tg, tc = tags[i]
        tw = text_w(ax, fig, tg, f_head, 9.5)
        ax.add_patch(FancyBboxPatch((cx-tw/2-1.4, ytop+8.2), tw+2.8, 3.4,
                     boxstyle="round,pad=0,rounding_size=0.8", fc=tc,
                     ec="none", zorder=6))
        ax.text(cx, ytop+9.9, tg, fontproperties=f_head, fontsize=9.5,
                color="white", ha="center", va="center", zorder=7)
        if i < 3:
            ax.add_patch(FancyArrowPatch((x+w+0.3, ytop+ch/2),
                         (x+w+gap-0.3, ytop+ch/2),
                         arrowstyle="-|>", mutation_scale=16,
                         color=GRIS, lw=2.0, zorder=8))
    bottom_banner(ax, fig, [
        ("Un proceso ", TXT, f_bodyb, None),
        ("simple, automático y explicable", NAVY, f_bodyb, AMAR),
        ("  —  el mismo para los 10 productos.", TXT, f_bodyb, None),
    ])
    fig.savefig(OUT+"/proc_estilo.png", dpi=200)
    plt.close(fig)

# =================================================================
# 3) EJEMPLO (Cable USB-C)
# =================================================================
def slide_ejemplo():
    fig, ax = new_fig()
    title_block(ax, "EJEMPLO REAL:  CABLE USB-C",
                "Siguiendo los mismos 4 pasos con datos reales  ·  pronóstico para el sábado 2026-09-05",
                accent=TEAL)
    cols = [MORADO, AZUL, TEAL, NAVY]
    titles = ["HISTORIAL DE VENTAS", "SEÑALES CLAVE",
              "LA SVM PRONOSTICA", "DECISIÓN DE INVENTARIO"]
    x0, w, gap = 6.0, 34.0, 4.0
    ytop, ch = 14.0, 47.0
    cxs = []
    for i in range(4):
        x = x0 + i*(w+gap)
        cx = step_card(ax, x, ytop, w, ch, cols[i], i+1, titles[i])
        cxs.append((x, cx))
        if i < 3:
            ax.add_patch(FancyArrowPatch((x+w+0.3, ytop+ch/2),
                         (x+w+gap-0.3, ytop+ch/2),
                         arrowstyle="-|>", mutation_scale=16,
                         color=GRIS, lw=2.0, zorder=8))

    # --- card 1: mini bar chart (últimos 7 días) ---
    x, cx = cxs[0]
    serie = [22, 30, 41, 14, 12, 18, 23]
    dias = ["L", "M", "X", "J", "V", "S", "D"]
    bx = fig.add_axes([0.075, 0.30, 0.135, 0.20])
    bx.bar(range(7), serie, color=MORADO, width=0.72)
    bx.set_ylim(0, 46)
    for s in bx.spines.values():
        s.set_visible(False)
    bx.set_xticks(range(7)); bx.set_xticklabels(dias, fontproperties=f_body, fontsize=7)
    bx.set_yticks([]); bx.tick_params(length=0)
    bx.set_title("últimos 7 días", fontproperties=f_body, fontsize=8, color=GRIS)
    ax.text(cx, ytop+9.5, "Ventas reales  ·  promedio 23/día",
            fontproperties=f_body, fontsize=9.5, color=TXT, ha="center", zorder=6)

    # --- card 2: señales ---
    x, cx = cxs[1]
    sig = [("Promedio", "23/día"), ("Ventas hoy", "23"),
           ("Mañana", "sábado"), ("Fin de semana", "sí")]
    yy = ytop+ch-15.0
    for lab, val in sig:
        ax.text(x+3.5, yy, lab, fontproperties=f_body, fontsize=10.5,
                color=GRIS, ha="left", va="center", zorder=6)
        ax.text(x+w-3.5, yy, val, fontproperties=f_bodyb, fontsize=10.5,
                color=NAVY, ha="right", va="center", zorder=6)
        ax.plot([x+3.5, x+w-3.5], [yy-2.6, yy-2.6], color=LINEA, lw=0.9, zorder=5)
        yy -= 6.2

    # --- card 3: pronóstico ---
    x, cx = cxs[2]
    ax.text(cx, ytop+ch-22, "≈ 24", fontproperties=f_display, fontsize=42,
            color=TEAL, ha="center", va="center", zorder=6)
    ax.text(cx, ytop+ch-31, "unidades mañana", fontproperties=f_body,
            fontsize=10.5, color=GRIS, ha="center", zorder=6)
    tw = text_w(ax, fig, "real: 23  ✓", f_bodyb, 11)
    ax.add_patch(FancyBboxPatch((cx-tw/2-1.6, ytop+9.5), tw+3.2, 4.0,
                 boxstyle="round,pad=0,rounding_size=1.0", fc="#e7f6ec",
                 ec=VERDE, lw=1.2, zorder=6))
    ax.text(cx, ytop+11.5, "real: 23  ✓", fontproperties=f_bodyb, fontsize=11,
            color=VERDE, ha="center", va="center", zorder=7)

    # --- card 4: decisión ---
    x, cx = cxs[3]
    ax.text(cx, ytop+ch-15.0, "Stock actual:  182", fontproperties=f_body,
            fontsize=10.5, color=TXT, ha="center", zorder=6)
    tw = text_w(ax, fig, "Demanda cubierta  ✓", f_bodyb, 10.5)
    ax.add_patch(FancyBboxPatch((cx-tw/2-1.6, ytop+ch-25.0), tw+3.2, 4.0,
                 boxstyle="round,pad=0,rounding_size=1.0", fc="#e7f6ec",
                 ec=VERDE, lw=1.2, zorder=6))
    ax.text(cx, ytop+ch-23.0, "Demanda cubierta  ✓", fontproperties=f_bodyb,
            fontsize=10.5, color=VERDE, ha="center", va="center", zorder=7)
    ax.text(cx, ytop+ch-33.0, "Reforzar de cara al\nfin de semana por la\nalta variabilidad.",
            fontproperties=f_body, fontsize=9.5, color=TXT, ha="center",
            va="center", linespacing=1.5, zorder=6)

    bottom_banner(ax, fig, [
        ("El modelo predijo 24 y se vendieron 23", NAVY, f_bodyb, AMAR),
        ("  →  decisión de inventario confiable.", TXT, f_bodyb, None),
    ])
    fig.savefig(OUT+"/ejem_estilo.png", dpi=200)
    plt.close(fig)

# =================================================================
# 4) TÉCNICO (3 cards)
# =================================================================
def codebox(ax, x, y, w, h, lines, fc="#0f1f3d"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0,rounding_size=1.0",
                 fc=fc, ec="none", zorder=5))
    yy = y+h-2.6
    for ln, col in lines:
        ax.text(x+1.8, yy, ln, fontproperties=f_mono, fontsize=7.6,
                color=col, ha="left", va="center", zorder=6)
        yy -= 2.7

def slide_tecnico():
    fig, ax = new_fig()
    title_block(ax, "DETALLE TÉCNICO  —  PARA INGENIERÍA",
                "Modelo SVM  ·  importancia desde su estructura interna  ·  agrupamiento con k-means",
                accent=MORADO)
    cols = [NAVY, AZUL, TEAL]
    titles = ["MODELO SVM + VALIDACIÓN", "IMPORTANCIA DE VARIABLES",
              "PRODUCTOS SIMILARES (K-MEANS)"]
    x0, w, gap = 6.0, 48.667, 3.0
    ytop, ch = 13.0, 50.0
    cxs = []
    for i in range(3):
        x = x0 + i*(w+gap)
        cx = step_card(ax, x, ytop, w, ch, cols[i], i+1, titles[i])
        cxs.append((x, cx))

    GREEN="#7fe0a0"; CYAN="#7fd6e0"; ORANGE="#f0b25a"; WHITE="#eef2f8"; KEY="#c9a0ff"
    # card 1
    x, cx = cxs[0]
    codebox(ax, x+3, ytop+ch-23, w-6, 12.5, [
        ("Pipeline([", WHITE),
        ("  StandardScaler(),", CYAN),
        ("  SVR(kernel='rbf', C=10,", GREEN),
        ("      gamma=0.05, epsilon=1.0)])", GREEN),
        ("GridSearchCV(cv=TimeSeriesSplit(5),", ORANGE),
        ("   scoring='neg_RMSE')", ORANGE),
    ])
    res = [("Vectores de soporte", "1086 / 1380"),
           ("RMSE / MAE", "5.11 / 3.65"),
           ("R²  (vs Práctica 2)", "0.42  vs  0.28")]
    yy = ytop+ch-32.0
    for lab, val in res:
        ax.text(x+3.5, yy, lab, fontproperties=f_body, fontsize=9,
                color=GRIS, ha="left", va="center", zorder=6)
        ax.text(x+w-3.5, yy, val, fontproperties=f_bodyb, fontsize=9.5,
                color=VERDE if "0.42" in val else NAVY, ha="right",
                va="center", zorder=6)
        yy -= 4.6
    ax.text(cx, ytop+5.0, "Validación temporal — sin fuga de datos (expanding window).",
            fontproperties=f_body, fontsize=8.5, color=GRIS, ha="center", zorder=6)

    # card 2: |w|
    x, cx = cxs[1]
    ax.text(x+3.5, ytop+ch-13.5, "w = LinearSVR().coef_   →   |w| ordenado",
            fontproperties=f_mono, fontsize=8.2, color=NAVY, ha="left", zorder=6)
    feats = [("rolling_mean_7", 4.66), ("cantidad_vendida", 1.11),
             ("lag_1", 0.61), ("es_weekend", 0.55)]
    maxw = 4.66; bx0 = x+3.5; bw = w-20
    yy = ytop+ch-19.0
    for fname, val in feats:
        ax.text(bx0, yy+1.4, fname, fontproperties=f_body, fontsize=8.5,
                color=TXT, ha="left", va="center", zorder=6)
        ax.add_patch(Rectangle((bx0, yy-1.6), bw, 1.8, fc="#e6ebf3",
                     ec="none", zorder=5))
        ax.add_patch(Rectangle((bx0, yy-1.6), bw*val/maxw, 1.8, fc=AZUL,
                     ec="none", zorder=6))
        ax.text(x+w-3.0, yy-0.7, f"{val:.2f}", fontproperties=f_bodyb,
                fontsize=8.5, color=NAVY, ha="right", va="center", zorder=6)
        yy -= 5.4
    ax.plot([x+3.5, x+w-3.5], [yy+1.0, yy+1.0], color=LINEA, lw=1.0, zorder=5)
    ax.text(cx, yy-2.0, "rolling_mean_7 pesa más que las otras 11 juntas\n(4.66 > 4.52)",
            fontproperties=f_bodyb, fontsize=8.5, color=NAVY, ha="center",
            va="center", linespacing=1.4, zorder=6)
    ax.text(cx, ytop+4.3, "Confirmado por permutación · SHAP · Integrated Gradients (Top-3 coincide).\nRBF no expone w → en producción se usa SHAP/permutación.",
            fontproperties=f_body, fontsize=7.6, color=GRIS, ha="center",
            va="center", linespacing=1.4, zorder=6)

    # card 3: k-means
    x, cx = cxs[2]
    codebox(ax, x+3, ytop+ch-20, w-6, 10, [
        ("perfil = [demanda_media, volatilidad,", WHITE),
        ("          uplift_finde, stock_medio]", WHITE),
        ("KMeans(n_clusters=3, n_init=10)", GREEN),
        ("      .fit(scale(perfil))", GREEN),
    ])
    sx = fig.add_axes([0.688, 0.235, 0.122, 0.155])
    G0 = ([30, 38, 34, 42], [6, 8, 7, 9])
    G1 = ([55, 62, 58, 66], [14, 17, 15, 19])
    G2 = ([88, 95], [34, 40])
    sx.scatter(*G0, c=TEAL, s=34)
    sx.scatter(*G1, c=AZUL, s=34)
    sx.scatter(*G2, c=NARANJA, s=34)
    sx.set_xlim(20, 105); sx.set_ylim(0, 46)
    sx.set_xticks([]); sx.set_yticks([])
    for s in sx.spines.values():
        s.set_color(LINEA)
    sx.set_xlabel("demanda media →", fontproperties=f_body, fontsize=7, color=GRIS)
    sx.set_ylabel("volatilidad →", fontproperties=f_body, fontsize=7, color=GRIS)
    # leyenda lateral derecha
    leg = [("G0 estables (4)", TEAL), ("G1 volumen medio (4)", AZUL),
           ("G2 alta rotación / finde (2)", NARANJA)]
    ly = ytop+ch-31.0
    for txt, col in leg:
        ax.add_patch(Circle((x+w-22.5, ly), 0.8, fc=col, ec="none", zorder=6))
        ax.text(x+w-21.0, ly, txt, fontproperties=f_body, fontsize=8.2,
                color=TXT, ha="left", va="center", zorder=6)
        ly -= 5.0
    ax.text(cx, ytop+4.6, "Agrupamos productos con perfiles parecidos.",
            fontproperties=f_body, fontsize=8, color=GRIS, ha="center", zorder=6)

    # banner stack
    by, bh = 3.0, 6.2
    ax.add_patch(FancyBboxPatch((6, by), W-12, bh,
                 boxstyle="round,pad=0,rounding_size=1.4",
                 fc=NAVY, ec="none", zorder=3))
    ax.text(W/2, by+bh/2,
            "Stack:  scikit-learn · StandardScaler · SVR/LinearSVR · KMeans · SHAP  —  determinista y sin GPU",
            fontproperties=f_mono, fontsize=8.6, color="#cfe0f2",
            ha="center", va="center", zorder=6)
    fig.savefig(OUT+"/tec_estilo.png", dpi=200)
    plt.close(fig)

# =================================================================
# 5) GRACIAS
# =================================================================
def slide_gracias():
    fig, ax = new_fig(bg=NAVYD)
    cmap = LinearSegmentedColormap.from_list("nt", [NAVYD, NAVY, "#175a8a", TEAL])
    grad = np.linspace(0, 1, 400).reshape(1, -1)
    ax.imshow(grad, extent=[0, W, 0, H], aspect="auto", cmap=cmap, zorder=-5)
    ys = np.linspace(0, H, 120)
    for k, base in enumerate([18, 34, 50]):
        amp = 6 + k*1.5
        xs = base + amp*np.sin(ys/12.0 + k*1.1)
        verts = [(0, 0), (0, H)] + list(zip(xs, ys))
        ax.add_patch(Polygon(verts, closed=True, fc="white", ec="none",
                     alpha=0.05+0.03*k, zorder=-3))
    ax.text(W/2, H/2+4, "GRACIAS", fontproperties=f_display, fontsize=70,
            color="white", ha="center", va="center")
    ax.text(W/2, H/2-9, "Pronóstico de demanda explicable con SVM  ·  Endify",
            fontproperties=f_head, fontsize=16, color=AMAR, ha="center", va="center")
    fig.savefig(OUT+"/grac_estilo.png", dpi=200)
    plt.close(fig)

if __name__ == "__main__":
    slide_caratula()
    slide_proceso()
    slide_ejemplo()
    slide_tecnico()
    slide_gracias()
    print("PNGs generados OK")
