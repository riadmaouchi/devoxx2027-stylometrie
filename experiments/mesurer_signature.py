#!/usr/bin/env python3
"""Mesure : (a) le test IA reproduit sur le corpus SAIN, (b) en quoi consiste
concretement la signature — quels tokens la machine surutilise et sous-utilise."""
import re, os
import numpy as np
from collections import Counter

import pathlib
os.chdir(pathlib.Path(__file__).resolve().parents[1])  # racine du repo

ENTETES = ('# Lignes ajoutees', '# Extraites', '# Code genere', '# Domaine :',
           '# Ce fichier', '# Le meme code', '# conserve dans')

def charger(chemin):
    """Lignes non vides. On ne retire QUE les en-tetes que j'ai ajoutes moi-meme :
    les commentaires des auteurs sont une feature, pas du bruit."""
    return [l for l in open(chemin, encoding='utf-8').read().split('\n')
            if l.strip() and not l.startswith(ENTETES)]

CODE = {f'Dev {i}': charger(f'corpus/devs/dev_{i}.py') for i in (1, 2, 3)}
NEUF = {f'Humain neuf {i}': charger(f'corpus/neuf/humain_{i}.py') for i in (1, 2, 3)}
IA   = charger('corpus/ia/assistant.py')

print(f'IA (corpus sain) : {len(IA)} lignes')
for k, v in CODE.items(): print(f'  {k}: {len(v):,}')
for k, v in NEUF.items(): print(f'  {k}: {len(v):,}')
print()

def blocs(L, n):
    return ['\n'.join(L[i:i+n]) for i in range(0, len(L)-n+1, n)]

TOK = lambda s: re.findall(r'[A-Za-z_]+|[^\sA-Za-z_]', s)
NOMS = lambda s: re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]+)\b', s)

TAILLE = 40

def experience(candidats, exclure=frozenset(), paires=True, tirages=20, seed=5):
    B = {q: blocs(v, TAILLE) for q, v in candidats.items()}
    k = min(len(b) for b in B.values())
    alltxt = '\n'.join('\n'.join(v) for v in candidats.values())
    voc = [w for w, _ in Counter(TOK(alltxt)).most_common(400) if w not in exclure][:300]
    pr = ([p for p, _ in Counter(zip(TOK(alltxt), TOK(alltxt)[1:])).most_common(300)]
          if paires else [])
    def f(s):
        t = [x for x in TOK(s) if x not in exclure]
        c = Counter(t); n = max(len(t), 1)
        cp = Counter(zip(t, t[1:])); m = max(len(t)-1, 1)
        nm = [x for x in NOMS(s) if x not in exclure]; nn = max(len(nm), 1)
        lg = Counter(min(len(x), 15) for x in nm)
        return np.array([c.get(w, 0)/n for w in voc]
                        + [cp.get(p, 0)/m for p in pr]
                        + [lg.get(i, 0)/nn for i in range(1, 16)])
    X = {q: np.array([f(b) for b in B[q][:k]]) for q in B}
    pool = np.vstack(list(X.values())); mu, sd = pool.mean(0), pool.std(0); sd[sd == 0] = 1
    Z = {q: (X[q]-mu)/sd for q in X}
    rng = np.random.default_rng(seed); ntr = max(2, int(k*0.6))
    acc = []; conf = Counter(); tot = 0
    for _ in range(tirages):
        idx = {q: rng.permutation(k) for q in Z}
        cen = {q: Z[q][idx[q][:ntr]].mean(0) for q in Z}
        ok = t = 0
        for q in Z:
            for i in idx[q][ntr:]:
                d = {r: np.abs(Z[q][i]-cen[r]).mean() for r in Z}
                p = min(d, key=d.get); ok += p == q; t += 1
                if q == 'IA': conf[p] += 1; tot += 1
        acc.append(ok/t)
    return float(np.mean(acc)), k, conf, tot

print('='*66)
print('A. LE TEST IA, REPRODUIT SUR LE CORPUS SAIN')
print('='*66)
C1 = dict(CODE); C1['IA'] = IA
a1, k1, cf1, t1 = experience(C1)
print(f'IA vs 3 devs production : {a1*100:.0f} %  (hasard 25 %, {a1*100/25:.1f}x)  k={k1} blocs/candidat')
print(f'   blocs IA attribues a : ' + '  '.join(f'{q} {v*100//t1} %' for q, v in cf1.most_common()))

EX = {'def', 'class', 'return', 'import', 'from', 'self'}
a2, _, _, _ = experience(C1, exclure=EX, paires=False)
print(f'contre-test sans def/class/return/import/from/self : {a2*100:.0f} %  ({a2*100/25:.1f}x)')

