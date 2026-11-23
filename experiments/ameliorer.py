#!/usr/bin/env python3
"""
ameliorer.py — peut-on faire mieux que 62 %, sans tricher ?

LE PROTOCOLE, ECRIT AVANT D'AVOIR VU UN SEUL RESULTAT (3 novembre 2026).

  Donnees   les 3 developpeurs Django de corpus/devs/, 3 000 lignes chacun, dans
            l'ordre des commits. Hasard : 33 %.
  Test      les 40 % de lignes les PLUS RECENTES de chacun. Jamais regardees pour
            choisir quoi que ce soit. Evaluees UNE fois, a la fin.
  Choix     sur les 60 % les plus anciennes seulement, recoupees a leur tour dans
            le temps : 60 % pour apprendre, 40 % pour valider. La methode qui gagne
            la VALIDATION est retenue ; a egalite, la plus simple (ordre de la
            grille ci-dessous). Puis elle est reapprise sur les 60 % et testee.
  Grille    features   : 10 lisibles, 7 syntaxiques, les deux ; 100 / 300 tokens ;
                         300 paires de tokens ; 300 / 800 / 2000 4-grammes ;
                         800 3-grammes
            comparaison: z-score + Manhattan (Delta de Burrows) ; z-score + cosinus ;
                         frequences brutes + cosinus
            vocabulaire, moyennes et ecarts-types : sur l'apprentissage seul
  Blocs     80 et 160 lignes (les deux tailles du talk), traitees separement.
  Rapport   le score de la methode RETENUE, avec son intervalle de confiance a 95 %
            (Wilson) ; PUIS le score de test de TOUTES les methodes de la grille,
            pour qu'on voie si le choix a eu de la chance.
  Separement, la meme selection restreinte aux features qu'on peut expliquer
  (lisibles, syntaxiques, tokens) : la question du talk, « peut-on dire pourquoi ? ».

Usage :  python3 experiments/ameliorer.py
"""
from __future__ import annotations

import math
import os
import re
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contre_tests import CODE, TOK
from _commun import sig
from deux_fichiers_ia import feats as syntaxe

DEVS = list(CODE)


def blocs(L, n):
    return ['\n'.join(L[i:i + n]) for i in range(0, len(L) - n + 1, n)]


# ── familles de features : (nom, explicable ?, fabrique(textes_apprentissage) -> f(bloc)) ──
def f_lisibles(_):
    return lambda b: np.array(sig(b), float)


def f_syntaxe(_):
    return lambda b: np.array(list(syntaxe(b).values()), float)


def f_les_deux(_):
    return lambda b: np.concatenate([np.array(sig(b), float), np.array(list(syntaxe(b).values()), float)])


def f_tokens(n):
    def fab(textes):
        voc = [w for w, _ in Counter(t for x in textes for t in TOK(x)).most_common(n)]
        def f(b):
            t = TOK(b); c = Counter(t); m = max(len(t), 1)
            return np.array([c.get(w, 0) / m for w in voc])
        return f
    return fab


def f_paires(n):
    def fab(textes):
        cnt = Counter()
        for x in textes:
            t = TOK(x); cnt.update(zip(t, t[1:]))
        voc = [p for p, _ in cnt.most_common(n)]
        def f(b):
            t = TOK(b); c = Counter(zip(t, t[1:])); m = max(len(t) - 1, 1)
            return np.array([c.get(p, 0) / m for p in voc])
        return f
    return fab


def f_grammes(k, n):
    def fab(textes):
        cnt = Counter()
        for x in textes:
            cnt.update(x[i:i + k] for i in range(len(x) - k + 1))
        voc = [g for g, _ in cnt.most_common(n)]
        def f(b):
            c = Counter(b[i:i + k] for i in range(len(b) - k + 1)); m = max(len(b) - k + 1, 1)
            return np.array([c.get(g, 0) / m for g in voc])
        return f
    return fab


FEATURES = [  # ordre = ordre de simplicite, pour departager les egalites
    ('10 lisibles', True, f_lisibles),
    ('7 syntaxiques', True, f_syntaxe),
    ('lisibles + syntaxiques', True, f_les_deux),
    ('100 tokens', True, f_tokens(100)),
    ('300 tokens', True, f_tokens(300)),
    ('300 paires de tokens', False, f_paires(300)),
    ('300 4-grammes', False, f_grammes(4, 300)),
    ('800 4-grammes', False, f_grammes(4, 800)),
    ('2000 4-grammes', False, f_grammes(4, 2000)),
    ('800 3-grammes', False, f_grammes(3, 800)),
]
COMPARAISONS = ['z + Manhattan', 'z + cosinus', 'brut + cosinus']


