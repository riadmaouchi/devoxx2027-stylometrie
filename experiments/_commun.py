"""
_commun.py — un seul protocole de mesure, partage par les scripts de controle.

Toujours la meme chose : des blocs de N lignes, des features, un z-score appris
sur l'APPRENTISSAGE SEUL, un centroide par classe, la distance de Manhattan, le
plus proche centroide. Ce qui change d'un controle a l'autre, c'est uniquement
la facon de separer l'apprentissage du test :

  alea     blocs tires au hasard (le protocole du notebook)
  contigu  les 60 % premiers blocs en apprentissage, les 40 % derniers en test :
           des mois de commits entre les deux
  fichier  apprentissage et test sur des FICHIERS differents : aucun fichier
           n'est des deux cotes
"""
from __future__ import annotations

import os
import re
from collections import Counter

import numpy as np


RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_TETE = ('# Lignes ajoutees', '# Extraites')
GRAINES = (7, 11, 23, 42, 101, 2024, 31337)
N_GRAMMES = 800


# ── les 10 features, copiées telles quelles depuis le notebook ───────────────
def sig(src: str) -> list[float]:
    lines = src.split('\n')
    ne = [l for l in lines if l.strip()]
    n = max(len(ne), 1)
    names = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]+)\b', src)
    nn = max(len(names), 1)
    nfun = max(len(re.findall(r'\bdef\s', src)), 1)
    return [
        len(re.findall(r'[a-z][A-Z]', src)) / nn,
        len([x for x in names if '_' in x and x == x.lower() and len(x) > 2]) / nn,
        sum(1 for l in lines if l.strip().startswith('#')) / n,
        len(re.findall(r':\s*(int|str|float|bool|list|dict|tuple)', src)) / n,
        len(re.findall(r'"""', src)) / n,
        len(re.findall(r'\[.+for .+in .+\]', src)) / n,
        len(re.findall(r'==\s*None|!=\s*None', src)) / n,
        len(re.findall(r'range\s*\(\s*len\s*\(', src)) / n,
        len(re.findall(r'\bwith\s+open', src)) / n,
        min(len(ne) / nfun / 12, 1.0),
    ]


def charger_devs():
    """({dev: [lignes]}, {dev: [(date, chemin)]}) — une origine par ligne."""
    code, origine = {}, {}
    for i in (1, 2, 3):
        base = os.path.join(RACINE, 'corpus', 'devs', f'dev_{i}')
        L = [l for l in open(base + '.py', encoding='utf-8').read().split('\n')
             if l.strip() and not l.startswith(EN_TETE)]
        O = [tuple(l.split('\t')) for l in open(base + '.origine.tsv', encoding='utf-8')
             .read().split('\n') if l]
        if len(L) != len(O):
            raise SystemExit(f'dev_{i} : {len(L)} lignes mais {len(O)} origines — '
                             f'relancer experiments/construire_corpus.py --ecrire')
        code[f'Dev {i}'], origine[f'Dev {i}'] = L, O
    return code, origine


def paquet(chemin: str) -> str:
    q = chemin.split('/')
    if len(q) > 3 and q[1] == 'contrib':
        return 'contrib/' + q[2]
    return q[1].replace('.py', '')


def blocs(L, n):
    return ['\n'.join(L[i:i + n]) for i in range(0, len(L) - n + 1, n)]


def _grammes(s):
    return Counter(s[i:i + 4] for i in range(len(s) - 3))


def classer(train: dict, test: dict, feat: str, vocab: str = 'train') -> float:
    """train / test : {classe: [blocs]}. Renvoie la precision sur le test."""
    noms = list(train)
    if feat == 'lisibles':
        X = {d: np.array([sig(b) for b in train[d]]) for d in noms}
        Y = {d: np.array([sig(b) for b in test[d]]) for d in noms}
    else:
        ctr = {d: [_grammes(b) for b in train[d]] for d in noms}
        cte = {d: [_grammes(b) for b in test[d]] for d in noms}
        g = Counter()
        for d in noms:
            for c in ctr[d] + (cte[d] if vocab == 'tout' else []):
                g.update(c)
        V = [x for x, _ in g.most_common(N_GRAMMES)]
        v = lambda c, b: np.array([c.get(x, 0) / max(len(b) - 3, 1) for x in V])
        X = {d: np.array([v(c, b) for c, b in zip(ctr[d], train[d])]) for d in noms}
        Y = {d: np.array([v(c, b) for c, b in zip(cte[d], test[d])]) for d in noms}
    pool = np.vstack([X[d] for d in noms])
    mu, sd = pool.mean(0), pool.std(0)
    sd[sd == 0] = 1
    cen = {d: ((X[d] - mu) / sd).mean(0) for d in noms}
    ok = t = 0
    for d in noms:
        for y in (Y[d] - mu) / sd:
            dist = {e: np.abs(y - cen[e]).mean() for e in noms}
            ok += min(dist, key=dist.get) == d
            t += 1
    return ok / t


def precision(corpus: dict, taille: int, feat: str, split: str = 'alea',
              vocab: str = 'train', origine: dict | None = None, graines=GRAINES):
    """(precision en %, nb de blocs de test par classe). None si trop peu de blocs."""
    noms = list(corpus)
    if split == 'fichier':
        res, kte_min = [], None
        for g in graines:
            rng = np.random.default_rng(g)
            tr, te = {}, {}
            for d in noms:
                par_fichier = {}
                for l, (_, ch) in zip(corpus[d], origine[d]):
                    par_fichier.setdefault(ch, []).append(l)
                fichiers = list(par_fichier)
                rng.shuffle(fichiers)
                a, b, seuil = [], [], 0.6 * len(corpus[d])
                for f in fichiers:
                    (a if len(a) < seuil else b).extend(par_fichier[f])
                tr[d], te[d] = blocs(a, taille), blocs(b, taille)
            ktr, kte = min(len(tr[d]) for d in noms), min(len(te[d]) for d in noms)
            if ktr < 4 or kte < 3:
                return None, 0
            kte_min = kte if kte_min is None else min(kte_min, kte)
            res.append(classer({d: tr[d][:ktr] for d in noms}, {d: te[d][:kte] for d in noms},
                               feat, vocab))
        return 100 * float(np.mean(res)), kte_min
    B = {d: blocs(corpus[d], taille) for d in noms}
    k = min(len(B[d]) for d in noms)
    ntr = max(2, int(k * 0.6))
    if k < 8:
        return None, 0
    if split == 'contigu':
        return 100 * classer({d: B[d][:ntr] for d in noms}, {d: B[d][ntr:k] for d in noms},
                             feat, vocab), k - ntr
    res = []
    for g in graines:
        rng = np.random.default_rng(g)
        idx = {d: rng.permutation(k) for d in noms}
        res.append(classer({d: [B[d][i] for i in idx[d][:ntr]] for d in noms},
                           {d: [B[d][i] for i in idx[d][ntr:]] for d in noms}, feat, vocab))
    return 100 * float(np.mean(res)), k - ntr
