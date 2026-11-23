# Licences des corpus

Ce dépôt redistribue des extraits de code de cinq projets libres. Leurs licences
demandent de conserver l'avis de copyright et le texte de la licence : ils sont ici,
copiés tels quels depuis chaque dépôt.

| corpus | vient de | licence | fichier |
|---|---|---|---|
| `corpus/devs/` | github.com/django/django | BSD-3-Clause | `django-LICENSE.txt` |
| `corpus/neuf/`, `corpus/eras/` | github.com/pallets/flask | BSD-3-Clause | `flask-LICENSE.txt` |
| `corpus/projets/werkzeug_*.py` | github.com/pallets/werkzeug | BSD-3-Clause | `werkzeug-LICENSE.txt` |
| `corpus/projets/requests.py` | github.com/psf/requests | Apache-2.0 | `requests-LICENSE.txt`, `requests-NOTICE.txt` |
| `corpus/projets/pyyaml.py` | github.com/yaml/pyyaml | MIT | `pyyaml-LICENSE.txt` |

Ces extraits ont été **modifiés** : ce ne sont pas des fichiers, mais des lignes
choisies et mises bout à bout (lignes ajoutées par un contributeur pour `devs/`,
`neuf/` et `eras/` ; lignes non vides concaténées pour `projets/`). La règle exacte
est dans `experiments/construire_corpus.py` et dans l'en-tête de chaque fichier.

Les quatre romans de `corpus/*.txt` sont dans le domaine public ; les textes
viennent du Projet Gutenberg, préambules d'éditeur retirés
(`experiments/nettoyer_romans.py`).

`corpus/ia/assistant.py` a été généré par un assistant : voir `corpus/ia/LISEZ-MOI.md`.

Ce tableau n'est pas un avis juridique. Si vous réutilisez ces corpus, relisez les
licences.
