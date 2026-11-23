#!/usr/bin/env python3
"""
pourquoi_pas_flask.py — le premier corpus de ce talk, et pourquoi il a ete jete.

Le premier corpus : les trois contributeurs de pallets/flask qui ont le plus de
lignes, commits de plus de 300 lignes exclus, rien apres juin 2021. Il donnait
un tres beau score d'attribution avec des n-grammes. Ce script montre ce que
ce score mesurait.

Il refait le corpus depuis un clone, sans aucun nom, et repond a quatre questions :
  1. le commit « Reformat with black » : qui est ce « developpeur » ?
  2. les trois contributeurs ecrivent-ils a la meme EPOQUE ?
  3. ecrivent-ils le meme TYPE de code ?
  4. le classifieur separe-t-il un developpeur de LUI-MEME ?

Usage :
    git clone https://github.com/pallets/flask /tmp/flask        # clone COMPLET
    python3 experiments/pourquoi_pas_flask.py /tmp/flask
"""
from __future__ import annotations

import collections
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _commun import precision

FIN = '2021-06-01'
MAX_COMMIT = 300
N_LIGNES = 3000


def lire(depot):
    p = subprocess.Popen(
        ['git', '-C', depot, '-c', 'diff.renames=true', 'log', '--no-merges', f'--before={FIN}', '--date=short',
         '--format=@@@%H|%an|%ad|%s', '-p', '--no-color', '-U0', '--', '*.py'],
        stdout=subprocess.PIPE)
    commits, cur, chemin = [], None, None
    for brut in p.stdout:
        l = brut.decode('utf-8', 'replace').rstrip('\n')
        if l.startswith('@@@'):
            sha, auteur, date, sujet = l[3:].split('|', 3)
            cur = [sha, auteur, date, sujet, []]
            commits.append(cur)
        elif l.startswith('+++ '):
            chemin = l[6:]
        elif cur is not None and l.startswith('+') and not l.startswith('+++'):
            cur[4].append((chemin, l[1:]))
    if p.wait() != 0:
        sys.exit(f'git log a echoue sur {depot}')
    return commits[::-1]


def est_test(c):
    return c.startswith('tests/') or '/test' in c or 'testsuite' in c


def est_bibliotheque(c):
    return (c.startswith('src/flask/') or c.startswith('flask/')) and not est_test(c)


