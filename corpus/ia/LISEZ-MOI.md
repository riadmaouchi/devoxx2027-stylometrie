# La signature de l'IA — ce qui est mesuré ici, et comment le refaire

Le talk avance deux choses. La première — votre code a une signature — est
démontrée sur trois contributeurs réels d'un dépôt Python. La seconde — la machine aussi — est démontrée **ici**, et c'est la seule mesure d'IA du talk qui n'est
pas simulée.

Ne pas confondre avec les profils « assistant » du Live 3 : ceux-là sont du code
que j'ai écrit moi-même pour qu'il soit caractéristique. Ils servent à faire
comprendre les features, pas à prouver quoi que ce soit. Les slides le disent.

## Le corpus

- `assistant.py` — 452 lignes, 39 fonctions et 6 classes, générées par un LLM
  (ChatGPT) en un seul prompt, sans aucune consigne de style, sur le même domaine
  que les humains neufs de `corpus/neuf/` (internals d'un micro-framework web). Version saine :
  l'indentation est intacte, le fichier parse.
- `assistant_via_pdf.py` — exactement le même code, passé par un PDF :
  l'indentation est détruite sur ~20 % des lignes. Gardé exprès. C'est le
  **piège n°2** (le label) en vrai : mesurer des 4-grammes de caractères sur ce fichier-là,
  c'est mesurer le convertisseur PDF, pas la machine.

**Limite de traçabilité :** pour ce fichier, le texte exact du prompt, la date et la version du modèle
n'ont pas été conservés. Le second fichier (`assistant_2.py`, Claude) porte son prompt complet en tête.

## Les résultats mesurés (blocs de 40 lignes, held-out 60/40, 20 tirages)

| test | précision | hasard | rapport |
|---|---|---|---|
| IA contre 3 développeurs de production | **69 %** | 25 % | ×2,8 |
| idem, sans `def` `class` `return` `import` `from` `self` | **74 %** | 25 % | ×3,0 |
| IA contre 3 humains **neufs** (fichiers jamais refactorés) | **72 %** | 25 % | ×2,9 |

95 % des blocs d'IA sont reconnus comme tels dans le premier test, 82 % dans le
troisième. Le signal ne baisse pas face à du code neuf : « neuf contre vieux » n'explique pas
le score. Objection ouverte : tout le code de la machine vient d'un seul fichier.

**Le contre-test du 84 %, appliqué ici** (`experiments/contre_tests.py --ia`). Même protocole,
mais la fenêtre de test est contiguë et glisse sur toutes les positions : plus jamais de
blocs voisins des deux côtés. Le score à quatre candidats tombe à **52 % / 62 % / 66 %**.
La machine, elle, reste reconnue dans **80 à 100 %** de ses blocs, et 7 à 10 % des blocs
humains sont pris pour elle : ce sont les humains qu'elle confond entre eux. 16 décisions
par essai — un bloc de plus ou de moins bien classé, c'est 6 points.

Les trois développeurs de production viennent de `django/django` (corpus contrôlé,
`experiments/construire_corpus.py`) : ils écrivent un ORM et des utilitaires, pas un
micro-framework HTTP. Les trois humains neufs, eux, viennent de `pallets/flask`, le
même domaine que le code généré. C'est le troisième test qui est à domaine égal.

## À quoi elle se reconnaît — 7 mesures, fichier par fichier

Comparaison à la **plage** des six humains, pas à leur moyenne.

| mesure | IA | plage des 6 humains | verdict |
|---|---|---|---|
| compréhensions / 100 lignes | 1,72 | 0,00 – 1,00 | hors, ×1,7 |
| ternaires / 100 lignes | 0,86 | 0,00 – 0,70 | hors, ×1,2 |
| try/except / 100 lignes | 1,72 | 0,00 – 1,70 | hors de 1 % — dans le bruit |
| lignes de commentaire | 0,0 % | 1,2 – 10,0 % | sous les six |
| lignes / fonction | 5,27 | 5,84 – 22,56 | hors de 10 % — dans le bruit |
| type hints / 100 lignes | 0,29 | 0,00 – 0,47 | **dans la plage — ne sépare pas** |
| identifiants de 1-2 caractères | 7,1 % | 4,5 – 12,1 % | **dans la plage — ne sépare pas** |

Trois mesures séparent nettement, deux sont à la limite du bruit sur un fichier
de 348 lignes non vides, deux contredisent l'hypothèse. Les sept sont affichées dans
le talk.

## Un second modèle — l'objection du fichier unique

Tout ce qui précède vient d'un seul fichier, d'un seul modèle. `assistant_2.py` est un second
fichier : Claude, même domaine, un seul prompt sans consigne de style, écrit par un agent qui ne
connaissait pas l'expérience (prompt exact en tête du fichier). `experiments/deux_fichiers_ia.py` :

- **reconnu lui aussi** : 68 / 69 / 77 % avec le protocole publié, 59 / 62 / 71 % avec le test
  durci, 99 à 100 % de ses blocs reconnus ;
- **appris sur un modèle, testé sur l'autre** : 62 à 95 % des blocs reconnus selon la variante —
  mais jusqu'à 45 % de blocs humains pris pour l'IA (appris sur ChatGPT, face aux humains neufs) ;
- **les 7 mesures** : un seul des trois traits de ChatGPT tient, les ternaires (1,36 pour 100 lignes,
  plage humaine 0,00 – 0,70). Claude commente (2,9 % des lignes) et ses compréhensions (0,82)
  restent dans la plage humaine.

Le tableau précédent est la signature de CE modèle. Un signal « machine » existe, une signature
universelle non.

Note : `mesurer_signature.py` (section D) et `mesurer_controles.py` ne comptent pas les ternaires
et les compréhensions avec les mêmes expressions régulières. Les chiffres du talk (slide 15) sont
ceux de `mesurer_controles.py`, que `deux_fichiers_ia.py` reprend à l'identique.

## Le piège du vocabulaire

Si on demande quels *tokens* la machine surutilise, on obtient `strip` ×18,
`response` ×13, `method` ×13, `split` ×13 — le vocabulaire d'un routeur HTTP. Et ce
qu'elle n'écrit jamais : `the`, `django`, `to`, `app` — le vocabulaire des dépôts des
humains.

Le contre-test tue la piste : le **même calcul entre deux humains du même dépôt**
donne `models` ×52, `db` ×37, et « jamais écrit » = `gettext`, `gettext_lazy`, `log`,
`ngettext`. Ce n'est pas un style, c'est un répertoire. (Les rapports sont lissés
à +1 sur les comptes : avec un lissage plus faible, « 48 fois contre 0 » affichait
×1 547, un chiffre qui ne mesurait rien.) C'est le
**piège n°1** (le sujet déguisé), celui des noms de personnages de l'Acte 2,
revenu sur l'IA.

D'où le tableau précédent : purement syntaxique, pas un seul nom de domaine dedans.

## Refaire la mesure

`python3 experiments/mesurer_signature.py` puis `experiments/mesurer_controles.py` reproduisent tous les chiffres
ci-dessus. Dans le notebook, les mêmes mesures sont dans la section
« La signature, en détail ».

Pour la refaire avec **votre** modèle :

1. Demandez 30 à 50 fonctions Python sur un domaine que vos humains connaissent.
   Un seul modèle, un seul prompt, notés dans l'en-tête du fichier.
2. Remplacez `assistant.py`. Ne reformatez pas le résultat : vous mesureriez
   votre formateur (piège n°2).
3. Relancez. Puis lisez le résultat ainsi :
   - **il se sépare** → dites-le pour CE modèle, CE prompt, CE domaine ;
   - **il ne se sépare pas** → c'est un résultat, pas un échec ;
   - **il se sépare trop bien (> 95 %)** → cherchez le confond. Comparez d'abord
     à du code humain neuf, extrait avec `git log --diff-filter=A`.

## Ce que ça ne prouve pas

8 blocs de 40 lignes par candidat : 348 lignes d'IA en tout, d'un seul fichier. Un seul
modèle, un seul prompt, une seule conversation, un seul domaine, un seul langage.

« Cette IA-là est reconnaissable sur ce corpus » — pas « l'IA est reconnaissable ».
