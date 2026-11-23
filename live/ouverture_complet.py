# OUVERTURE — Deux fonctions, deux personnes
# Speech : « OUVERTURE — Deux fonctions, deux personnes » (2:00 → 3:30)
#
# Shift+Enter : execute la cellule et passe a la suivante.
# Sur une ligne « ← xx » : taper xx, puis Tab, puis Shift+Enter.
# Plan B : live/ouverture_complet.py (meme chose, deja tape), ou le notebook.

# %% Deux fonctions. Meme resultat. Pas le meme auteur.
from outils import *          # ce qu on ne tape pas : live/outils.py
montrer_extraits()

# %% Mettre des chiffres dessus
def signature(src):
    lignes = [l for l in src.split('\n') if l.strip()]
    n = max(len(lignes), 1)
    noms = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]+)\b', src); nn = max(len(noms), 1)
    return {
        'camelCase'      : len(re.findall(r'[a-z][A-Z]', src)) / nn,
        'snake_case'     : len([x for x in noms if '_' in x and x == x.lower() and len(x) > 2]) / nn,
        'commentaires'   : sum(1 for l in lignes if l.strip().startswith('#')) / n,
        '== None'        : len(re.findall(r'==\s*None', src)) / n,
        'range(len(...))': len(re.findall(r'range\s*\(\s*len\s*\(', src)) / n,
        'lignes'         : n,
    }

comparer(signature)
