#!/usr/bin/env python3
"""
contre_tests.py — le contre-test du 84 %, applique aux trois mesures qui ne l'avaient
pas encore subi : la courbe (82 %), les features lisibles (58 %) et le test IA (69 / 74 / 72 %).

Ajoute le 3 novembre 2026, apres l'audit. Rien n'est change dans les protocoles
d'origine : chaque bloc rejoue d'abord la mesure TELLE QU'ELLE EST dans le notebook
(colonne « publie »), verifie qu'il retrouve le chiffre publie, puis ne change
QU'UNE chose a la fois :

  contigu   les 60 % premiers blocs en apprentissage, les 40 % derniers en test,
            au lieu d'un tirage au hasard : plus de blocs voisins des deux cotes
  glissant  la meme fenetre de test contigue, placee a 9 positions regulieres
            (toutes s'il y en a moins), puis la moyenne : moins dependant d'un
            seul decoupage
  train     vocabulaire et z-score calcules sur l'apprentissage seul
  les deux  les deux corrections a la fois
  fichier   (features lisibles seulement) aucun fichier des deux cotes

Limite propre au test IA : tout le code de la machine vient d'UN fichier. Un
decoupage par fichier y est impossible ; le decoupage contigu separe le debut et
la fin de ce fichier, c'est le mieux que ce corpus permette.

Usage :  python3 experiments/contre_tests.py            # les trois
         python3 experiments/contre_tests.py --ia       # le test IA seul (celui du notebook)
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _commun

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)

ENTETES = ('# Lignes ajoutees', '# Extraites', '# Code genere', '# Domaine :',
           '# Ce fichier', '# Le meme code', '# conserve dans')
TOK = lambda s: re.findall(r'[A-Za-z_]+|[^\sA-Za-z_]', s)
NOMS = lambda s: re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]+)\b', s)


def charger(chemin):
    return [l for l in open(chemin, encoding='utf-8').read().split('\n')
            if l.strip() and not l.startswith(ENTETES)]


CODE = {f'Dev {i}': charger(f'corpus/devs/dev_{i}.py') for i in (1, 2, 3)}
NEUF = {f'Humain neuf {i}': charger(f'corpus/neuf/humain_{i}.py') for i in (1, 2, 3)}
IA = charger('corpus/ia/assistant.py')


def blocs(L, n):
    return ['\n'.join(L[i:i + n]) for i in range(0, len(L) - n + 1, n)]


# ── 1. LE TEST IA — protocole de experiments/mesurer_signature.py ────────────
def test_ia(candidats, exclure=frozenset(), paires=True, split='alea', apprentissage='tout',
            tirages=20, seed=5, taille=40):
    B = {q: blocs(v, taille) for q, v in candidats.items()}
    k = min(len(b) for b in B.values())
    ntr = max(2, int(k * 0.6))

    def features(textes):
        alltxt = '\n'.join(textes)
        voc = [w for w, _ in Counter(TOK(alltxt)).most_common(400) if w not in exclure][:300]
        pr = ([p for p, _ in Counter(zip(TOK(alltxt), TOK(alltxt)[1:])).most_common(300)]
              if paires else [])

        def f(s):
            t = [x for x in TOK(s) if x not in exclure]
            c = Counter(t); n = max(len(t), 1)
            cp = Counter(zip(t, t[1:])); m = max(len(t) - 1, 1)
            nm = [x for x in NOMS(s) if x not in exclure]; nn = max(len(nm), 1)
            lg = Counter(min(len(x), 15) for x in nm)
            return np.array([c.get(w, 0) / n for w in voc]
                            + [cp.get(p, 0) / m for p in pr]
                            + [lg.get(i, 0) / nn for i in range(1, 16)])
        return f

    def un_essai(idx):
        tr = {q: [B[q][i] for i in idx[q][:ntr]] for q in B}
        te = {q: [B[q][i] for i in idx[q][ntr:k]] for q in B}
        if apprentissage == 'tout':      # le protocole publie : tout le texte des candidats
            f = features(['\n'.join(v) for v in candidats.values()])
            pool_src = {q: B[q][:k] for q in B}
        else:                            # vocabulaire et z-score sur l'apprentissage seul
            f = features([b for q in tr for b in tr[q]])
            pool_src = tr
        pool = np.vstack([np.array([f(b) for b in pool_src[q]]) for q in B])
        mu, sd = pool.mean(0), pool.std(0); sd[sd == 0] = 1
        cen = {q: ((np.array([f(b) for b in tr[q]]) - mu) / sd).mean(0) for q in B}
        ok = t = ia_ok = ia_t = fp = h_t = 0
        for q in B:
            for b in te[q]:
                z = (f(b) - mu) / sd
                d = {r: np.abs(z - cen[r]).mean() for r in B}
                p = min(d, key=d.get); ok += p == q; t += 1
                if q == 'IA': ia_ok += p == 'IA'; ia_t += 1
                else: fp += p == 'IA'; h_t += 1
        return ok / t, ia_ok / ia_t, t, fp / h_t

    if split == 'contigu':
        acc, ia, t, fp = un_essai({q: list(range(k)) for q in B})
        return acc, ia, k, t, 1, fp
    if split == 'glissant':
        # la fenetre de test (k - ntr blocs consecutifs) glisse sur toutes les positions
        A = []; I = []; F = []
        for s0 in sorted(set(np.linspace(0, ntr, min(ntr + 1, 9)).astype(int))):   # au plus 9 positions
            te = list(range(s0, s0 + k - ntr)); tr = [i for i in range(k) if i not in te]
            acc, ia, t, fp = un_essai({q: tr + te for q in B})
            A.append(acc); I.append(ia); F.append(fp)
        return float(np.mean(A)), float(np.mean(I)), k, t, len(A), float(np.mean(F))
    rng = np.random.default_rng(seed); A = []; I = []; F = []
    for _ in range(tirages):
        acc, ia, t, fp = un_essai({q: rng.permutation(k) for q in B})
        A.append(acc); I.append(ia); F.append(fp)
    return float(np.mean(A)), float(np.mean(I)), k, t, tirages, float(np.mean(F))


# ── 2. LA COURBE — protocole de la cellule 19 du notebook (Delta de Burrows) ──
_TOKC = {d: TOK('\n'.join(CODE[d])) for d in CODE}
_PAR_LIGNE = sum(len(t) for t in _TOKC.values()) / sum(len(CODE[d]) for d in CODE)


def courbe(taille, split='alea', apprentissage='tout', tirages=30, seed=42):
    DEVS = list(CODE)
    B = {d: [_TOKC[d][i:i + taille] for i in range(0, len(_TOKC[d]) - taille + 1, taille)] for d in DEVS}
    k = min(len(b) for b in B.values())
    if k < 6:
        return None
    ntr = max(2, int(k * 0.6))

    def essai(idx):
        tr = {d: [B[d][i] for i in idx[d][:ntr]] for d in DEVS}
        te = {d: [B[d][i] for i in idx[d][ntr:k]] for d in DEVS}
        if apprentissage == 'tout':
            VOC = [w for w, _ in sum((Counter(t) for t in _TOKC.values()), Counter()).most_common(150)]
            src = {d: B[d][:k] for d in DEVS}
        else:
            VOC = [w for w, _ in sum((Counter(b) for d in DEVS for b in tr[d]), Counter()).most_common(150)]
            src = tr
        fr = lambda b: (lambda c: [c[w] / taille for w in VOC])(Counter(b))
        pool = np.array([fr(b) for d in DEVS for b in src[d]])
        mu, sd = pool.mean(0), pool.std(0); sd[sd == 0] = 1
        cen = {d: ((np.array([fr(b) for b in tr[d]]) - mu) / sd).mean(0) for d in DEVS}
        bon = tot = 0
        for d in DEVS:
            for b in te[d]:
                z = (np.array(fr(b)) - mu) / sd
                dd = {e: np.abs(z - cen[e]).mean() for e in DEVS}
                bon += min(dd, key=dd.get) == d; tot += 1
        return bon / tot

    if split == 'contigu':
        return 100 * essai({d: list(range(k)) for d in DEVS})
    if split == 'glissant':
        R = []
        for s0 in sorted(set(np.linspace(0, ntr, min(ntr + 1, 9)).astype(int))):   # au plus 9 positions
            te = list(range(s0, s0 + k - ntr)); tr = [i for i in range(k) if i not in te]
            R.append(essai({d: tr + te for d in DEVS}))
        return 100 * float(np.mean(R))
    rng = np.random.default_rng(seed)
    return 100 * float(np.mean([essai({d: rng.permutation(k) for d in DEVS}) for _ in range(tirages)]))


if __name__ == '__main__':
    QUOI = {'--courbe', '--lisibles', '--ia'} & set(sys.argv[1:]) or {'--courbe', '--lisibles', '--ia'}
    pc = lambda x: f'{x:5.0f} %' if x is not None else '    — '

    if '--courbe' in QUOI:
        print('=' * 74)
        print('1. LA COURBE (Delta de Burrows, 150 tokens, 3 devs Django) — hasard 33 %')
        print('=' * 74)
        print(f"{'tokens':>7} {'lignes':>7}   {'publie':>7} {'contigu':>8} {'glissant':>8} {'train':>7} {'glis.+train':>11}")
        for T in (50, 100, 200, 400, 800, 1600):
            r = [courbe(T), courbe(T, 'contigu'), courbe(T, 'glissant'), courbe(T, 'alea', 'train'), courbe(T, 'glissant', 'train')]
            print(f'{T:>7} {T / _PAR_LIGNE:>7.0f}   ' + ' '.join(f'{pc(x):>8}' for x in r))
        print()

    if '--lisibles' in QUOI:
        print('=' * 74)
        print('2. LES 10 FEATURES LISIBLES (experiments/_commun.py) — hasard 33 %')
        print('=' * 74)
        code, origine = _commun.charger_devs()
        print(f"{'bloc':>5}   {'alea':>6} {'contigu':>8} {'fichier':>8}    (alea et fichier : moyenne sur 7 graines)")
        for T in (80, 160):
            a = _commun.precision(code, T, 'lisibles')[0]
            c = _commun.precision(code, T, 'lisibles', split='contigu')[0]
            f = _commun.precision(code, T, 'lisibles', split='fichier', origine=origine)[0]
            print(f'{T:>5}   ' + ' '.join(f'{pc(x):>8}' for x in (a, c, f)))
        print()

    if '--ia' in QUOI:
        print('=' * 74)
        print('3. LE TEST IA (8 blocs de 40 lignes par candidat) — hasard 25 %')
        print('=' * 74)
        EX = frozenset({'def', 'class', 'return', 'import', 'from', 'self'})
        C1 = dict(CODE); C1['IA'] = IA
        C3 = dict(NEUF); C3['IA'] = IA
        mesures = [('IA contre 3 devs de production', C1, frozenset(), True),
                   ('idem, sans def/class/return/import/from/self', C1, EX, False),
                   ('IA contre 3 humains neufs', C3, frozenset(), False)]
        print(f"{'':46} {'publie':>8} {'contigu':>8} {'glissant':>9} {'train':>8} {'glis.+train':>12}")
        for nom, C, ex, pr in mesures:
            r = [test_ia(C, ex, pr), test_ia(C, ex, pr, 'contigu'), test_ia(C, ex, pr, 'glissant'),
                 test_ia(C, ex, pr, 'alea', 'train'), test_ia(C, ex, pr, 'glissant', 'train')]
            print(f'{nom:46} ' + ' '.join(f'{x[0] * 100:>7.0f}%' for x in r))
            print(f"{'   dont blocs IA reconnus':46} " + ' '.join(f'{x[1] * 100:>7.0f}%' for x in r))
            print(f"{'   blocs humains pris pour l IA':46} " + ' '.join(f'{x[5] * 100:>7.0f}%' for x in r))
        k, t = r[0][2], r[0][3]
        print()
        print(f'  {k} blocs par candidat, {t} decisions de test par essai.')
        print('  « contigu » = UN seul essai, deterministe : un bloc de plus ou de moins')
        print(f'  bien classe fait bouger le score de {100 / t:.1f} points.')
        print('  « glissant » = la fenetre de test contigue placee a chaque position')
        print(f'  possible ({r[2][4]} ici), puis la moyenne : aucun bloc voisin tire au hasard.')
