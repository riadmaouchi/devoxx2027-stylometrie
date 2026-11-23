# Le live coding, dans VS Code

Le notebook reste la référence et le plan B. Cette version-ci montre le code
**naître à l'écran** : chaque démo part d'un fichier qui ne contient que des
titres, et tu tapes devant la salle ce qui porte l'idée — la signature, les
trois gestes, le critère du rang, les deux vocabulaires, les dix regex.

Tout le reste (charger le corpus, découper, tracer) est déjà écrit dans
`outils.py`, repris ligne pour ligne des cellules du notebook : **mêmes
chiffres à l'écran**. Vérifié : les 61 lignes chiffrées que produisent les
quatre fichiers sont identiques à celles du notebook (une seule phrase est
reformulée, son chiffre ×1,4 est le même).

Le texte du speech ne change pas. Seul le geste change : au lieu de
Shift+Enter sur une cellule déjà écrite, tu tapes un préfixe, Tab, puis
Shift+Enter.

---

## Une fois, à l'installation

1. VS Code, avec les extensions **Python** et **Jupyter** (Microsoft).
2. `pip install -r requirements.txt ipykernel`
3. **File → Open Folder → `devoxx2027-stylometrie/`.** C'est indispensable :
   les snippets (`.vscode/live.code-snippets`) et les réglages de scène
   (`.vscode/settings.json`) ne s'activent que si c'est ce dossier qui est ouvert.
4. *Python: Select Interpreter* → l'environnement où tu viens d'installer.

Les réglages fournis : police à 20, minimap masquée, Tab qui déplie les
snippets, **complétion par IA coupée** (Copilot et suggestions en ligne).
Dans un talk qui demande « qui a écrit ce code ? », une IA qui complète ta
frappe en direct serait le pire moment possible.

---

## Avant de monter sur scène

1. `python live/remettre_a_zero.py` — les quatre fichiers reviennent à leur
   trame de départ (à faire aussi avant chaque répétition).
2. Ouvre `ouverture.py`, `live1.py`, `live2.py`, `live3.py` dans quatre
   onglets, dans cet ordre.
3. **Réveille le noyau** : dans chaque fichier, exécute la première cellule,
   puis vide la fenêtre interactive (bouton *Clear All*). Le premier démarrage
   d'un noyau prend quelques secondes ; sur scène, il doit être déjà chaud.
4. Palette de commandes → **Developer: Toggle Screencast Mode**. La salle voit
   s'afficher les touches que tu frappes, Tab et Shift+Enter compris.
5. Vérifie dans la barre d'état que Copilot est bien désactivé.

---

## Sur scène : un seul geste, toujours le même

Une ligne de titre qui finit par `← l1a` attend du code. Curseur sur la
ligne vide en dessous :

> **taper `l1a` → Tab → laisser 2 secondes le code à l'écran → Shift+Enter**

Shift+Enter exécute la cellule et passe à la suivante ; Ctrl+Enter
l'exécute sans bouger. Les titres sans `←` sont déjà écrits : Shift+Enter
suffit.

Pour que ce soit spectaculaire sans être risqué : après le Tab, **lis à voix
haute une seule ligne**, celle qui porte l'idée. Elle est signalée ci-dessous.

---

## Le déroulé

Chaque cellule s'exécute en **1,1 s au plus** (mesuré, noyau chaud).

### Ouverture — `ouverture.py` (speech 2:00 → 3:30)

| Moment du speech | Geste | À l'écran |
|---|---|---|
| → Afficher les deux extraits | Shift+Enter | les deux fonctions — **vote** |
| → Mettre des chiffres dessus | `o1` Tab, Shift+Enter | camelCase 0,43 / 0,00 · commentaires 0,07 / 0,00 · 14 lignes / 4 + l'image |

Ligne à lire : `'camelCase' : len(re.findall(r'[a-z][A-Z]', src)) / nn` —
« une regex, c'est tout ».

### Live 1 — `live1.py` (speech 7:30 → 15:00)

