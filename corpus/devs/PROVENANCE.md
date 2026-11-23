# corpus/devs/ — d'ou viennent ces trois fichiers

Ecrit par `experiments/construire_corpus.py`. Ne pas modifier a la main : relancer le script.

| | |
|---|---|
| depot | github.com/django/django (BSD-3-Clause) |
| fenetre | auteur et commit dates du 2015-03-01 au 2021-05-31 : apres isort, avant black, avant juin 2021 |
| type de code | bibliotheque seule : `django/**.py`, sans tests, sans migrations, sans `conf/locale` |
| commits | non-merge, 300 lignes `.py` ajoutees au plus |
| qui | les 3 auteurs qui ont le plus de lignes dans ces conditions — aucun choix a la main |
| quoi | pour chacun, ses 3000 dernieres lignes ajoutees non vides, dans l'ordre des commits |

Les contributeurs sont anonymises par politesse. Ce n'est pas une protection :
quiconque clone le depot et lance le script retrouve les noms.

## Dev 1

- 3000 lignes : ses dernieres, sur 4478 retenues par la regle
- du 2015-10-02 au 2021-04-23, 418 commits
- par annee : 2015 : 94, 2016 : 966, 2017 : 1082, 2018 : 518, 2019 : 131, 2020 : 135, 2021 : 74
- sous-paquets : db 28 %, utils 11 %, contrib/gis 11 %, contrib/admin 9 %, core 8 %
- 2075 lignes ecartees chez lui (commits de plus de 300 lignes)

## Dev 2

- 3000 lignes : ses dernieres, sur 4170 retenues par la regle
- du 2015-05-25 au 2021-05-14, 193 commits
- par annee : 2015 : 19, 2016 : 939, 2017 : 1018, 2018 : 547, 2019 : 101, 2020 : 317, 2021 : 59
- sous-paquets : utils 18 %, core 15 %, contrib/gis 14 %, db 10 %, contrib/auth 7 %
- 1078 lignes ecartees chez lui (commits de plus de 300 lignes)

## Dev 3

- 3000 lignes : ses dernieres, sur 3764 retenues par la regle
- du 2015-12-17 au 2021-05-11, 208 commits
- par annee : 2015 : 78, 2016 : 521, 2017 : 392, 2018 : 560, 2019 : 993, 2020 : 352, 2021 : 104
- sous-paquets : db 78 %, core 5 %, contrib/postgres 5 %, contrib/contenttypes 4 %, test 3 %
- 396 lignes ecartees chez lui (commits de plus de 300 lignes)

