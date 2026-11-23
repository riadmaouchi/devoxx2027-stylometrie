# Qui a écrit ce code : vous, l'IA… ou les deux ?

Notebook, corpus et scripts de mesure du talk **Devoxx France 2027**
*Ce que vos commits disent de vous — et de l'IA qui vous assiste.*

> **Le style est une empreinte mesurable. Mais mesurer une différence ne dit pas
> ce qui l'a causée.**

---

## Ce que contient ce dépôt

Tout ce qui est montré à l'écran pendant le talk, et de quoi le refaire chez vous.

```
devoxx2027-livecoding.ipynb   le notebook du talk, dans l'ordre de la scène
live/                         les mêmes démos en live coding, pour VS Code
corpus/                       tous les corpus, aucun téléchargement requis
experiments/                  les mesures qui ne tiennent pas dans le notebook
```

**Deux façons de jouer les démos, mêmes chiffres.** Le notebook, cellule par
cellule. Ou `live/`, dans VS Code : chaque démo part d'un fichier qui ne
contient que des titres, et le code s'écrit devant la salle à coups de
snippets (`.vscode/live.code-snippets`). Mode d'emploi : `live/LISEZ-MOI.md`.

**Aucune dépendance maison.** Le notebook n'importe que `numpy`, `matplotlib`
et la bibliothèque standard, plus deux modules de `experiments/`. Chaque mesure tient en quelques lignes que vous
pouvez relire. Pas de réseau, pas de GPU, pas de `pip install` d'une librairie
qu'il faudrait croire sur parole.

```bash
pip install -r requirements.txt
jupyter notebook devoxx2027-livecoding.ipynb      # depuis CE dossier : il lit corpus/ et experiments/
```

---

## Le corpus

| dossier | contenu | provenance |
|---|---|---|
| `corpus/*.txt` | Zola, Maupassant, Flaubert (~36 000 mots chacun), Verne (31 000) — préambules d'éditeur retirés | Projet Gutenberg, `experiments/nettoyer_romans.py` |
| `corpus/devs/` | 3 contributeurs de `django/django`, anonymisés — corpus **contrôlé** | `experiments/construire_corpus.py`, voir `corpus/devs/PROVENANCE.md` |
| `corpus/neuf/` | code humain **neuf** : uniquement des lignes de création de fichier | `pallets/flask`, `git log --diff-filter=A` |
| `corpus/eras/` | le même développeur avant / après juin 2021 | `pallets/flask` |
| `corpus/projets/` | requests, PyYAML, trois sous-paquets de werkzeug — pour le piège 3 | fichiers figés, licences en tête |
| `corpus/ia/` | 348 lignes non vides générées par un LLM (ChatGPT), un seul prompt, aucune consigne de style | voir `corpus/ia/LISEZ-MOI.md` |

### Le premier corpus a été jeté : c'est le piège du label

`git log --author` donne le **committeur**, pas l'auteur du code. Le premier
corpus venait de `pallets/flask`. Un « développeur » y avait 3 788 de ses 3 796
lignes dans un seul commit : *« Reformat with black »*. Quatrième contributeur du
dépôt par le volume ; techniquement, un script.

L'écarter ne suffisait pas. `experiments/pourquoi_pas_flask.py` refait ce corpus
depuis un clone et montre ce que son score mesurait :

| | Dev 1 | Dev 2 | Dev 3 |
|---|---|---|---|
| lignes écrites **après** l'adoption de black par le projet | 0 % | 92 % | 0 % |
| lignes dans `tests/` | 31 % | 24 % | 90 % |

Et le même développeur, sa bibliothèque contre ses tests, était séparé de
**lui-même** à 100 %. Ce corpus affichait près de 90 % d'attribution : il mesurait
une époque, un formateur et un type de code.

D'où le second corpus, `corpus/devs/`, construit par une règle fixée avant de
regarder un score (`experiments/construire_corpus.py`) :

- un seul dépôt, `django/django` ;
- une seule époque : mars 2015 → mai 2021, après isort, avant black, avant juin 2021 ;
- un seul type de code : la bibliothèque, sans tests ni migrations ;
- commits de 300 lignes au plus ;
- les trois auteurs qui ont le plus de lignes dans ces conditions — aucun choix à la main ;
- pour chacun, ses 3 000 dernières lignes, avec la date et le fichier d'origine de
  chaque ligne (`dev_N.origine.tsv`).

