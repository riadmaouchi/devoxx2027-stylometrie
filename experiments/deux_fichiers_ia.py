#!/usr/bin/env python3
"""
deux_fichiers_ia.py — l'objection du fichier unique.

Tout le code « IA » du talk venait d'UN fichier, genere par UN modele (ChatGPT) en UNE
conversation. Un classifieur qui reconnait ses blocs peut reconnaitre « ce fichier-la »
— ses identifiants, son sujet — plutot que « une machine ».

Le test qui repond : un SECOND fichier, d'un AUTRE modele (Claude), meme domaine, un seul
prompt, aucune consigne de style, ecrit par un agent qui ne connaissait ni le talk ni
l'experience (le prompt exact est en tete de corpus/ia/assistant_2.py). Puis :

  A. le test publie, rejoue sur le second fichier seul ;
  B. APPRENDRE sur un fichier, TESTER sur l'autre : les blocs du fichier jamais vu
     sont-ils classes « IA » ? Vocabulaire et z-score sur l'apprentissage seul.
     Les humains : 60 % de leurs blocs en apprentissage, 40 % en test, fenetre
     contigue glissante (le protocole durci de contre_tests.py) ;
  C. les 7 mesures syntaxiques de la slide 15 sur le second fichier.

Usage :  python3 experiments/deux_fichiers_ia.py
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contre_tests import CODE, NEUF, IA, TOK, NOMS, blocs, charger, test_ia

IA2 = charger('corpus/ia/assistant_2.py')
TAILLE = 40


def croise(humains, ia_train, ia_test, exclure=frozenset(), paires=True):
    """Apprendre la classe IA sur ia_train, tester sur ia_test (autre fichier).
    Humains : fenetre de test contigue glissante. Renvoie (ia reconnus, humains pris pour l IA, precision 4 classes)."""
    Bh = {q: blocs(v, TAILLE) for q, v in humains.items()}
    Ba, Bb = blocs(ia_train, TAILLE), blocs(ia_test, TAILLE)
    k = min(min(len(b) for b in Bh.values()), len(Ba), len(Bb))
    ntr = max(2, int(k * 0.6))
    R = []
    for s0 in sorted(set(np.linspace(0, ntr, min(ntr + 1, 9)).astype(int))):
        te_i = list(range(s0, s0 + k - ntr)); tr_i = [i for i in range(k) if i not in te_i]
        tr = {q: [Bh[q][i] for i in tr_i] for q in Bh}; tr['IA'] = Ba[:k]
        te = {q: [Bh[q][i] for i in te_i] for q in Bh}; te['IA'] = Bb[:k]
        alltxt = '\n'.join(b for q in tr for b in tr[q])
        voc = [w for w, _ in Counter(TOK(alltxt)).most_common(400) if w not in exclure][:300]
        pr = ([p for p, _ in Counter(zip(TOK(alltxt), TOK(alltxt)[1:])).most_common(300)] if paires else [])

        def f(s):
            t = [x for x in TOK(s) if x not in exclure]
            c = Counter(t); n = max(len(t), 1)
            cp = Counter(zip(t, t[1:])); m = max(len(t) - 1, 1)
            nm = [x for x in NOMS(s) if x not in exclure]; nn = max(len(nm), 1)
            lg = Counter(min(len(x), 15) for x in nm)
            return np.array([c.get(w, 0) / n for w in voc] + [cp.get(p, 0) / m for p in pr]
                            + [lg.get(i, 0) / nn for i in range(1, 16)])
        pool = np.vstack([np.array([f(b) for b in tr[q]]) for q in tr])
        mu, sd = pool.mean(0), pool.std(0); sd[sd == 0] = 1
        cen = {q: ((np.array([f(b) for b in tr[q]]) - mu) / sd).mean(0) for q in tr}
        ok = t = ia = fp = nh = 0
        for q in te:
            for b in te[q]:
                z = (f(b) - mu) / sd
                d = {r: np.abs(z - cen[r]).mean() for r in cen}
                p = min(d, key=d.get); ok += p == q; t += 1
                if q == 'IA': ia += p == 'IA'
                else: fp += p == 'IA'; nh += 1
        R.append((ia / len(te['IA']), fp / nh, ok / t))
    R = np.array(R)
    return R[:, 0].mean(), R[:, 1].mean(), R[:, 2].mean(), k, len(te['IA']), len(R)


def feats(t):
    L = [l for l in t.split('\n') if l.strip()]
    n = max(len(L), 1)
    nf = max(len(re.findall(r'\bdef\s', t)), 1)
    noms = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]+)\b', t)
    return {
        'lignes/fonction': n / nf,
        'ternaire /100l': 100 * len(re.findall(r'=\s*[^\n=]+\bif\b[^\n]+\belse\b', t)) / n,
        'comprehension /100l': 100 * (len(re.findall(r'\[[^\]\n]+\bfor\b[^\]\n]+\bin\b[^\]\n]+\]', t))
                                      + len(re.findall(r'\{[^}\n]+\bfor\b[^}\n]+\bin\b[^}\n]+\}', t))) / n,
        'type hints /100l': 100 * len(re.findall(r':\s*(?:int|str|float|bool|list|dict|tuple)\b', t)) / n,
        'except /100l': 100 * len(re.findall(r'\bexcept\b', t)) / n,
        'commentaires %': 100 * sum(1 for l in L if l.strip().startswith('#')) / n,
        'noms 1-2 car. %': 100 * sum(1 for x in noms if len(x) <= 2) / max(len(noms), 1),
    }


if __name__ == '__main__':
    print(f'Fichier 1 (ChatGPT) : {len(IA)} lignes non vides  ·  fichier 2 (Claude) : {len(IA2)} lignes non vides\n')
    EX = frozenset({'def', 'class', 'return', 'import', 'from', 'self'})
    C = [('contre 3 devs de production', CODE, frozenset(), True),
         ('idem, sans def/class/return/import/from/self', CODE, EX, False),
         ('contre 3 humains neufs', NEUF, frozenset(), False)]

    print('=' * 78)
    print('A. LE TEST PUBLIE, REJOUE SUR LE SECOND FICHIER — hasard 25 %')
    print('=' * 78)
    print(f"{'':46} {'publie':>8} {'glissant':>9}   (blocs IA reconnus)")
    for nom, H, ex, pr in C:
        c = dict(H); c['IA'] = IA2
        a, g = test_ia(c, ex, pr), test_ia(c, ex, pr, 'glissant')
        print(f'{nom:46} {a[0] * 100:>7.0f}% {g[0] * 100:>8.0f}%   ({a[1] * 100:.0f} % / {g[1] * 100:.0f} %)')
    print()

    print('=' * 78)
    print('B. APPRENDRE SUR UN FICHIER, TESTER SUR L AUTRE')
    print('=' * 78)
    print(f"{'':46} {'IA reconnus':>12} {'humains -> IA':>14} {'4 classes':>10}")
    for sens, a_, b_ in (('ChatGPT -> Claude', IA, IA2), ('Claude -> ChatGPT', IA2, IA)):
        print(f'  apprend sur {sens.split(" -> ")[0]}, teste sur {sens.split(" -> ")[1]}')
        for nom, H, ex, pr in C:
            ia, fp, acc, k, nte, npos = croise(H, a_, b_, ex, pr)
            print(f'    {nom:42} {ia * 100:>11.0f}% {fp * 100:>13.0f}% {acc * 100:>9.0f}%')
    print(f'\n  {k} blocs de {TAILLE} lignes par candidat ; {nte} blocs du fichier jamais vu par essai ; '
          f'{npos} positions de la fenetre humaine.')
    print()

    print('=' * 78)
    print('C. LES 7 MESURES SYNTAXIQUES — les deux machines contre la plage des 6 humains')
    print('=' * 78)
    H = {**{k: '\n'.join(v) for k, v in CODE.items()}, **{k: '\n'.join(v) for k, v in NEUF.items()}}
    FH = {k: feats(t) for k, t in H.items()}
    F1, F2 = feats('\n'.join(IA)), feats('\n'.join(IA2))
    print(f"  {'mesure':<22}{'ChatGPT':>9}{'Claude':>9}   {'humains min-max':>17}   verdict pour Claude")
    for c in F1:
        v = [FH[k][c] for k in FH]; lo, hi = min(v), max(v)
        verdict = 'DANS la plage' if lo <= F2[c] <= hi else ('AU-DESSUS' if F2[c] > hi else 'EN DESSOUS')
        print(f'  {c:<22}{F1[c]:>9.2f}{F2[c]:>9.2f}   {lo:>7.2f} - {hi:<7.2f}   {verdict}')
