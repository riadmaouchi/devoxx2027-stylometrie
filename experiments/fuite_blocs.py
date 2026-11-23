#!/usr/bin/env python3
"""
fuite_blocs.py — CONTRE-TEST DES 4-GRAMMES.  Protocole complet, resultat final.

CE QU'ON TESTE. Le notebook donne le score des 800 4-grammes de caracteres a
160 lignes (cellule « CE QUI FERAIT MIEUX »). Deux fuites peuvent le gonfler.
Elles sont testees separement, ici.

  FUITE 1 — LA PROXIMITE DES BLOCS.  Le corpus est decoupe en blocs CONTIGUS,
  puis ces blocs sont melanges au hasard entre apprentissage et test. Deux
  blocs voisins partagent imports, noms de fonctions, chantier en cours : ils
  ne sont pas independants. Contre-protocole : split CONTIGU — les 60 % premiers
  blocs en apprentissage, les 40 % derniers en test. Des mois de commits
  separent alors le train du test.

  FUITE 2 — LE VOCABULAIRE.  Les 800 4-grammes les plus frequents sont choisis
  sur TOUT le corpus, test compris. Contre-protocole : les choisir sur le
  TRAIN SEUL.

  ET UN TROISIEME DECOUPAGE, pour savoir CE QUI fuit : apprentissage et test
  sur des FICHIERS differents (aucun fichier des deux cotes), a dates melees.

PROTOCOLE EXACT, identique dans toutes les conditions.
  1. Corpus : corpus/devs/dev_{1,2,3}.py — 3 contributeurs de django/django,
     construits par experiments/construire_corpus.py. Chargeur identique a
     celui du notebook : on ne retire que les deux lignes d'en-tete.
  2. Blocs de N lignes consecutives, N dans {40, 60, 80, 120, 160}, tronques au
     plus petit nombre de blocs commun aux 3 devs.
  3. Split 60 / 40.  « alea » = permutation des blocs (protocole du notebook).
     « contigu » = les premiers 60 % en train, les derniers 40 % en test.
  4. Features : 800 4-grammes de caracteres, frequence relative.
  5. Normalisation : z-score (mu, sigma du POOL D'APPRENTISSAGE seulement).
  6. Classement : centroide par dev sur le train, distance de Manhattan
     moyenne, plus proche centroide. Hasard = 33 %.
  7. Repetitions : bras « alea » = moyenne sur 7 graines ; bras « contigu » =
     passe unique deterministe (il n'y a rien a tirer au sort).

Usage :  python3 experiments/fuite_blocs.py            # tout, une douzaine de secondes
         python3 experiments/fuite_blocs.py --court    # sans le dernier decoupage, 2 s
"""
from __future__ import annotations

import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _commun

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEVS = [f'Dev {i}' for i in (1, 2, 3)]
TAILLES = (40, 60, 80, 120, 160)
GRAINES = (7, 11, 23, 42, 101, 2024, 31337)
N_GRAMMES = 800
EN_TETE = ('# Lignes ajoutees', '# Extraites')


def charger() -> dict[str, list[str]]:
    """Le chargeur du notebook, a l'identique."""
    out = {}
    for d in DEVS:
        p = os.path.join(RACINE, 'corpus', 'devs', f'dev_{d[-1]}.py')
        out[d] = [l for l in open(p, encoding='utf-8').read().split('\n')
                  if not l.startswith(EN_TETE)]
    return out


def blocs(L, n):
    return ['\n'.join(L[i:i + n]) for i in range(0, len(L) - n + 1, n)]


def mesurer(CODE, taille):
    """Renvoie (nb_blocs, nb_train, {(split, vocabulaire): precision en %})."""
    B = {d: blocs(CODE[d], taille) for d in DEVS}
    k = min(len(B[d]) for d in DEVS)              # etape 2 : blocs egalises
    B = {d: B[d][:k] for d in DEVS}
    ntr = max(2, int(k * 0.6))                    # etape 3 : split 60 / 40
    CNT = {d: [Counter(s[i:i + 4] for i in range(len(s) - 3)) for s in B[d]] for d in DEVS}
    LEN = {d: [max(len(s) - 3, 1) for s in B[d]] for d in DEVS}

    def essai(split, vocabulaire, graine):
        rng = np.random.default_rng(graine)
        idx = {d: (rng.permutation(k) if split == 'alea' else np.arange(k)) for d in DEVS}
        tr = {d: idx[d][:ntr] for d in DEVS}
        te = {d: idx[d][ntr:] for d in DEVS}
        g = Counter()                             # etape 4 : les 800 4-grammes
        for d in DEVS:
            for i in (tr[d] if vocabulaire == 'train' else range(k)):
                g.update(CNT[d][i])
        V = [x for x, _ in g.most_common(N_GRAMMES)]
        vec = lambda d, i: np.array([CNT[d][i].get(x, 0) / LEN[d][i] for x in V])
        X = {d: np.array([vec(d, i) for i in tr[d]]) for d in DEVS}
        Y = {d: np.array([vec(d, i) for i in te[d]]) for d in DEVS}
        pool = np.vstack([X[d] for d in DEVS])    # etape 5 : z-score sur le train
        mu, sd = pool.mean(0), pool.std(0)
        sd[sd == 0] = 1
        cen = {d: ((X[d] - mu) / sd).mean(0) for d in DEVS}
        ok = t = 0                                # etape 6 : plus proche centroide
        for d in DEVS:
            for v in (Y[d] - mu) / sd:
                dd = {e: np.abs(v - cen[e]).mean() for e in DEVS}
                ok += min(dd, key=dd.get) == d
                t += 1
        return ok / t

    r = {}
    for vocabulaire in ('tout', 'train'):         # etape 7 : repetitions
        r[('alea', vocabulaire)] = float(
            np.mean([essai('alea', vocabulaire, g) for g in GRAINES])) * 100
        r[('contigu', vocabulaire)] = essai('contigu', vocabulaire, 7) * 100
    return k, ntr, r