def evaluer(app: dict, test: dict, fab, comp):
    """app, test : {dev: [blocs]}. Tout ce qui est appris l'est sur app seul."""
    f = fab([b for d in app for b in app[d]])
    X = {d: np.array([f(b) for b in app[d]]) for d in app}
    Y = {d: np.array([f(b) for b in test[d]]) for d in test}
    if comp.startswith('z'):
        pool = np.vstack(list(X.values())); mu, sd = pool.mean(0), pool.std(0); sd[sd == 0] = 1
        X = {d: (X[d] - mu) / sd for d in X}; Y = {d: (Y[d] - mu) / sd for d in Y}
    cen = {d: X[d].mean(0) for d in X}
    def dist(v, c):
        if comp.endswith('Manhattan'):
            return np.abs(v - c).mean()
        nv, nc = np.linalg.norm(v), np.linalg.norm(c)
        return 1 - v @ c / (nv * nc) if nv and nc else 1.0
    ok = n = 0
    for d in Y:
        for v in Y[d]:
            p = min(cen, key=lambda e: dist(v, cen[e])); ok += p == d; n += 1
    return ok, n


def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return 100 * (c - h), 100 * (c + h)


def selection(taille, explicables_seulement=False):
    coupe = {d: int(len(CODE[d]) * 0.6) for d in DEVS}
    APP = {d: CODE[d][:coupe[d]] for d in DEVS}
    TEST = {d: CODE[d][coupe[d]:] for d in DEVS}
    c2 = {d: int(len(APP[d]) * 0.6) for d in DEVS}
    a_in = {d: blocs(APP[d][:c2[d]], taille) for d in DEVS}
    val = {d: blocs(APP[d][c2[d]:], taille) for d in DEVS}
    a_out = {d: blocs(APP[d], taille) for d in DEVS}
    te = {d: blocs(TEST[d], taille) for d in DEVS}
    grille = [(fn, ex, fab, cp) for fn, ex, fab in FEATURES for cp in COMPARAISONS
              if ex or not explicables_seulement]
    lignes = []
    for fn, ex, fab, cp in grille:
        kv, nv = evaluer(a_in, val, fab, cp)
        kt, nt = evaluer(a_out, te, fab, cp)
        lignes.append((fn, cp, kv / nv, kt, nt))
    meilleur = max(range(len(lignes)), key=lambda i: (lignes[i][2], -i))   # egalite : le premier
    return lignes, meilleur, sum(len(v) for v in val.values()), sum(len(v) for v in te.values())


if __name__ == '__main__':
    for taille in (80, 160):
        for restreint in (False, True):
            lignes, m, nv, nt = selection(taille, restreint)
            fn, cp, sv, kt, ntt = lignes[m]
            lo, hi = wilson(kt, ntt)
            titre = 'FEATURES EXPLICABLES SEULEMENT' if restreint else 'TOUTES LES FEATURES'
            print('=' * 78)
            print(f'BLOCS DE {taille} LIGNES — {titre}   (validation : {nv} decisions, test : {nt})')
            print('=' * 78)
            print(f'  RETENUE SUR LA VALIDATION : {fn}, {cp}  (validation {sv * 100:.0f} %)')
            print(f'  TEST, UNE SEULE FOIS      : {kt}/{ntt} = {kt / ntt * 100:.0f} %   IC 95 % [{lo:.0f} ; {hi:.0f}]   hasard 33 %')
            ref = [l for l in lignes if l[0] == '800 4-grammes' and l[1] == 'z + Manhattan']
            if ref:
                r = ref[0]; print(f'  reference du talk (800 4-grammes, z + Manhattan) au test : {r[3] / r[4] * 100:.0f} %')
            ref = [l for l in lignes if l[0] == '10 lisibles' and l[1] == 'z + Manhattan']
            if ref:
                r = ref[0]; print(f'  reference du talk (10 lisibles, z + Manhattan) au test    : {r[3] / r[4] * 100:.0f} %')
            print('  toutes les methodes essayees (validation -> test) :')
            for i, (f_, c_, v_, k_, n_) in enumerate(lignes):
                print(f"    {'>' if i == m else ' '} {f_:24} {c_:15} {v_ * 100:4.0f} % -> {k_ / n_ * 100:4.0f} %")
            print()
