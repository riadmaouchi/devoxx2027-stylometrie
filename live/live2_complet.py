# LIVE 2 — La mesure apprend-elle l'auteur, ou le sujet ?
# Speech : « LIVE 2 » (15:00 → 17:30)
#
# Shift+Enter : execute la cellule et passe a la suivante.
# Sur une ligne « ← xx » : taper xx, puis Tab, puis Shift+Enter.
# Plan B : live/live2_complet.py (meme chose, deja tape), ou le notebook.

# %% Quatre romans du domaine public
from outils import *
charger_romans()

# %% Deux vocabulaires, deux classifieurs
contenu  = [w for w, _ in POOL.most_common(600) if w not in GRAMMATICAUX and len(w) > 3][:60]
fonction = [w for w, _ in POOL.most_common(400) if w in FONCTIONNELS][:60]

duel(contenu, fonction)

# %% Avant de le garder : qu'a-t-il appris ?
ce_qu_il_a_appris(contenu, fonction)
