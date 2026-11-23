#!/usr/bin/env python3
"""
piege_projet.py — PIÈGE 3 / 4 : « le projet ».

LA QUESTION. Un score d'attribution eleve prouve-t-il qu'on reconnait une
PERSONNE ? Ou reconnait-on aussi bien un projet, voire un simple sous-paquet ?

  CONDITION A — 3 contributeurs du MÊME dépôt (django/django, corpus contrôlé).
  CONDITION B — 3 PROJETS différents (django / requests / PyYAML).
  CONDITION C — 3 SOUS-PAQUETS d'un même projet (werkzeug). Aucune personne
                ici : seulement trois sujets. C'est le témoin.

Même protocole, même nombre de blocs dans les trois conditions, donc même
hasard (33 %). Deux jeux de features, parce qu'ils ne répondent pas pareil :
  - les 10 features lisibles de `sig()` ;
  - les 800 4-grammes de caractères, ceux qui « marchent ».

Les corpus B et C sont figés dans corpus/projets/ : le script tourne hors-ligne.

Usage :  python3 experiments/piege_projet.py
"""
from __future__ import annotations

import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _commun import precision as precision_commune, sig   # sig : les 10 features lisibles

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAILLES = (60, 80, 100, 120)   # plusieurs granularites : le resultat doit tenir
TIRAGES = 20
GRAINES = (7, 11, 23, 42, 101, 2024, 31337)
TAILLE_BLOC = 80


def blocs(lignes: list[str], n: int) -> list[str]:
    return ['\n'.join(lignes[i:i + n]) for i in range(0, len(lignes) - n + 1, n)]


def precision(corpus: dict[str, list[str]], taille=TAILLE_BLOC,
              tirages=TIRAGES, graine=7, kmax=None):
    """Précision held-out, protocole identique au notebook."""
    noms = list(corpus)
    B = {d: blocs(corpus[d], taille) for d in noms}
    k = min(len(B[d]) for d in noms)
    if kmax:
        k = min(k, kmax)
    if k < 8:
        return None, 0
    X = {d: np.array([sig(b) for b in B[d][:k]]) for d in noms}
    pool = np.vstack([X[d] for d in noms])
    mu, sd = pool.mean(0), pool.std(0)
    sd[sd == 0] = 1
    Z = {d: (X[d] - mu) / sd for d in noms}
    rng = np.random.default_rng(graine)
    ntr = max(2, int(k * 0.6))
    accs = []
    for _ in range(tirages):
        idx = {d: rng.permutation(k) for d in noms}
        cen = {d: Z[d][idx[d][:ntr]].mean(0) for d in noms}
        ok = t = 0
        for d in noms:
            for i in idx[d][ntr:]:
                dist = {e: np.abs(Z[d][i] - cen[e]).mean() for e in noms}
                ok += min(dist, key=dist.get) == d
                t += 1
        accs.append(ok / t)
    return float(np.mean(accs)), k


# ── les deux corpus ──────────────────────────────────────────────────────────
def contributeurs() -> dict[str, list[str]]:
    out = {}
    for i in (1, 2, 3):
        p = os.path.join(RACINE, 'corpus', 'devs', f'dev_{i}.py')
        out[f'Dev {i}'] = [l for l in open(p, encoding='utf-8').read().split('\n')
                           if l.strip()
                           and not l.startswith('# Lignes ajoutees')
                           and not l.startswith('# Extraites')]
    return out


def corpus_projet(nom: str) -> list[str]:
    """Un corpus « projet », fige dans corpus/projets/ — aucune dependance
    sur ce qui est installe, le notebook doit tourner hors-ligne."""
    p = os.path.join(RACINE, 'corpus', 'projets', f'{nom}.py')
    if not os.path.exists(p):
        return []
    return [l for l in open(p, encoding='utf-8').read().split('\n')
            if l.strip() and not l.startswith('# Corpus « projet »')
            and not l.startswith('# Licence') and not l.startswith('# Utilise')
            and not l.startswith('# Hors ecosysteme')]


def corpus_temoin(sous: str) -> list[str]:
    """Un sous-paquet du MEME projet, fige lui aussi — le temoin de la condition C."""
    p = os.path.join(RACINE, 'corpus', 'projets', f'werkzeug_{sous}.py')
    if not os.path.exists(p):
        return []
    return [l for l in open(p, encoding='utf-8').read().split('\n')
            if l.strip() and not l.startswith('# Corpus « temoin »')
            and not l.startswith('# Licence') and not l.startswith('# condition B')]


