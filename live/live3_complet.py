# LIVE 3 — Votre code, puis celui de la machine
# Speech : « LIVE 3 » (22:15 → 26:30)
#
# Shift+Enter : execute la cellule et passe a la suivante.
# Sur une ligne « ← xx » : taper xx, puis Tab, puis Shift+Enter.
# Plan B : live/live3_complet.py (meme chose, deja tape), ou le notebook.

# %% Trois profils, ECRITS A LA MAIN pour la demo
from outils import *
montrer_profils()

# %% Dix mesures. Que du regex et des compteurs.
def sig(src):
    lines = src.split('\n')
    ne    = [l for l in lines if l.strip()]
    n     = max(len(ne), 1)
    names = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]+)\b', src)
    nn    = max(len(names), 1)
    nfun  = max(len(re.findall(r'\bdef\s', src)), 1)
    return [
        len(re.findall(r'[a-z][A-Z]', src)) / nn,                                    # camelCase
        len([x for x in names if '_' in x and x == x.lower() and len(x) > 2]) / nn,  # snake_case
        sum(1 for l in lines if l.strip().startswith('#')) / n,                      # commentaires
        len(re.findall(r':\s*(int|str|float|bool|list|dict|tuple)', src)) / n,       # type hints
        len(re.findall(r'"""', src)) / n,                                            # docstrings
        len(re.findall(r'\[.+for .+in .+\]', src)) / n,                              # list comp
        len(re.findall(r'==\s*None|!=\s*None', src)) / n,                            # == None
        len(re.findall(r'range\s*\(\s*len\s*\(', src)) / n,                          # range(len())
        len(re.findall(r'\bwith\s+open', src)) / n,                                  # with open
        min(len(ne) / nfun / 12, 1.0),                                               # lignes/fonction
    ]

empreintes(sig)

# %% Un fichier que le modele n a jamais vu — la salle vote
montrer_fichier('D')

# %% La reponse
reveler()
