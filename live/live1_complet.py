# LIVE 1 — Les 4 tests de Juola, sur votre code
# Speech : « LIVE 1 » (7:30 → 15:00)
#
# Shift+Enter : execute la cellule et passe a la suivante.
# Sur une ligne « ← xx » : taper xx, puis Tab, puis Shift+Enter.
# Plan B : live/live1_complet.py (meme chose, deja tape), ou le notebook.

# %% Trois developpeurs de django/django, anonymises
from outils import *
charger_devs()

# %% Les trois gestes : compter, normaliser, comparer
# GESTE 1 — une liste : les 41 tokens les plus frequents
MOTS = [t for t, _ in Counter(t for d in DEVS for t in TOKENS[d]).most_common(41)]

# GESTE 2 — compter, normaliser : un passage devient une direction
def vecteur(toks):
    c = Counter(toks); n = max(len(toks), 1)
    v = np.array([c[m] / n for m in MOTS]); k = np.linalg.norm(v)
    return v / k if k > 0 else v

# GESTE 3 — comparer deux directions
def dist(a, b):
    return 1 - float(np.dot(a, b))          # 1 - cosinus

trois_gestes(MOTS, vecteur, dist)

# %% Le texte mystere — la salle vote
montrer_mystere()

# %% Le critere de 2013 : le RANG, pas la distance
def juola(mystere):
    rangs = {d: [] for d in DEVS}
    for nom, test in TESTS:                 # les 4 tests de 2013
        d = {k: cosinus(test(mystere), test(REF[k])) for k in DEVS}
        for rang, k in enumerate(sorted(d, key=d.get), 1):
            rangs[k].append(rang)           # on garde le RANG
    return rangs

tableau_des_rangs(juola(MYSTERE))

# %% Un seul extrait ne prouve rien : les douze
tous_les_extraits(juola)

# %% Combien de code faut-il ?
courbe()