def main() -> int:
    CODE = charger()
    print('CONTRE-TEST DES 4-GRAMMES — LE SCORE TIENT-IL A UNE FUITE ?')
    print()
    print('  colonne 1 : alea + vocabulaire sur tout  =  LE PROTOCOLE DU NOTEBOOK')
    print('  colonne 2 : split contigu  — des mois de commits entre train et test')
    print('  colonne 3 : vocabulaire choisi sur le train seul')
    print('  colonne 4 : les deux corrections a la fois')
    print()
    print(f"{'bloc':>5}{'blocs':>6}{'train':>6}  {'NOTEBOOK':>9}{'contigu':>9}"
          f"{'voc.train':>11}{'les deux':>10}")
    print('-' * 62)
    prox, voc, R = [], [], {}
    for T in TAILLES:
        k, ntr, r = mesurer(CODE, T)
        R[T] = r
        prox.append(r[('contigu', 'tout')] - r[('alea', 'tout')])
        voc.append(r[('alea', 'tout')] - r[('alea', 'train')])
        print(f'{T:>5}{k:>6}{ntr:>6}  {r[("alea","tout")]:>8.0f}%'
              f'{r[("contigu","tout")]:>8.0f}%{r[("alea","train")]:>10.0f}%'
              f'{r[("contigu","train")]:>9.0f}%')
    print('-' * 62)
    print('hasard : 33 %   ·   800 4-grammes de caracteres   ·   3 devs, 1 depot')
    print()
    r160 = R[160]
    a, c, v, les2 = (r160[('alea', 'tout')], r160[('contigu', 'tout')],
                     r160[('alea', 'train')], r160[('contigu', 'train')])
    mp, mv = float(np.mean(prox)), float(np.mean(voc))

    print(f'  FUITE 1, proximite des blocs  (col.2 - col.1) : {mp:+.1f} points en')
    print(f'  moyenne, de {min(prox):+.1f} a {max(prox):+.1f}.')
    if mp <= -5 and max(prox) < 0:
        print('  Separer le train du test dans le temps FAIT tomber le score, a toutes')
        print(f'  les tailles de bloc : {a:.0f} % -> {c:.0f} % a 160 lignes. Les blocs voisins se')
        print('  ressemblent — memes fichiers, meme chantier — et le classifieur en')
        print('  profite. L objection TIENT.')
    elif mp >= -2:
        print('  Separer le train du test dans le temps ne fait PAS tomber le score.')
        print('  L objection est legitime, elle est testee, elle ne tient pas ici.')
    else:
        print('  Separer le train du test dans le temps fait baisser le score, mais')
        print('  pas a toutes les tailles de bloc : effet faible, a ne pas surinterpreter.')
    print()
    print(f'  FUITE 2, vocabulaire  (col.1 - col.3) : {mv:+.1f} point en moyenne,')
    print(f'  de {min(voc):+.1f} a {max(voc):+.1f}. ' + (
        'Reelle, et petite.' if 0.5 <= mv < 5 else
        'Negligeable ici.' if mv < 0.5 else 'Reelle, et pas petite.'))
    print()
    print(f'  LES DEUX CORRIGEES, a 160 lignes : {les2:.0f} %, contre {a:.0f} % annonces.')
    print('  Hasard : 33 %.')

    if '--court' in sys.argv:          # le notebook, en direct : on s'arrete ici
        return 0

    # ── qu'est-ce qui fuit : le fichier, ou la periode ? ─────────────────────
    code, origine = _commun.charger_devs()
    print()
    print('  CE QUI FUIT : LE FICHIER, OU LA PERIODE ?')
    lignes = []
    for T in (80, 160):
        al = _commun.precision(code, T, 'ngrammes')[0]
        fi = _commun.precision(code, T, 'ngrammes', split='fichier', origine=origine)[0]
        co = _commun.precision(code, T, 'ngrammes', split='contigu')[0]
        lignes.append((T, al, fi, co))
        print(f'    blocs de {T:>3} :  au hasard {al:.0f} %   fichiers disjoints {fi:.0f} %'
              f'   periodes disjointes {co:.0f} %')
    if all(fi >= al - 3 for _, al, fi, _ in lignes) and all(co <= al - 5 for _, al, _, co in lignes):
        print('  Tester sur des fichiers jamais vus ne coute rien. Tester sur une periode')
        print('  jamais vue coute cher. Le classifieur ne retient pas des fichiers : il')
        print('  retient ce sur quoi le developpeur travaillait A CE MOMENT-LA.')
    print()
    print('  Meme question, posee autrement : experiments/controles_corpus.py separe')
    print('  un developpeur de LUI-MEME, premiere moitie contre seconde.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