| Moment du speech | Geste | À l'écran |
|---|---|---|
| → Le corpus, et son assainissement | Shift+Enter | 3 × 3 000 lignes |
| → Les trois gestes, sur du code | `l1a` Tab, Shift+Enter | même développeur **0,051**, deux développeurs **0,071** + l'image |
| → Le texte mystère — FAIRE VOTER | Shift+Enter | 20 lignes sur 400 — **vote** |
| → Lire le tableau des rangs | `l1b` Tab, Shift+Enter | Dev 1 : **1 1 1 1** + la grille |
| → Tous les extraits possibles | `l1c` Tab, Shift+Enter | **7 sur 12**, hasard 4 · 3 sur 3 près des références, 4 sur 9 plus loin |
| → La courbe | `l1d` Tab, Shift+Enter | **50 %** à 5 lignes, **64 %** à 20, **82 %** à 157 + la courbe |

Ligne à lire dans `l1b` : `rangs[k].append(rang)  # on garde le RANG` —
c'est le critère de Juola (« #1 or #2 », Language Log, 2013).

### Live 2 — `live2.py` (speech 15:00 → 17:30)

| Moment du speech | Geste | À l'écran |
|---|---|---|
| → Poser l'expérience | Shift+Enter | les quatre romans, en mots |
| (« J'entraîne deux classifieurs… ») | `l2a` Tab, Shift+Enter | contenu **72 %**, mots-fonction **61 %**, hasard 25 % |
| → Le retournement | `l2b` Tab, Shift+Enter | **fogg, passepartout, phileas** → Verne + l'image |

Ligne à lire dans `l2a` : `if w not in GRAMMATICAUX` — « tout ce qui n'est
pas un mot-outil ». Le retournement arrive tout seul.

### Live 3 — `live3.py` (speech 22:15 → 26:30)

| Moment du speech | Geste | À l'écran |
|---|---|---|
| → Afficher les trois profils | Shift+Enter | les trois profils, **écrits à la main** (c'est affiché) |
| → Le bar chart | `l3a` Tab, Shift+Enter | camelCase 0,30 chez Dev A · type hints 0,30 et docstrings 0,23 chez le profil assistant + le graphique |
| → Le fichier D | Shift+Enter | le fichier — **vote** |
| (révéler) | `l3b` Tab, Shift+Enter | **Assistant**, Dev B juste derrière, Dev A nulle part |

`l3a` insère dix lignes de regex d'un coup : c'est le moment « relisez-les,
il n'y a rien d'autre ». Pas besoin de les lire toutes.

---

## Si quelque chose casse

| Ce qui arrive | Ce que tu fais |
|---|---|
| Faute de frappe dans le préfixe | Ctrl+Z, retape le préfixe |
| Une cellule plante | Ouvre `live/<nom>_complet.py` : mêmes titres, déjà tapés. Même cellule, Shift+Enter |
| `ModuleNotFoundError: outils` | Le dossier ouvert n'est pas `devoxx2027-stylometrie/` (étape 3 de l'installation). Sur scène : passe au notebook |
| Le noyau ne répond plus | Le notebook : ses sorties sont sauvegardées, rien à exécuter |
| VS Code lui-même | Terminal : `python live/live1_complet.py` (chaque figure s'ouvre dans une fenêtre) |

**Le temps.** Le speech fait 38:45 pour 40:00. Le live coding ajoute neuf
frappes de préfixe, quelques secondes chacune. À répéter chrono en main : si
tu dépasses 15:30 à la fin du Live 1, ouvre `live2_complet.py` et
`live3_complet.py` pour la suite.

---

## Les fichiers

| Fichier | Rôle |
|---|---|
| `ouverture.py`, `live1.py`, `live2.py`, `live3.py` | ce que la salle voit au départ : des titres |
| `*_complet.py` | la même chose, déjà tapée — plan B, et référence |
| `outils.py` | tout ce qu'on ne tape pas, repris du notebook |
| `trames/` | les états de départ, que `remettre_a_zero.py` recopie |
| `../.vscode/live.code-snippets` | les 9 snippets : `o1`, `l1a` à `l1d`, `l2a`, `l2b`, `l3a`, `l3b` |
| `../.vscode/settings.json` | les réglages de scène |

Trame + snippets = version complète, caractère pour caractère : c'est vérifié
à la génération. Si tu modifies un snippet, modifie aussi le `*_complet.py`
correspondant.
