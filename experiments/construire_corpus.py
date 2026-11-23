#!/usr/bin/env python3
"""
construire_corpus.py — d'ou vient corpus/devs/, et comment le refaire.

POURQUOI CE SCRIPT EXISTE. Le premier corpus de ce talk venait de pallets/flask.
Trois vrais contributeurs, pres de 90 % d'attribution. Puis il a fallu regarder
de pres (experiments/pourquoi_pas_flask.py rejoue tout) :
  - l'un des trois avait 92 % de ses lignes APRES l'adoption de black par le
    projet (mai 2019), les deux autres aucune : le classifieur pouvait apprendre
    le formateur ;
  - un autre avait 90 % de ses lignes dans tests/ : le classifieur pouvait
    apprendre « code de test » ;
  - et le MEME developpeur, coupe en deux (sa bibliotheque / ses tests), etait
    separe a 100 %. Mieux que deux personnes differentes.
flask n'a que deux contributeurs avec assez de code de bibliotheque : impossible
d'y construire un corpus controle a trois. D'ou ce second corpus.

LA REGLE, fixee avant de regarder le moindre score.
  depot      django/django (BSD-3-Clause)
  fenetre    auteur ET commit dates du 2015-03-01 au 2021-05-31.
             Apres isort (janvier 2015), avant black (fevrier 2022), avant
             juin 2021 : un seul regime de mise en forme, et pas d'assistant.
  type       code de BIBLIOTHEQUE seulement : django/**.py, sans tests, sans
             migrations (generees), sans conf/locale (des donnees).
  commits    non-merge, 300 lignes .py ajoutees au plus (au-dela : reformatages,
             deplacements, vendoring — ce n'est plus quelqu'un qui ecrit).
  qui        les TROIS auteurs qui ont le plus de lignes dans ces conditions.
             Pas de choix a la main.
  quoi       pour chacun, ses 3 000 dernieres lignes ajoutees non vides, dans
             l'ordre des commits.

CE QUE LA REGLE NE CONTROLE PAS, et qu'il faut dire :
  - le sous-paquet. Chacun a ses habitudes (ORM, GIS, utils). C'est le piege 3 ;
    experiments/controles_corpus.py mesure ce que ca pese.
  - git enregistre un AUTEUR par commit. Une ligne « ajoutee » peut etre une
    ligne d'un autre, retouchee ; un patch peut avoir ete repris par celui qui
    l'a integre. Aucune commande git ne le dit.
  - l'anonymat est une politesse, pas une protection : quiconque clone le depot
    retrouve les noms avec ce script.

Usage :
    git clone https://github.com/django/django /tmp/django      # clone COMPLET
    python3 experiments/construire_corpus.py /tmp/django          # affiche, n'ecrit rien
    python3 experiments/construire_corpus.py /tmp/django --ecrire # reecrit corpus/devs/
"""
from __future__ import annotations

import collections
import os
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUT, FIN = '2015-03-01', '2021-06-01'        # FIN exclue
MAX_COMMIT = 300
N_LIGNES = 3000
N_DEVS = 3


PROVENANCE_TETE = f"""# corpus/devs/ — d'ou viennent ces trois fichiers

Ecrit par `experiments/construire_corpus.py`. Ne pas modifier a la main : relancer le script.

| | |
|---|---|
| depot | github.com/django/django (BSD-3-Clause) |
| fenetre | auteur et commit dates du {DEBUT} au 2021-05-31 : apres isort, avant black, avant juin 2021 |
| type de code | bibliotheque seule : `django/**.py`, sans tests, sans migrations, sans `conf/locale` |
| commits | non-merge, {MAX_COMMIT} lignes `.py` ajoutees au plus |
| qui | les {N_DEVS} auteurs qui ont le plus de lignes dans ces conditions — aucun choix a la main |
| quoi | pour chacun, ses {N_LIGNES} dernieres lignes ajoutees non vides, dans l'ordre des commits |

Les contributeurs sont anonymises par politesse. Ce n'est pas une protection :
quiconque clone le depot et lance le script retrouve les noms.

"""


def est_bibliotheque(chemin: str) -> bool:
    nom = chemin.split('/')[-1]
    return (chemin.startswith('django/')
            and '/migrations/' not in chemin
            and not chemin.startswith('django/conf/locale/')
            and '/tests/' not in chemin
            and not nom.startswith('test'))


def paquet(chemin: str) -> str:
    q = chemin.split('/')
    if len(q) > 3 and q[1] == 'contrib':
        return 'contrib/' + q[2]
    return q[1].replace('.py', '')


def lire(depot: str):
    """[(sha, auteur, date_auteur, [(chemin, ligne ajoutee)])], du plus ancien au plus recent."""
    p = subprocess.Popen(
        ['git', '-C', depot, '-c', 'diff.renames=true', 'log', '--no-merges', f'--since={DEBUT}', f'--before={FIN}',
         '--date=short', '--format=@@@%H|%an|%ad', '-p', '--no-color', '-U0', '--', '*.py'],
        stdout=subprocess.PIPE)
    commits, cur, chemin = [], None, None
    for brut in p.stdout:
        l = brut.decode('utf-8', 'replace').rstrip('\n')
        if l.startswith('@@@'):
            sha, auteur, date = l[3:].split('|', 2)
            cur = [sha, auteur, date, []]
            commits.append(cur)
        elif l.startswith('+++ '):
            chemin = l[6:]
        elif cur is not None and l.startswith('+') and not l.startswith('+++'):
            cur[3].append((chemin, l[1:]))
    if p.wait() != 0:
        sys.exit(f"git log a echoue sur {depot} — est-ce bien un clone de django/django ?")
    return commits[::-1]