C3 = dict(NEUF); C3['IA'] = IA
a3, k3, cf3, t3 = experience(C3, paires=False)
print(f'IA vs 3 humains NEUFS   : {a3*100:.0f} %  ({a3*100/25:.1f}x)  k={k3} blocs/candidat')
print(f'   blocs IA bien identifies : {cf3["IA"]*100//t3} %')
print()

print('='*66)
print("B. A QUOI ELLE SE RECONNAIT — tokens sur/sous-utilises")
print('='*66)
humains = '\n'.join('\n'.join(v) for v in list(CODE.values()) + list(NEUF.values()))
ia_txt = '\n'.join(IA)
th, ti = TOK(humains), TOK(ia_txt)
ch, ci = Counter(th), Counter(ti)
nh, ni = len(th), len(ti)
print(f'tokens humains {nh:,}  ·  tokens IA {ni:,}')
print()

# On ne regarde que les tokens assez frequents pour que le ratio ait un sens
cands = [w for w in set(ch) | set(ci) if ch[w] + ci[w] >= 40]
rows = []
for w in cands:
    fh, fi = ch[w]/nh, ci[w]/ni
    # lissage +1 sur les COMPTES, le meme que dans le notebook : un lissage a
    # 1e-6 sur les frequences fabrique des « x1500 » des qu'un compte vaut zero.
    r = ((ci[w] + 1) / ni) / ((ch[w] + 1) / nh)
    rows.append((w, fh*1000, fi*1000, r, ch[w], ci[w]))
rows.sort(key=lambda x: (-x[3], x[0]))   # ex aequo : ordre alphabetique

def montre(sub, titre):
    print(titre)
    print(f"  {'token':<14}{'humains /1000':>15}{'IA /1000':>11}{'ratio':>9}{'n_h':>7}{'n_ia':>7}")
    for w, fh, fi, r, a, b in sub:
        aff = repr(w) if not w.isalnum() and w != '_' else w
        print(f'  {aff:<14}{fh:>15.2f}{fi:>11.2f}{r:>8.1f}x{a:>7}{b:>7}')
    print()

montre(rows[:12], 'SURUTILISES par la machine')
montre(rows[-12:][::-1], 'SOUS-UTILISES par la machine')

print('='*66)
print('C. LONGUEUR DES IDENTIFIANTS')
print('='*66)
nh_, ni_ = NOMS(humains), NOMS(ia_txt)
print(f'  humains : moyenne {np.mean([len(x) for x in nh_]):.2f} caracteres, mediane {np.median([len(x) for x in nh_]):.0f}')
print(f'  IA      : moyenne {np.mean([len(x) for x in ni_]):.2f} caracteres, mediane {np.median([len(x) for x in ni_]):.0f}')
un_h = sum(1 for x in nh_ if len(x) <= 2)/len(nh_)
un_i = sum(1 for x in ni_ if len(x) <= 2)/len(ni_)
print(f'  identifiants de 1-2 caracteres : humains {un_h*100:.1f} %  ·  IA {un_i*100:.1f} %')
print()

print('='*66)
print('D. QUELQUES FEATURES LISIBLES, MESUREES')
print('='*66)
def stats(txt, label):
    lignes = [l for l in txt.split('\n') if l.strip()]
    n = len(lignes)
    nfun = max(len(re.findall(r'\bdef\s', txt)), 1)
    d = {
        'lignes non vides': n,
        'fonctions': nfun,
        'lignes/fonction': round(n/nfun, 1),
        'commentaires %': round(100*sum(1 for l in lignes if l.strip().startswith('#'))/n, 1),
        'docstrings /100l': round(100*len(re.findall(r'"""', txt))/2/n, 1),
        'type hints /100l': round(100*len(re.findall(r':\s*(int|str|float|bool|list|dict|tuple)', txt))/n, 1),
        'list comp /100l': round(100*len(re.findall(r'\[[^\]]+for [^\]]+in [^\]]+\]', txt))/n, 1),
        'dict comp /100l': round(100*len(re.findall(r'\{[^}]+for [^}]+in [^}]+\}', txt))/n, 1),
        'f-strings /100l': round(100*len(re.findall(r"f['\"]", txt))/n, 1),
        'try/except /100l': round(100*len(re.findall(r'\bexcept\b', txt))/n, 1),
        'ternaires /100l': round(100*len(re.findall(r'\bif\b[^\n]+\belse\b', txt))/n, 1),
    }
    print(f'  {label}')
    for k2, v in d.items(): print(f'     {k2:<20}{v}')
    return d
sh = stats(humains, 'HUMAINS (6 fichiers, production + neuf)')
si = stats(ia_txt, 'IA (1 fichier, 452 lignes)')
print()
print('  RATIOS IA / humains sur les features normalisees :')
for k2 in si:
    if '/100l' in k2 or '%' in k2 or k2 == 'lignes/fonction':
        if sh[k2]: print(f'     {k2:<20}{si[k2]/sh[k2]:.1f}x')