def pct(r):
    return '    —' if r[0] is None else f'{r[0]:4.0f} %'


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    commits = lire(sys.argv[1])

    # ── 1. le commit black ──────────────────────────────────────────────────
    black = next((c for c in commits if c[3].strip() == 'Reformat with black'), None)
    if black is None:
        sys.exit('Commit « Reformat with black » introuvable : est-ce bien pallets/flask ?')
    DATE_BLACK, auteur_black = black[2], black[1]
    brut = collections.Counter()
    for _, a, _, _, add in commits:
        brut[a] += len(add)
    rang_brut = [a for a, _ in brut.most_common()]
    en_2019 = collections.Counter()
    for _, a, d, _, add in commits:
        if d[:4] == DATE_BLACK[:4]:
            en_2019[a] += len(add)
    print('1. LE COMMIT « Reformat with black »')
    print(f'   date : {DATE_BLACK}     lignes .py ajoutees : {len(black[4])}')
    print(f'   son auteur a {brut[auteur_black]} lignes .py dans tout le depot : '
          f'{100 * len(black[4]) / brut[auteur_black]:.1f} % viennent de ce commit.')
    print(f'   Il est {rang_brut.index(auteur_black) + 1}e contributeur sur {len(rang_brut)} par le volume, '
          f'et {[a for a, _ in en_2019.most_common()].index(auteur_black) + 1}er de l annee {DATE_BLACK[:4]}.')
    print('   Ce « developpeur », c est un formateur.')

    # ── le corpus : les 3 premiers, commits <= 300 lignes ───────────────────
    par = collections.defaultdict(list)
    for sha, a, d, _, add in commits:
        if len(add) > MAX_COMMIT:
            continue
        par[a] += [(d, c, x) for c, x in add if x.strip()]
    devs = sorted(par, key=lambda a: (-len(par[a]), a))[:3]
    corpus = {f'Dev {i}': par[a][-N_LIGNES:] for i, a in enumerate(devs, 1)}

    brut3 = {d: [x for _, _, x in L] for d, L in corpus.items()}
    s3 = (precision(brut3, 160, 'lisibles'), precision(brut3, 160, 'ngrammes', vocab='tout'))
    print()
    print('   CE QUE CE CORPUS DONNAIT — trois contributeurs, blocs de 160 lignes, hasard 33 % :')
    print(f'   10 features lisibles {pct(s3[0]).strip()}   ·   800 4-grammes {pct(s3[1]).strip()}')
    print('   Un tres beau score. Voici ce qu il mesurait.')
    print()
    print('2 et 3. LES TROIS CONTRIBUTEURS RETENUS — commit black exclu, comme tous')
    print(f'   les commits de plus de {MAX_COMMIT} lignes. Leurs {N_LIGNES} dernieres lignes.')
    print()
    print(f"   {'':6}{'lignes':>7}{'du':>12}{'au':>12}{'apres black':>13}{'dans tests/':>13}")
    for d, L in corpus.items():
        dates = [x for x, _, _ in L]
        ap = 100 * sum(x >= DATE_BLACK for x in dates) / len(L)
        te = 100 * sum(est_test(c) for _, c, _ in L) / len(L)
        print(f'   {d:6}{len(L):>7}{min(dates):>12}{max(dates):>12}{ap:>11.0f} %{te:>11.0f} %')
    print()
    print('   Apres mai 2019, le projet passe chaque commit dans black. Un contributeur')
    print('   dont toutes les lignes datent d apres porte le style du formateur.')
    print('   Et un contributeur qui ecrit surtout des tests se reconnait a « assert ».')

    # ── 4. la meme personne, deux etiquettes ────────────────────────────────
    print()
    print('4. LA MEME PERSONNE, DEUX ETIQUETTES   (blocs de 160 lignes, hasard 50 %)')
    print()
    print(f"   {'':46}{'lisibles':>10}{'4-grammes':>11}")
    a1, a2 = devs[0], devs[1]
    lib = [x for d, c, x in par[a1] if d < DATE_BLACK and est_bibliotheque(c)][-N_LIGNES:]
    tst = [x for d, c, x in par[a1] if d < DATE_BLACK and est_test(c)][-N_LIGNES:]
    C = {'bibliotheque': lib, 'tests': tst}
    r1 = (precision(C, 160, 'lisibles'), precision(C, 160, 'ngrammes'))
    print(f"   {'Dev 1 : sa bibliotheque / ses tests':46}{pct(r1[0]):>10}{pct(r1[1]):>11}")
    av = [x for d, c, x in par[a2] if d < DATE_BLACK][-N_LIGNES:]
    ap = [x for d, c, x in par[a2] if d >= DATE_BLACK][-N_LIGNES:]
    C = {'avant': av, 'apres': ap}
    r2 = (precision(C, 160, 'lisibles'), precision(C, 160, 'ngrammes'))
    print(f"   {'Dev 2 : avant black / apres black':46}{pct(r2[0]):>10}{pct(r2[1]):>11}")
    g = lambda L: (lambda s: 100 * s.count('"') / max(s.count('"') + s.count("'"), 1))('\n'.join(L))
    print()
    print(f'   Dev 2, part de guillemets doubles : {g(av):.0f} % avant black, {g(ap):.0f} % apres.')
    print()
    if r1[1][0] is not None and r1[1][0] >= 90:
        print(f'   Le classifieur separe un developpeur de lui-meme a {r1[1][0]:.0f} %.')
        print('   Ce corpus ne mesurait pas trois personnes. Il mesurait une epoque,')
        print('   un formateur et un type de code — sous trois etiquettes.')
    print()
    print('   D ou le second corpus : experiments/construire_corpus.py.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
