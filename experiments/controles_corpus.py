#!/usr/bin/env python3
"""
controles_corpus.py — quand on « reconnait » un developpeur, que reconnait-on ?

Le corpus est controle par construction (experiments/construire_corpus.py) :
meme depot, meme epoque, meme type de code. Ce script verifie que c'est vrai,
puis pose la question qui reste : a type de code et epoque egaux, le score
mesure-t-il la PERSONNE, ou ce sur quoi elle travaillait a ce moment-la ?

La reponse tient en une comparaison. Si le classifieur separe un developpeur
de LUI-MEME — ses 1 500 premieres lignes contre ses 1 500 dernieres — alors il
n'apprend pas seulement une personne.

Usage :  python3 experiments/controles_corpus.py
"""
from __future__ import annotations

import collections
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # pour _commun
from _commun import blocs, charger_devs, paquet, precision


def pct(r):
    return '    —' if r[0] is None else f'{r[0]:4.0f} %'


def main() -> int:
    CODE, ORI = charger_devs()
    devs = list(CODE)

    print('CONTROLES DU CORPUS')
    print()
    print('1. LE CORPUS EST-IL CE QU IL PRETEND ETRE ?')
    print()
    print(f"   {'':6}{'lignes':>7}{'du':>12}{'au':>12}{'fichiers':>10}   trois premiers sous-paquets")
    for d in devs:
        dates = [x for x, _ in ORI[d]]
        pq = collections.Counter(paquet(c) for _, c in ORI[d])
        mix = ', '.join(f'{p} {100 * n / len(ORI[d]):.0f} %' for p, n in pq.most_common(3))
        print(f'   {d:6}{len(CODE[d]):>7}{min(dates):>12}{max(dates):>12}'
              f'{len({c for _, c in ORI[d]}):>10}   {mix}')
    hors = sum(1 for d in devs for _, c in ORI[d]
               if not c.startswith('django/') or '/tests/' in c or '/migrations/' in c)
    dehors = sum(1 for d in devs for x, _ in ORI[d] if not ('2015-03-01' <= x < '2021-06-01'))
    print()
    print(f'   lignes hors bibliotheque : {hors}     lignes hors fenetre 2015-03 / 2021-05 : {dehors}')
    print('   Un seul depot, un seul regime de mise en forme, du code de bibliotheque.')
    print('   Ce qui differe encore : les sous-paquets. Dev 3 vit dans l ORM.')

    print()
    print('2. DEUX PERSONNES DIFFERENTES   (blocs de 80 lignes, hasard 50 %)')
    print()
    print(f"   {'':22}{'10 features lisibles':>22}{'4-grammes':>12}")
    deux = {'lisibles': [], 'ngrammes': []}
    for a in range(3):
        for b in range(a + 1, 3):
            C = {devs[a]: CODE[devs[a]], devs[b]: CODE[devs[b]]}
            r = {f: precision(C, 80, f) for f in deux}
            for f in deux:
                deux[f].append(r[f][0])
            print(f"   {devs[a]} / {devs[b]:14}{pct(r['lisibles']):>22}{pct(r['ngrammes']):>12}")

    print()
    print('3. LA MEME PERSONNE, COUPEE EN DEUX DANS LE TEMPS   (memes blocs, hasard 50 %)')
    print('   ses 1 500 premieres lignes contre ses 1 500 dernieres')
    print()
    print(f"   {'':22}{'10 features lisibles':>22}{'4-grammes':>12}")
    meme = {'lisibles': [], 'ngrammes': []}
    for d in devs:
        h = len(CODE[d]) // 2
        C = {'avant': CODE[d][:h], 'apres': CODE[d][h:]}
        r = {f: precision(C, 80, f) for f in meme}
        for f in meme:
            meme[f].append(r[f][0])
        print(f"   {d + ' contre ' + d:22}{pct(r['lisibles']):>22}{pct(r['ngrammes']):>12}")

    ml, mn = float(np.mean(meme['lisibles'])), float(np.mean(meme['ngrammes']))
    dl, dn = float(np.mean(deux['lisibles'])), float(np.mean(deux['ngrammes']))
    print()
    print('   EN MOYENNE')
    print(f"   {'deux personnes':22}{dl:>20.0f} %{dn:>10.0f} %")
    print(f"   {'la meme, deux epoques':22}{ml:>20.0f} %{mn:>10.0f} %")
    print()
    print('   LECTURE.')
    if abs(ml - 50) <= 6:
        print(f'   Les features lisibles ne separent pas un developpeur de lui-meme ({ml:.0f} %,')
        print('   le hasard) : ce qu elles mesurent ne bouge pas avec le chantier du moment.')
    else:
        print(f'   Les features lisibles separent un developpeur de lui-meme a {ml:.0f} % :')
        print('   elles aussi bougent avec le temps.')
    if mn - 50 > 6:
        print(f'   Les 4-grammes, si : {mn:.0f} %. Ils apprennent donc AUSSI ce sur quoi il')
        print('   travaillait a ce moment-la — ses fichiers, ses identifiants, son chantier.')
        print(f'   Entre deux personnes ils montent a {dn:.0f} % : soit {dn - 50:.0f} points au-dessus du')
        print(f'   hasard, dont {mn - 50:.0f} s obtiennent deja sans changer de personne.')
    else:
        print(f'   Les 4-grammes non plus ({mn:.0f} %) : ici, ils mesurent bien la personne.')
    print()
    print('   Peu de blocs (une quinzaine par classe au test) : ces chiffres donnent un')
    print('   ordre de grandeur, pas une unite.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