def main() -> int:
    A = contributeurs()
    B = {'django Dev 1': A['Dev 1'],
         'requests': corpus_projet('requests'),
         'PyYAML': corpus_projet('pyyaml')}
    C = {'werkzeug/sansio': corpus_temoin('sansio'),
         'werkzeug/routing': corpus_temoin('routing'),
         'werkzeug/debug': corpus_temoin('debug')}

    for nom, D in (('A', A), ('B', B), ('C', C)):
        if any(len(v) < 600 for v in D.values()):
            print(f'Corpus insuffisant pour la condition {nom}.')
            return 1

    print('PIEGE 3 / 4 — « le projet ». Mesure, pas affirmation.')
    print()
    print('  A  trois PERSONNES, meme depot (django/django)')
    print('  B  trois PROJETS differents (django / requests / PyYAML)')
    print('  C  trois SOUS-PAQUETS du meme projet (werkzeug)  <- temoin, aucune personne')
    print()
    print(f'  Meme protocole, MEME nombre de blocs partout, {len(GRAINES)} graines. Hasard = 33 %.')
    print()
    print(f"{'':>19}{'10 FEATURES LISIBLES':^27}{'800 4-GRAMMES':^27}")
    print(f"{'lignes/bloc':>12}{'blocs':>7}" + f"{'A':>9}{'B':>9}{'C':>9}" * 2)
    print('-' * 73)
    L, G = {l: [] for l in 'ABC'}, {l: [] for l in 'ABC'}
    for taille in TAILLES:
        k = min(min(len(blocs(v, taille)) for v in D.values()) for D in (A, B, C))
        if k < 8:
            continue
        ligne = f'{taille:>12}{k:>7}'
        for lbl, D in (('A', A), ('B', B), ('C', C)):
            v = float(np.mean([precision(D, taille=taille, graine=g, kmax=k)[0] * 100
                               for g in GRAINES]))
            L[lbl].append(v)
            ligne += f'{v:>8.0f}%'
        for lbl, D in (('A', A), ('B', B), ('C', C)):
            egal = {d: x[:k * taille] for d, x in D.items()}       # memes blocs partout
            v = precision_commune(egal, taille, 'ngrammes')[0]
            G[lbl].append(v)
            ligne += f'{v:>8.0f}%'
        print(ligne)
    print('-' * 73)
    mL = {l: float(np.mean(L[l])) for l in 'ABC'}
    mG = {l: float(np.mean(G[l])) for l in 'ABC'}
    print(f"{'moyenne':>12}{'':>7}" + ''.join(f'{mL[l]:>8.0f}%' for l in 'ABC')
          + ''.join(f'{mG[l]:>8.0f}%' for l in 'ABC'))
    print()

    eL = mL['B'] - mL['A']
    print(f'  FEATURES LISIBLES — trois projets, compares a trois personnes : {eL:+.0f} points.')
    if eL >= 3:
        print('  Melanger des depots gonfle le score : ces features reconnaissent aussi le projet.')
    elif eL <= -3:
        print('  Trois projets ne sont PAS plus faciles a separer que trois personnes.')
        print('  Ces features-la ne reconnaissent pas un projet.')
    else:
        print('  Pas de difference mesurable.')
    print()
    eB, eC = mG['B'] - mG['A'], mG['C'] - mG['A']
    print(f'  4-GRAMMES — trois projets : {eB:+.0f} points.  Trois sous-paquets : {eC:+.0f} points.')
    if eB >= 5 and eC >= 5:
        print(f'  Le classifieur separe trois sous-paquets d un meme projet ({mG["C"]:.0f} %) mieux')
        print(f'  que trois personnes ({mG["A"]:.0f} %). Et trois projets, mieux encore ({mG["B"]:.0f} %).')
        print('  Un score eleve avec des n-grammes ne dit donc pas « qui ».')
        print('  Il dit au moins autant « quel code ».')
    elif eB >= 5:
        print('  Trois projets se separent mieux que trois personnes : le projet pese.')
    else:
        print('  Pas d effet « projet » mesurable avec les 4-grammes sur ces corpus.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