def construire(depot: str):
    commits = lire(depot)
    par_auteur = collections.defaultdict(list)       # auteur -> [(date, sha, chemin, ligne)]
    exclus = collections.Counter()
    for sha, auteur, date, ajouts in commits:
        if not (DEBUT <= date < FIN):                # date d'AUTEUR dans la fenetre aussi
            continue
        utiles = [(c, x) for c, x in ajouts if x.strip() and est_bibliotheque(c)]
        if len(ajouts) > MAX_COMMIT:
            exclus[auteur] += len(utiles)
            continue
        par_auteur[auteur] += [(date, sha, c, x) for c, x in utiles]
    rang = sorted(par_auteur, key=lambda a: (-len(par_auteur[a]), a))
    return commits, par_auteur, exclus, rang


def en_tete() -> str:
    """Deux lignes, celles que tous les chargeurs du depot savent retirer."""
    return ("# Lignes ajoutees par un contributeur de github.com/django/django (BSD-3-Clause)\n"
            "# Extraites par experiments/construire_corpus.py — regle et provenance : corpus/devs/PROVENANCE.md\n")


def provenance(i, lignes, total, exclu) -> str:
    dates = [d for d, *_ in lignes]
    pq = collections.Counter(paquet(c) for _, _, c, _ in lignes)
    ans = collections.Counter(d[:4] for d in dates)
    return (
        f"## Dev {i}\n\n"
        f"- {len(lignes)} lignes : ses dernieres, sur {total} retenues par la regle\n"
        f"- du {min(dates)} au {max(dates)}, {len({s for _, s, _, _ in lignes})} commits\n"
        f"- par annee : " + ', '.join(f'{y} : {n}' for y, n in sorted(ans.items())) + "\n"
        f"- sous-paquets : " + ', '.join(f'{p} {100 * n / len(lignes):.0f} %' for p, n in pq.most_common(5)) + "\n"
        f"- {exclu} lignes ecartees chez lui (commits de plus de {MAX_COMMIT} lignes)\n\n")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 1:
        print(__doc__)
        return 2
    ecrire = '--ecrire' in sys.argv
    commits, par_auteur, exclus, rang = construire(args[0])
    print(f'{len(commits)} commits .py non-merge dans la fenetre, {len(par_auteur)} auteurs '
          f'avec du code de bibliotheque.')
    print()
    print(f"{'rang':>4} {'lignes':>7} {'commits':>8} {'ecartees':>9}   sous-paquets")
    print('-' * 78)
    for k, a in enumerate(rang[:6], 1):
        L = par_auteur[a]
        pq = collections.Counter(paquet(c) for _, _, c, _ in L)
        mix = ', '.join(f'{p} {100 * n / len(L):.0f} %' for p, n in pq.most_common(4))
        marque = '  <- retenu' if k <= N_DEVS else ''
        print(f'{k:>4} {len(L):>7} {len({s for _, s, _, _ in L}):>8} {exclus[a]:>9}   {mix}{marque}')
    print('-' * 78)
    print(f'Les {N_DEVS} premiers sont retenus. Aucun nom n est affiche ni ecrit.')
    print()
    prov = []
    for i, a in enumerate(rang[:N_DEVS], 1):
        L = par_auteur[a][-N_LIGNES:]
        ans = collections.Counter(d[:4] for d, *_ in L)
        print(f'  Dev {i} : {len(L)} lignes, {min(d for d, *_ in L)} -> {max(d for d, *_ in L)}   '
              + ' '.join(f'{y}:{n}' for y, n in sorted(ans.items())))
        prov.append(provenance(i, L, len(par_auteur[a]), exclus[a]))
        if ecrire:
            dest = os.path.join(RACINE, 'corpus', 'devs', f'dev_{i}.py')
            assert not any(x.startswith(('# Lignes ajoutees', '# Extraites')) for *_, x in L)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(en_tete())
                f.write('\n'.join(x for _, _, _, x in L) + '\n')
            # le jumeau : pour CHAQUE ligne du corpus, sa date et son fichier d'origine.
            # C'est lui qui permet les controles — couper par fichier, par sous-paquet,
            # par date — sans avoir besoin du clone.
            with open(dest[:-3] + '.origine.tsv', 'w', encoding='utf-8') as f:
                f.write('\n'.join(f'{d}\t{c}' for d, _, c, _ in L) + '\n')
    if ecrire:
        with open(os.path.join(RACINE, 'corpus', 'devs', 'PROVENANCE.md'), 'w', encoding='utf-8') as f:
            f.write(PROVENANCE_TETE + ''.join(prov))
    print()
    print('corpus/devs/ reecrit.' if ecrire else 'Rien n a ete ecrit (ajouter --ecrire).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