---

## Les mesures, et où elles sont produites

Tous les chiffres montrés en direct viennent du **notebook**.

| mesure | résultat | où |
|---|---|---|
| courbe précision / volume (Burrows's Delta, 3 développeurs) | 50 % à 5 lignes → 82 % à 157, hasard 33 % | notebook, Acte 1 |
| part des mots-fonction dans un texte | 65 mots-fonction = 45 % des mots des 4 romans (44 à 47 %) | `experiments/part_mots_fonction.py` |
| les 4 tests de Juola, transposés au code | 7 extraits sur 12, hasard 4 ; 3/3 près des références, 4/9 plus tard | notebook, Live 1 |
| le classifieur qui apprend le sujet | 72 % (mots de contenu) vs 61 % (mots-fonction), 4 romans | notebook, Live 2 |
| attribution sur 3 vrais développeurs | 58 % (features lisibles) vs 84 % (4-grammes), hasard 33 % | notebook, Acte 2 |
| le même score, testé sur une période jamais vue | 84 % → 67 %, puis 62 % | notebook + `experiments/fuite_blocs.py` |
| une méthode explicable, choisie à l'aveugle, même test | 100 tokens + Delta : 71 % [IC 50–86] à 160 lignes, 69 % [54–80] à 80 ; 4-grammes : 62 % / 56 % | `experiments/ameliorer.py` (protocole commité avant exécution) |
| personnes, projets, sous-paquets (4-grammes) | 75 % / 90 % / 83 % | notebook + `experiments/piege_projet.py` |
| la machine est-elle reconnaissable ? | 69 % / 74 % / 72 %, hasard 25 % | notebook + `experiments/mesurer_signature.py` |
| la même mesure, test durci (blocs voisins séparés) | 52 % / 62 % / 66 % ; 80 à 100 % des blocs IA reconnus | notebook + `experiments/contre_tests.py` |
| à quoi elle se reconnaît (7 mesures) | 3 séparent, 2 dans le bruit, 2 contredisent | notebook + `experiments/mesurer_controles.py` |
| un second modèle (Claude, 733 lignes) | reconnu à 68 / 69 / 77 % ; un seul des 3 traits tient (les ternaires) | notebook + `experiments/deux_fichiers_ia.py` |
| avant / après juin 2021 | type hints +2 118 % (×22), docstrings −77 %, commentaires −38 % | notebook, Acte 3 |

### Le contre-test des 4-grammes

Le 84 % est le résultat d'un protocole, et un protocole peut fuir. Deux fuites
possibles, testées séparément — `experiments/fuite_blocs.py` :

| | protocole du notebook | split contigu | vocabulaire sur le train | les deux |
|---|---|---|---|---|
| 40 lignes  | 73 % | 60 % | 73 % | 54 % |
| 60 lignes  | 72 % | 63 % | 69 % | 50 % |
| 80 lignes  | 76 % | 62 % | 76 % | 51 % |
| 120 lignes | 78 % | 67 % | 75 % | 63 % |
| 160 lignes | 84 % | 67 % | 83 % | 62 % |

- **Fuite 1 — la proximité des blocs.** Les blocs sont contigus puis mélangés au
  hasard entre apprentissage et test. Contre-protocole : split **contigu**, les
  60 % premiers blocs en apprentissage, les 40 % derniers en test — des mois de
  commits entre les deux. Écart : **−12,8 points** en moyenne (de −17,3 à −8,3), à
  toutes les tailles de bloc. **L'objection tient.**
- **Fuite 2 — le vocabulaire.** Les 800 4-grammes sont choisis sur tout le corpus,
  test compris. Choisis sur le train seul : **−1,4 point** en moyenne. Réelle, et petite.
- **Ce qui fuit.** Tester sur des *fichiers* jamais vus ne coûte rien (87 % à 80
  lignes) ; tester sur une *période* jamais vue coûte cher (51 %). Le classifieur ne
  retient pas des fichiers : il retient ce sur quoi le développeur travaillait à ce
  moment-là.

Sur le premier corpus, ce contre-test ne montrait rien : l'époque et le type de
code séparaient déjà tout le monde, partout. Il a fallu contrôler le corpus pour
que la fuite devienne visible.

### La même personne, deux étiquettes

`experiments/controles_corpus.py` coupe chaque développeur en deux dans le temps —
ses 1 500 premières lignes contre ses 1 500 dernières — et demande au classifieur
de les séparer (hasard 50 %) :

| | 10 features lisibles | 4-grammes |
|---|---|---|
| deux personnes différentes | 71 % | 84 % |
| la même personne, deux époques | 51 % | 68 % |

Les features lisibles ne séparent pas un développeur de lui-même : ce qu'elles
mesurent ne bouge pas avec le chantier du moment. Les 4-grammes, si.

### Ce qui demande un clone

Deux mesures ont besoin d'un vrai dépôt Git et vivent donc dans `experiments/`.
Ce sont celles que le talk vous demande de lancer sur **votre** dépôt en partant :

```bash
git clone https://github.com/psf/requests /tmp/requests   # clone COMPLET, voir ci-dessous
python3 experiments/real_repo_check.py /tmp/requests
python3 experiments/false_positives.py /tmp/requests
```

- `real_repo_check.py` → médiane de **9 auteurs par fichier**, record à **122** ;
  dans le fichier médian, l'auteur principal ne détient que **49 %** des lignes,
  et seulement **3 fichiers sur 25** ont un auteur dominant à plus de 80 %.
- `false_positives.py` → **4 %** de faux positifs (1 fichier sur 23) sur requests
  tel qu'il était au 31 mai 2021, un mois avant la préversion de Copilot. Le script
  ne lit pas le dossier : il lit le dépôt au dernier commit avant une date
  (`--avant`, 2021-06-01 par défaut). Le fichier classé « IA » est
  `exceptions.py` : aucune annotation de type, mais des docstrings partout et des
  noms comme `ConnectionError`, que le score compte comme du camelCase.

Deux autres scripts refont les corpus de développeurs, et il leur faut le dépôt d'origine :

```bash
git clone https://github.com/django/django /tmp/django
python3 experiments/construire_corpus.py /tmp/django            # affiche la sélection, n'écrit rien
python3 experiments/construire_corpus.py /tmp/django --ecrire   # réécrit corpus/devs/ à l'identique

git clone https://github.com/pallets/flask /tmp/flask
python3 experiments/pourquoi_pas_flask.py /tmp/flask            # le premier corpus, et ce qu'il mesurait
```

Tout le reste tourne hors-ligne, sur les fichiers de `corpus/` :

```bash
python3 experiments/controles_corpus.py    # la même personne, deux étiquettes
python3 experiments/fuite_blocs.py         # le contre-test des 4-grammes
python3 experiments/piege_projet.py        # personnes, projets, sous-paquets
python3 experiments/contre_tests.py        # le contre-test du 84 %, applique a la courbe, au 58 % et au test IA
python3 experiments/part_mots_fonction.py  # la part des mots-fonction dans les 4 romans (45 %)
python3 experiments/deux_fichiers_ia.py    # un second modele : l'objection du fichier unique
python3 experiments/ameliorer.py           # faire mieux sans tricher : choix a l'aveugle, test une fois
```

> **La règle de décision du talk :** plusieurs auteurs par fichier, et toute
> métrique « par développeur » tirée de `git` mélange leurs mains — tableaux de
> contribution, attribution de reviewers « par propriétaire », `CODEOWNERS`.
> Vérifiez avant de vous en servir. (Aucun seuil n'est mesuré ici.)

> ⚠️ **Clonez en entier.** Un `git clone --depth N` tronque l'historique et fait
> chuter le nombre d'auteurs par fichier : avec `--depth 200`, la médiane tombe
> de 9 à 3. Les chiffres ci-dessus supposent l'historique complet.

---

## Les quatre pièges, démontrés en direct

1. **Le sujet déguisé** — un classifieur à 72 % qui a appris « fogg » et
   « passepartout ». Et, sur l'IA, une « signature » qui n'est que le vocabulaire de
   ce qu'on lui a demandé d'écrire : le même calcul entre deux humains du même dépôt
   les sépare davantage encore, sur `models` et `gettext`.
2. **Le label** — `git log` donne le committeur, pas l'auteur. Et un contributeur peut
   n'être, à l'arrivée, qu'un formateur, une époque ou un dossier `tests/`. Le corpus
   littéraire avait le même défaut : 11 % du « Verne » était une licence en anglais.
3. **Le projet** — avec les n-grammes, trois sous-paquets d'un même projet se
   séparent à 83 %, trois projets à 90 %, trois personnes à 75 %. Le classifieur
   reconnaît mieux un sous-paquet qu'une personne — `experiments/piege_projet.py`.
   Les features lisibles, elles, ne reconnaissent pas un projet (37 % contre 51 %).
4. **La cause** — le style d'un même humain a bougé après juin 2021. Copilot ?
   Peut-être. Mais aussi Python 3.9, mypy et les conventions du projet. Le
   déplacement est réel ; sa cause n'est pas démontrable.

---

## Ce que ce dépôt ne prouve pas

Le corpus IA fait 348 lignes non vides, d'un seul fichier ; la mesure en lit 8 blocs
de 40 lignes par candidat, **un seul modèle, un seul prompt, une seule conversation, un seul
domaine, un seul langage**. Et ce domaine — un microframework HTTP — n'est pas
celui des trois développeurs, qui écrivent un ORM et des utilitaires.

Les trois développeurs diffèrent encore par leurs sous-paquets, et chaque mesure
repose sur une quinzaine de blocs par classe : des ordres de grandeur, pas des unités.

> « Cette IA-là est reconnaissable sur ce corpus » — pas « l'IA est reconnaissable ».

Si quelqu'un vous vend un détecteur d'IA universel, les trois questions à poser
sont : combien de modèles, combien de prompts, combien de blocs.

---

## Sources

- Juola (2013), *Rowling and "Galbraith": an authorial analysis*, Language Log,
  16 juillet 2013 — blocs de 1 000 lignes, « #1 or #2 », « suggestive »
- *Oxford don aids Rowling pseudonym revelations*, The Oxford Student, 19 juillet 2013
  — l'analyse de Peter Millican
- Juola (2015), *The Rowling Case: A Proposed Standard Analytic Protocol for
  Authorship Questions*, Digital Scholarship in the Humanities 30, suppl. 1
- Kestemont et al. (2020), *Overview of the Cross-Domain Authorship Verification
  Task at PAN 2020*, CEUR-WS vol. 2696 — section 3 (41 000 auteurs), section 8
  (le sujet, « one of the main causes driving misclassifications »), Table 1
- Caliskan-Islam et al. (2015), *De-anonymizing Programmers via Code Stylometry*,
  USENIX Security — 94 % sur 1 600 auteurs, sur Google Code Jam
- Cammarota, Bozza, Roten & Taroni (2024), *Forensic Science International:
  Synergy* 9, 100481
- van Halteren, Baayen, Tweedie, Haverkort & Neijt (2005), *Journal of
  Quantitative Linguistics* 12(1) — la notion de « stylome »
- Brennan & Greenstadt (2009), IAAI — attaques adversariales

---

## Dépôts compagnons

Les mesures qui ne tiennent pas dans un live de quatre minutes vivent à côté :

| dépôt | ce qu'il contient |
|---|---|
| [dev-fingerprint](https://github.com/riadmaouchi/dev-fingerprint) | 6 670 commits, 11 développeurs, 2018–2025. Détection de points de rupture sur les signaux de process. C'est d'ici que vient le résultat Willison / Abramov. |
| [copilot-signal](https://github.com/riadmaouchi/copilot-signal) | Étude cas-témoin : 147 paires appariées, 13 auteurs, 11 dépôts, Wilcoxon apparié. |
| [llm-style-fingerprints](https://github.com/riadmaouchi/llm-style-fingerprints) | 80 extraits de Zola et Maupassant réécrits par 4 modèles, vecteurs de 57 mots-fonction. |
| [stylometry-python](https://github.com/riadmaouchi/stylometry-python) | La librairie : `StyleAnalyzer`, `CodeAnalyzer`. `pip install stylometry-python`. |

**Le notebook de ce dépôt n'importe aucun des quatre.** Il tourne en numpy et
stdlib pour que chaque mesure reste relisible pendant le talk. La librairie sert
à rebrancher les mêmes features sur votre propre code.

---

## Licence

MIT pour le notebook et les scripts (`LICENSE`).

Les corpus gardent la licence du projet dont ils viennent — `django/django`,
`pallets/flask` et `pallets/werkzeug` (BSD-3-Clause), `psf/requests` (Apache-2.0),
`yaml/pyyaml` (MIT). Les textes de ces licences sont dans `corpus/LICENCES/`, avec
le tableau de ce qui vient d'où. Les romans sont dans le domaine public (Projet
Gutenberg).

Les contributeurs sont anonymisés par politesse : quiconque clone ces dépôts
retrouve les noms.
