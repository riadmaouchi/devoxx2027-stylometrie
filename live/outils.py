"""
outils.py — tout ce qu'on NE tape PAS sur scene.

Le live coding ne montre que ce qui porte l'idee : la signature, les trois
gestes, le critere du rang, les deux vocabulaires. Le reste — charger le
corpus, decouper, tracer — est ici, deja ecrit.

Chaque fonction de ce fichier reprend, ligne pour ligne, la cellule
correspondante du notebook devoxx2027-livecoding.ipynb : memes donnees,
memes graines aleatoires, donc memes chiffres a l'ecran.

Aucune dependance hors numpy et matplotlib. Aucun appel reseau.
"""
import os
import re
from collections import Counter

import numpy as np
from math import comb
import matplotlib.pyplot as plt


# ── LE DEPOT : trouve depuis n'importe quel dossier de travail ───────────────
def _trouver_le_depot():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):
        for cand in (d, os.path.join(d, 'devoxx2027-stylometrie')):
            if os.path.isfile(os.path.join(cand, 'corpus', 'devs', 'dev_1.py')):
                return cand
        d = os.path.dirname(d)
    raise FileNotFoundError(
        "corpus/ introuvable : live/ doit rester DANS le dossier devoxx2027-stylometrie/.")


os.chdir(_trouver_le_depot())

# ── PALETTE DE SCENE (la meme que le notebook) ───────────────────────────────
ACCENT, BLEU, VIOLET = '#E4611F', '#0C8EC7', '#8B5CF6'
FOND, PANNEAU = '#0D1117', '#161B22'
ENCRE, ENCRE2, GRIS = '#E6EDF3', '#9CA3AF', '#30363D'


def scene(w=14, h=6):
    """Une figure prete a projeter : fond sombre, axes recessifs, gros texte."""
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(FOND); ax.set_facecolor(FOND)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=ENCRE2, labelsize=14, length=0)
    ax.grid(axis='x', color=GRIS, lw=0.8, alpha=.6); ax.set_axisbelow(True)
    return fig, ax


def _cadre(titre, largeur=56):
    print('╔' + '═' * largeur + '╗')
    print(f'║  {titre:<{largeur - 2}}║')
    print('╚' + '═' * largeur + '╝')


# ═════════════════════════════════════════════════════════════════════════════
# OUVERTURE — deux fonctions, deux personnes
# ═════════════════════════════════════════════════════════════════════════════
EXTRAIT_1 = """
# Tri des elements d une liste
def sortElements(inputList, reverseOrder):
    if inputList == None or len(inputList) == 0:
        return []
    resultList = []
    for i in range(len(inputList)):
        resultList.append(inputList[i])
    for i in range(len(resultList)):
        for j in range(i + 1, len(resultList)):
            if resultList[i] > resultList[j]:
                tempValue = resultList[i]
                resultList[i] = resultList[j]
                resultList[j] = tempValue
    return resultList
"""

EXTRAIT_2 = """
def sort_elements(lst, reverse=False):
    if not lst:
        return []
    return sorted(lst, reverse=reverse)
"""


def montrer_extraits():
    for titre, src in [('EXTRAIT 1', EXTRAIT_1), ('EXTRAIT 2', EXTRAIT_2)]:
        _cadre(titre)
        for l in src.strip().split('\n'):
            print('  ' + l)
        print()
    print('─' * 58)
    print('  Deux personnes ? Ou la même, deux jours différents ?')
    print('─' * 58)


def comparer(signature):
    """Le tableau des six nombres, puis l'image — avec la fonction tapee en direct."""
    s1, s2 = signature(EXTRAIT_1), signature(EXTRAIT_2)
    print(f"{'':20}{'extrait 1':>12}{'extrait 2':>12}")
    print('-' * 44)
    for k in s1:
        v1, v2 = s1[k], s2[k]
        fmt = (lambda v: f'{v:>12.0f}') if k == 'lignes' else (lambda v: f'{v:>12.2f}')
        flag = '   <--' if abs(v1 - v2) > (2 if k == 'lignes' else 0.05) else ''
        print(f'  {k:<18}{fmt(v1)}{fmt(v2)}{flag}')
    print('-' * 44)
    print()
    print('Six nombres. Aucun ne parle de ce que fait la fonction.')
    print('Tous parlent de qui l a ecrite.')
    _cles = [k for k in s1 if k != 'lignes'][::-1]
    fig, ax = scene(12.5, 4.2)
    for i, k in enumerate(_cles):
        v1, v2 = s1[k], s2[k]
        ax.plot([v1, v2], [i, i], color=GRIS, lw=3, zorder=2)
        ax.scatter([v1], [i], s=270, color=ACCENT, zorder=4)
        ax.scatter([v2], [i], s=270, color=BLEU, zorder=4)
        for v in (v1, v2):
            ax.text(v, i + .28, f'{v:.2f}', color=ENCRE2, fontsize=13, ha='center', va='bottom')
    ax.set_yticks(range(len(_cles))); ax.set_yticklabels(_cles, color=ENCRE, fontsize=15)
    ax.set_xticks([]); ax.set_xlim(-.05, .52); ax.set_ylim(-.6, len(_cles) - .15)
    ax.scatter([], [], s=200, color=ACCENT, label='extrait 1')
    ax.scatter([], [], s=200, color=BLEU, label='extrait 2')
    leg = ax.legend(loc='lower right', fontsize=15, frameon=False)
    for t in leg.get_texts(): t.set_color(ENCRE)
    ax.set_title("Cinq mesures, cinq ecarts. Aucune ne parle de ce que fait la fonction.\n"
                 f"(et {s1['lignes']:.0f} lignes contre {s2['lignes']:.0f})",
                 color='white', fontsize=17, fontweight='bold', pad=16, loc='left')
    ax.title.set_linespacing(1.6)
    plt.tight_layout(); plt.show()


# ═════════════════════════════════════════════════════════════════════════════
# LIVE 1 — trois developpeurs de django/django, les 4 tests de 2013
# ═════════════════════════════════════════════════════════════════════════════
DEVS = {f'Dev {i}': f'corpus/devs/dev_{i}.py' for i in (1, 2, 3)}


def _charger_code(chemin):
    # On ne retire QUE les deux lignes d'en-tete ajoutees par l'extraction.
    return [l for l in open(chemin, encoding='utf-8').read().split('\n')
            if l.strip() and not l.startswith('# Lignes ajoutees')
            and not l.startswith('# Extraites')]


CODE = {d: _charger_code(p) for d, p in DEVS.items()}
REF = {d: '\n'.join(CODE[d][:1200]) for d in DEVS}            # 1 200 lignes de reference
tokens = lambda src: re.findall(r'[A-Za-z_]+|[^\sA-Za-z_]', src)   # un mot, ou un signe
TOKENS = {d: tokens('\n'.join(CODE[d])) for d in DEVS}
MYSTERE = '\n'.join(CODE['Dev 1'][1300:1700])                  # 400 lignes jamais vues
_QUI = 'Dev 1'


def charger_devs():
    for d in DEVS:
        print(f'  {d} : {len(CODE[d]):>6,} lignes'.replace(',', ' '))
    print('\nReferences : 1 200 lignes par developpeur.')
    print('Corpus controle : meme depot, meme epoque, meme type de code.')


def trois_gestes(MOTS, vecteur, dist, N=2000):
    """Les trois gestes tapes en direct, appliques a quelques centaines de paires."""
    _v = vecteur(TOKENS['Dev 1'][:N])
    print(f'GESTE 1   {len(MOTS)} tokens :  ' + '  '.join(MOTS[:22]) + '  ...')
    print(f'GESTE 2   un passage de Dev 1, {N} tokens  ->  {len(_v)} nombres, longueur {np.linalg.norm(_v):.2f}')
    print('          [' + '  '.join(f'{x:.2f}' for x in _v[:9]) + '  ...]')
    _rng = np.random.default_rng(1); _meme, _autre = [], []; _noms = list(DEVS)
    for _ in range(600):
        d = _noms[_rng.integers(3)]; e = _noms[(_noms.index(d) + 1 + _rng.integers(2)) % 3]
        a, b = _rng.integers(0, len(TOKENS[d]) - N, 2); c = _rng.integers(0, len(TOKENS[e]) - N)
        if abs(a - b) < N: continue
        _meme.append(dist(vecteur(TOKENS[d][a:a + N]), vecteur(TOKENS[d][b:b + N])))
        _autre.append(dist(vecteur(TOKENS[d][a:a + N]), vecteur(TOKENS[e][c:c + N])))
    _dm, _da = float(np.median(_meme)), float(np.median(_autre))
    print(f'GESTE 3   distance mediane entre deux passages, sur {len(_meme)} paires :')
    print(f'             meme developpeur        {_dm:.3f}')
    print(f'             deux developpeurs       {_da:.3f}')
    _p = {d: {m: 1000 * Counter(TOKENS[d])[m] / len(TOKENS[d]) for m in MOTS} for d in ('Dev 1', 'Dev 2')}
    _top = sorted(MOTS, key=lambda m: -abs(_p['Dev 1'][m] - _p['Dev 2'][m]))[:8][::-1]
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={'width_ratios': [1.55, 1]})
    fig.patch.set_facecolor(FOND)
    for a_ in (ax, bx):
        a_.set_facecolor(FOND)
        for sp in a_.spines.values(): sp.set_visible(False)
        a_.tick_params(colors=ENCRE2, labelsize=14, length=0)
    y = np.arange(len(_top)); h = .38
    ax.barh(y + h / 2, [_p['Dev 1'][m] for m in _top], height=h, color=ACCENT, zorder=3)
    ax.barh(y - h / 2, [_p['Dev 2'][m] for m in _top], height=h, color=BLEU, zorder=3)
    _nom = {'"': '"  double', "'": "'  simple", '`': '`  backtick'}
    ax.set_yticks(y); ax.set_yticklabels([_nom.get(m, m) for m in _top], color=ENCRE, fontsize=19,
                                         fontweight='bold', family='monospace')
    ax.grid(axis='x', color=GRIS, lw=.8, alpha=.6); ax.set_axisbelow(True)
    ax.set_xlabel('occurrences pour 1 000 tokens', color=ENCRE2, fontsize=13)
    ax.text(.99, .14, 'Dev 1', color=ACCENT, fontsize=17, fontweight='bold', ha='right', transform=ax.transAxes)
    ax.text(.99, .05, 'Dev 2', color=BLEU, fontsize=17, fontweight='bold', ha='right', transform=ax.transAxes)
    ax.set_title(f'Le vecteur : Dev 1 contre Dev 2, 8 tokens sur {len(MOTS)}',
                 color='white', fontsize=16, fontweight='bold', pad=14, loc='left')
    bx.barh([1, 0], [_dm, _da], height=.5, color=[GRIS, VIOLET], zorder=3)
    for yy, vv, nn in ((1, _dm, 'meme developpeur'), (0, _da, 'deux developpeurs')):
        bx.text(vv + .006, yy, f'{vv:.3f}', color='white', fontsize=26, fontweight='bold', va='center')
        bx.text(0, yy + .36, nn, color=ENCRE, fontsize=15, va='bottom')
    bx.set_xlim(0, _da * 1.5); bx.set_ylim(-.55, 1.8); bx.set_xticks([]); bx.set_yticks([])
    bx.set_title("L'angle : distance entre deux passages", color='white', fontsize=16,
                 fontweight='bold', pad=14, loc='left')
    plt.tight_layout(); plt.show()
    print(f'Un ecart de x{_da / _dm:.1f}. Il est la, et il est mince : il faut du volume, et plusieurs mesures.')


# Les 4 familles de mesures de 2013, transposees au code (notebook, cellule 12)
_ALL = '\n'.join(REF.values())
_TOK = tokens
VOC100 = [w for w, _ in Counter(_TOK(_ALL)).most_common(100)]
PAIRS = [p for p, _ in Counter(zip(_TOK(_ALL), _TOK(_ALL)[1:])).most_common(300)]
GRAMS = [g for g, _ in Counter(_ALL[i:i + 4] for i in range(len(_ALL) - 3)).most_common(300)]


def t_identifiants(s):
    w = re.findall(r'[A-Za-z_]+', s); c = Counter(min(len(x), 15) for x in w)
    n = max(len(w), 1)
    return np.array([c.get(i, 0) / n for i in range(1, 16)])


def t_tokens(s):
    t = _TOK(s); c = Counter(t); n = max(len(t), 1)
    return np.array([c.get(w, 0) / n for w in VOC100])


def t_paires(s):
    t = _TOK(s); c = Counter(zip(t, t[1:])); n = max(len(t) - 1, 1)
    return np.array([c.get(p, 0) / n for p in PAIRS])


def t_grammes(s):
    c = Counter(s[i:i + 4] for i in range(len(s) - 3)); n = max(len(s) - 3, 1)
    return np.array([c.get(g, 0) / n for g in GRAMS])


TESTS = [('longueur identifiants', t_identifiants), ('100 tokens frequents', t_tokens),
         ('paires de tokens', t_paires), ('4-grammes', t_grammes)]


def cosinus(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return 1 - np.dot(a, b) / (na * nb) if na > 0 and nb > 0 else 1.0


def _fenetre_lisible(lignes, n=20):
    code = re.compile(r'^\s*(def |class |if |for |while |return|import |from |'
                      r'try|except|with |elif |else:|raise |assert )|=')
    score = [1 if code.search(l) else 0 for l in lignes]
    cumul = np.cumsum([0] + score)
    best = max(range(len(lignes) - n + 1), key=lambda i: cumul[i + n] - cumul[i])
    return lignes[best:best + n], cumul[best + n] - cumul[best]


def montrer_mystere():
    _vue, _dense = _fenetre_lisible(CODE[_QUI][1300:1700])
    print('Lignes AJOUTEES par ce contributeur, concatenees dans l ordre des')
    print('commits. Ce n est pas un fichier — c est ce que git sait de lui.')
    print('─' * 62)
    print('\n'.join(_vue))
    print('...')
    print('─' * 62)
    print(f'  (20 lignes sur les 400 que la mesure va lire — {_dense} portent du code)')
    print('  Dev 1 ?    Dev 2 ?    Dev 3 ?')
    print('─' * 62)


def tableau_des_rangs(rangs):
    moy = {d: np.mean(rangs[d]) for d in DEVS}
    print(f"{'candidat':<10}" + ''.join(f'{n[:19]:>22}' for n, _ in TESTS) + f"{'moyenne':>10}")
    print('-' * 100)
    for d in sorted(DEVS, key=lambda x: moy[x]):
        print(f'{d:<10}' + ''.join(f'{r:>22}' for r in rangs[d]) + f'{moy[d]:>10.2f}'
              + ('   <--' if moy[d] == min(moy.values()) else ''))
    print('-' * 100)
    gagnant = min(moy, key=moy.get)
    print(f'\n  Attribution : {gagnant}     Reponse : {_QUI}   ' + ('OK' if gagnant == _QUI else 'RATE'))
    _r = rangs[_QUI]
    print('  Premier a chaque test.' if max(_r) == 1 else
          '  Premier ou deuxieme a chaque test.' if max(_r) <= 2 else
          '  Premier ou deuxieme a presque chaque test.')
    from matplotlib.colors import LinearSegmentedColormap
    _cmap = LinearSegmentedColormap.from_list('rangs', ['#E4611F', '#7A3514', '#241208'])
    _ordre = sorted(DEVS, key=lambda d: np.mean(rangs[d]))
    _R = np.array([rangs[d] for d in _ordre], dtype=float)
    fig, ax = scene(12.5, 3.9)
    ax.grid(False)
    ax.imshow(_R, cmap=_cmap, vmin=1, vmax=len(DEVS), aspect='auto')
    for yy in range(_R.shape[0]):
        for xx in range(_R.shape[1]):
            ax.text(xx, yy, int(_R[yy, xx]), ha='center', va='center', fontsize=30,
                    fontweight='bold', color='white' if _R[yy, xx] > 1 else FOND)
    ax.set_xticks(range(len(TESTS)))
    ax.set_xticklabels([n for n, _ in TESTS], color=ENCRE, fontsize=14)
    ax.set_yticks(range(len(_ordre)))
    ax.set_yticklabels([f'{d}   ' for d in _ordre], color=ENCRE, fontsize=17, fontweight='bold')
    ax.get_yticklabels()[0].set_color(ACCENT)
    ax.set_title("Premier ou deuxieme a chaque test — le critere de Juola, 2013.\n"
                 f"Reponse : {_QUI}.   Le rang moyen le plus bas donne l'attribution.",
                 color='white', fontsize=17.5, fontweight='bold', pad=14, loc='left')
    ax.title.set_linespacing(1.7)
    plt.tight_layout(); plt.show()


def tous_les_extraits(juola):
    print('Quatre extraits de 400 lignes par developpeur, jamais vus par les references.')
    print('Entre crochets : son rang aux quatre tests.\n')
    bons = tot = 0; _pres, _loin = [0, 0], [0, 0]
    for vrai in DEVS:
        ligne = []
        for n, a in enumerate(range(1300, len(CODE[vrai]) - 399, 400)):
            r = juola('\n'.join(CODE[vrai][a:a + 400])); moy = {d: np.mean(r[d]) for d in DEVS}
            ok = min(moy, key=moy.get) == vrai
            bons += ok; tot += 1
            q = _pres if n == 0 else _loin
            q[0] += ok; q[1] += 1
            ligne.append(f"{'OK  ' if ok else 'RATE'} {r[vrai]}")
        print(f'  {vrai} :  ' + '   '.join(ligne))
    print()
    print(f'  {bons} sur {tot}.  Hasard : {tot // 3} sur {tot}.')
    _p = sum(comb(tot, k) * (1/3)**k * (2/3)**(tot - k) for k in range(bons, tot + 1))
    print(f'  Pris seul, c est un indice : au hasard, {bons} bons ou plus arrivent {_p*100:.1f} % du temps.')
    print(f'  L extrait qui suit juste les references : {_pres[0]} sur {_pres[1]}.')
    print(f'  Les extraits ecrits plus tard           : {_loin[0]} sur {_loin[1]}.')


def courbe():
    """Le Delta de Burrows a 3 candidats, sur des extraits de plus en plus longs."""
    VOC = [w for w, _ in sum((Counter(t) for t in TOKENS.values()), Counter()).most_common(150)]
    _PAR_LIGNE = sum(len(t) for t in TOKENS.values()) / sum(len(CODE[d]) for d in DEVS)

    def precision_a(taille, tirages=30, seed=42):
        B = {d: [TOKENS[d][i:i + taille] for i in range(0, len(TOKENS[d]) - taille + 1, taille)] for d in DEVS}
        k = min(len(b) for b in B.values())
        if k < 6:
            return None, 0

        def _freq(bloc):
            c = Counter(bloc)
            return [c[w] / taille for w in VOC]
        X = {d: np.array([_freq(b) for b in B[d][:k]]) for d in DEVS}
        pool = np.vstack(list(X.values())); mu = pool.mean(0); sd = pool.std(0); sd[sd == 0] = 1
        Z = {d: (X[d] - mu) / sd for d in DEVS}
        rng = np.random.default_rng(seed); ntr = max(2, int(k * 0.6)); scores = []
        for _ in range(tirages):
            idx = {d: rng.permutation(k) for d in DEVS}
            cen = {d: Z[d][idx[d][:ntr]].mean(0) for d in DEVS}
            bon = tot = 0
            for d in DEVS:
                for i in idx[d][ntr:]:
                    dd = {e: np.abs(Z[d][i] - cen[e]).mean() for e in DEVS}
                    bon += min(dd, key=dd.get) == d; tot += 1
            scores.append(bon / tot)
        return float(np.mean(scores)), k

    TAILLES = [50, 100, 200, 400, 800, 1600]
    PRECISION = []
    print(f"{'tokens/extrait':>15} {'soit, en lignes':>16} {'extraits':>10} {'precision':>11}")
    print('-' * 56)
    for t in TAILLES:
        a, k = precision_a(t)
        PRECISION.append(a * 100)
        print(f'{t:>15} {t / _PAR_LIGNE:>15.0f}  {k:>10} {a * 100:>10.0f} %')
    print('-' * 56)
    print('hasard = 33 %   ·   3 developpeurs, un seul depot')
    fig, ax = scene(13, 5.6)
    ax.grid(False, axis='x'); ax.grid(True, axis='y', color=GRIS, lw=.8, alpha=.6)
    ax.axhline(33.3, color=ENCRE2, ls='--', lw=2)
    ax.text(TAILLES[-1], 35, 'hasard  33 %', color=ENCRE2, fontsize=14, style='italic', ha='right')
    ax.plot(TAILLES, PRECISION, color=ACCENT, lw=3.5, marker='o', ms=13, mec=FOND, mew=2.5, zorder=5)
    for x, y in zip(TAILLES, PRECISION):
        ax.annotate(f'{y:.0f} %', (x, y), textcoords='offset points', xytext=(0, 16), ha='center',
                    color='white', fontsize=17, fontweight='bold')
    ax.set_xscale('log'); ax.set_xticks(TAILLES); ax.minorticks_off()
    ax.set_xlim(TAILLES[0] * .78, TAILLES[-1] * 1.3)
    ax.set_xticklabels([f'{t} tokens\n{t / _PAR_LIGNE:.0f} lignes' for t in TAILLES], color=ENCRE, fontsize=13)
    ax.set_ylim(25, 100); ax.set_yticks([40, 60, 80]); ax.set_yticklabels(['40 %', '60 %', '80 %'])
    ax.set_title('La methode marche. Elle a besoin de volume.',
                 color='white', fontsize=19, fontweight='bold', pad=18, loc='left')
    plt.tight_layout(); plt.show()


# ═════════════════════════════════════════════════════════════════════════════
# LIVE 2 — quatre romans : l'auteur, ou le sujet ?
# ═════════════════════════════════════════════════════════════════════════════
AUTEURS = {'Zola': 'corpus/zola_germinal.txt', 'Maupassant': 'corpus/maupassant_boule_de_suif.txt',
           'Flaubert': 'corpus/flaubert_madame_bovary.txt', 'Verne': 'corpus/verne_tour_du_monde.txt'}


def _charger_roman(chemin):
    txt = open(chemin, encoding='utf-8').read()
    txt = '\n'.join(l for l in txt.split('\n') if not l.startswith('#'))
    return re.findall(r'[a-zA-Z]+', txt.lower())


_T = {a: _charger_roman(p) for a, p in AUTEURS.items()}
FONCTIONNELS = set(('le la les un une des de du et ou mais donc ni car que qui dans sur '
                    'avec sans pour par il elle ils elles je tu nous vous ne pas plus tres '
                    'bien tout tous rien ce se son sa ses leur a au aux en y d l s c n j m t '
                    'qu est etait sont ete avoir etre fait').split())
# « comme » et « cette » ne sont pas dans la liste ci-dessus, mais ce sont des mots
# grammaticaux : on les ecarte aussi du vocabulaire de CONTENU (audit du 3 novembre 2026).
GRAMMATICAUX = FONCTIONNELS | {'comme', 'cette'}
_n = min(len(t) for t in _T.values())
TT = {a: _T[a][:_n] for a in AUTEURS}
POOL = Counter(sum(TT.values(), []))                          # tous les mots des 4 romans


def charger_romans():
    for a in AUTEURS:
        print(f'  {a:12s} {len(_T[a]):>7,} mots')


def _freq(tk, voc):
    n = len(tk); c = Counter(tk)
    return np.array([c.get(w, 0) / n for w in voc])


def _vec(tk, voc):
    v = _freq(tk, voc); k = np.linalg.norm(v)
    return v / k if k > 0 else v


def _precision(voc, tirages=20, seed=3):
    rng = np.random.default_rng(seed); accs = []
    for _ in range(tirages):
        cent = {}; tests = []
        for a in AUTEURS:
            b = [TT[a][i:i + 1000] for i in range(0, len(TT[a]) - 999, 1000)]
            h = len(b) // 2
            idx = rng.permutation(h)[:max(4, h // 2)]
            cent[a] = np.mean([_vec(b[i], voc) for i in idx], axis=0)
            for j in rng.permutation(range(h, len(b)))[:6]:
                tests.append((a, _vec(b[j], voc)))
        ok = sum(1 for vrai, v in tests if min(cent, key=lambda x: 1 - np.dot(v, cent[x])) == vrai)
        accs.append(ok / len(tests))
    return float(np.mean(accs))


_DUEL = {}


def duel(contenu, fonction):
    _DUEL['contenu'], _DUEL['fonction'] = _precision(contenu), _precision(fonction)
    pc, pf = _DUEL['contenu'], _DUEL['fonction']
    print('Attribution sur 4 auteurs, extraits de 1 000 mots tenus a l ecart :')
    print('-' * 58)
    print(f'  mots de CONTENU   {pc * 100:5.0f} %   {"#" * int(pc * 34)}')
    print(f'  mots-FONCTION     {pf * 100:5.0f} %   {"#" * int(pf * 34)}')
    print('-' * 58)
    print(f'  hasard             {25:5.0f} %')


def _discriminants(voc, k=6):
    M = np.array([_freq(TT[a], voc) for a in AUTEURS])
    noms = list(AUTEURS)
    ecart = M.max(axis=0) - M.min(axis=0)
    return [(voc[i], noms[int(np.argmax(M[:, i]))]) for i in np.argsort(ecart)[::-1][:k]]


def ce_qu_il_a_appris(contenu, fonction):
    pc = _DUEL.get('contenu') or _precision(contenu)
    pf = _DUEL.get('fonction') or _precision(fonction)
    for titre, p, voc in ((f'MOTS DE CONTENU — le classifieur a {pc * 100:.0f} %', pc, contenu),
                          (f'MOTS-FONCTION — le classifieur a {pf * 100:.0f} %', pf, fonction)):
        print(titre)
        print('-' * 48)
        for w, a in _discriminants(voc):
            print(f'   {w:18s} -> {a}')
        print()
    fig, ax = scene(13, 4.4)
    _v = [pc * 100, pf * 100]
    ax.barh([1, 0], _v, height=.46, color=[ACCENT, BLEU], zorder=3)
    ax.axvline(25, color=ENCRE2, ls='--', lw=2, zorder=4)
    ax.text(25, 1.55, ' hasard  25 %', color=ENCRE2, fontsize=15, style='italic', va='bottom')
    for y, v in zip([1, 0], _v):
        ax.text(v - 1.5, y, f'{v:.0f} %', color='white', fontsize=30, fontweight='bold',
                va='center', ha='right', zorder=5)
    for y, (lbl, voc) in zip([1, 0], [('mots de CONTENU', contenu), ('mots-FONCTION', fonction)]):
        ax.text(1.5, y + .30, lbl, color=ENCRE, fontsize=15, fontweight='bold', va='bottom')
        ax.text(1.5, y - .30, 'a appris :  ' + '   '.join(w for w, _ in _discriminants(voc, 3)),
                color=ENCRE2, fontsize=14.5, va='top', style='italic')
    ax.set_yticks([]); ax.set_xticks([]); ax.set_xlim(0, 100); ax.set_ylim(-.75, 1.9)
    ax.set_title("Le meilleur des deux a appris des noms de personnages.",
                 color='white', fontsize=18, fontweight='bold', pad=20, loc='left')
    plt.tight_layout(); plt.show()


# ═════════════════════════════════════════════════════════════════════════════
# LIVE 3 — trois profils ECRITS A LA MAIN pour la demo, puis le fichier D
# ═════════════════════════════════════════════════════════════════════════════
DEV_A = '''
# Tri des elements d une liste
def sortElements(inputList, reverseOrder):
    if inputList == None or len(inputList) == 0:
        return []
    resultList = []
    for i in range(len(inputList)):
        resultList.append(inputList[i])
    for i in range(len(resultList)):
        for j in range(i + 1, len(resultList)):
            if resultList[i] > resultList[j]:
                tempValue = resultList[i]
                resultList[i] = resultList[j]
                resultList[j] = tempValue
    return resultList
'''

DEV_B = '''
def sort_elements(lst, reverse=False):
    if not lst:
        return []
    return sorted(lst, reverse=reverse)
'''

COPILOT = '''
def sort_elements(
        elements: list,
        reverse: bool = False
) -> list:
    """
    Sort a list of elements.
    Args:
        elements: The list to sort.
        reverse: Descending if True.
    Returns:
        Sorted list.
    """
    if not elements:
        return []
    return sorted(elements, reverse=reverse)
'''

A_all = [DEV_A,
    '''def parseConfig(filePath):
    configDict = {}
    for line in open(filePath).read().split(chr(10)):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k = line[:line.index('=')].strip()
            configDict[k] = line[line.index('=')+1:].strip()
    return configDict''',
    '''def calculateStats(numList):
    if numList == None: return None
    total = 0
    for i in range(len(numList)): total += numList[i]
    return {'mean': total/len(numList), 'min': min(numList), 'max': max(numList)}''']

B_all = [DEV_B,
    '''def parse_config(path):
    cfg = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            k, _, v = line.partition('=')
            cfg[k.strip()] = v.strip()
    return cfg''',
    '''def stats(nums):
    if not nums: return None
    clean = [x for x in nums if x is not None]
    return {'mean': sum(clean)/len(clean), 'min': min(clean), 'max': max(clean)}''']

C_all = [COPILOT,
    '''def parse_config(file_path: str) -> dict:
    """Parse key-value config file.
    Args: file_path: path to config.
    Returns: parsed dict."""
    config: dict = {}
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()
    return config''',
    '''def calculate_stats(values: list[float]) -> dict | None:
    """Calculate descriptive stats. Args: values: list of floats.",
    Returns: dict with mean/min/max or None."""
    if not values: return None
    return {"mean": sum(values)/len(values), "min": min(values), "max": max(values)}''']

FEATS = ['camelCase', 'snake_case', 'Commentaires', 'Type hints', 'Docstrings',
         'List comp', '== None', 'range(len())', 'with open', 'Lignes/fonction']

FICHIERS = {
    'D': '''
def filter_records(
        records: list,
        min_score: float = 0.0
) -> list:
    """Filter records above minimum score threshold."""
    if not records: return []
    return [r for r in records if r.get('score', 0) >= min_score]
''',
}


def montrer_profils():
    print('/!\\  PROFILS ILLUSTRATIFS — ecrits a la main pour la demo.')
    print("    Le profil « ASSISTANT » n'est pas une sortie d'assistant : je l'ai ecrit.")
    print()
    for label, src in [('DEV A  —  Java-style    (camelCase, commentaires)', DEV_A),
                       ('DEV B  —  Pythoniste    (snake_case, compact)', DEV_B),
                       ('ASSISTANT  —  illustratif  (type hints, docstrings)', COPILOT)]:
        _cadre(label, 62)
        for line in src.strip().split('\n'):
            print(f'  {line}')
        print()


_ETAT = {}


def empreintes(sig):
    """Dix nombres par profil, on trace — avec la fonction tapee en direct."""
    assert len(sig(DEV_A)) == len(FEATS), f'sig() doit rendre {len(FEATS)} nombres'
    _all = np.array([sig(f) for f in A_all + B_all + C_all])
    scale = np.where(_all.max(axis=0) > 0, _all.max(axis=0), 1.0)
    SA = np.mean([sig(f) for f in A_all], axis=0)
    SB = np.mean([sig(f) for f in B_all], axis=0)
    SC = np.mean([sig(f) for f in C_all], axis=0)

    def vecteur_code(src):
        v = np.array(sig(src)) / scale
        n = np.linalg.norm(v)
        return v / n if n > 0 else v
    _ETAT.update(vecteur=vecteur_code,
                 centres={nom: np.mean([vecteur_code(f) for f in fs], axis=0)
                          for nom, fs in (('Dev A', A_all), ('Dev B', B_all), ('Assistant', C_all))})
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#0D1117'); ax.set_facecolor('#161B22')
    x = np.arange(len(FEATS)); w = 0.26
    for offset, vals, lbl, col in [(-w, SA, 'Dev A (Java)', '#E63946'), (0, SB, 'Dev B (Python)', '#457B9D'),
                                   (w, SC, 'Assistant (illustratif)', '#2EC4B6')]:
        bars = ax.bar(x + offset, vals, w, label=lbl, color=col, edgecolor='#0D1117')
        for bar, v in zip(bars, vals):
            if v > 0.06:
                ax.text(bar.get_x() + bar.get_width() / 2, v + 0.003, f'{v:.2f}', ha='center',
                        fontsize=9, color=col, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(FEATS, fontsize=9, color='#C9D1D9', fontweight='bold', rotation=30, ha='right')
    ax.set_title("D'ou vous venez, et ce qui ne se fatigue jamais",
                 fontsize=16, fontweight='bold', color='white', pad=15)
    ax.legend(fontsize=12, labelcolor='white', framealpha=0.1)
    for sp in ['top', 'right']: ax.spines[sp].set_visible(False)
    for sp in ['bottom', 'left']: ax.spines[sp].set_color('#374151')
    ax.tick_params(colors='#9CA3AF'); ax.set_ylim(0, 0.85)
    ax.grid(axis='y', color='#1F2937', linewidth=0.8)
    plt.tight_layout(); plt.show()
    print(f'camelCase  : Dev A={SA[0]:.2f}  Dev B={SB[0]:.2f}  Assistant={SC[0]:.2f}')
    print(f'Type hints : Dev A={SA[3]:.2f}  Dev B={SB[3]:.2f}  Assistant={SC[3]:.2f}')
    print(f'Docstrings : Dev A={SA[4]:.2f}  Dev B={SB[4]:.2f}  Assistant={SC[4]:.2f}')


def montrer_fichier(lettre='D'):
    _ETAT['fichier'] = lettre
    print(FICHIERS[lettre])
    print('─' * 50)
    print('  Dev A ?   Dev B ?   Assistant ?')
    print('─' * 50)


def reveler():
    if 'centres' not in _ETAT:
        raise RuntimeError("Lancer d'abord la cellule empreintes(sig).")
    lettre = _ETAT.get('fichier', 'D')
    v = _ETAT['vecteur'](FICHIERS[lettre])
    dists = {nom: 1 - np.dot(v, c) for nom, c in _ETAT['centres'].items()}
    pred = min(dists, key=dists.get)
    ratio = (sorted(dists.values())[1] - dists[pred]) / max(dists[pred], 1e-9)
    conf = 'HAUTE' if ratio > 1.5 else ('MOYENNE' if ratio > 0.3 else 'FAIBLE')
    print(f'  [?]  Prédit : {pred}  ({conf} confiance)')
    _o = sorted(dists, key=dists.get)[::-1]
    fig, ax = scene(11, 2.9)
    ax.barh(range(len(_o)), [1 - min(dists[n], 1) for n in _o], height=.5,
            color=[ACCENT if n == pred else GRIS for n in _o], zorder=3)
    for y, n in enumerate(_o):
        ax.text(1 - min(dists[n], 1) + .012, y, n, color=ENCRE if n == pred else ENCRE2, fontsize=17,
                fontweight='bold' if n == pred else 'normal', va='center')
    ax.set_yticks([]); ax.set_xticks([]); ax.grid(False)
    ax.set_xlim(0, 1.3); ax.set_ylim(-.6, len(_o) - .25)
    ax.set_title(f'Proximite au profil  ·  predit : {pred}  ({conf} confiance)',
                 color='white', fontsize=17, fontweight='bold', pad=14, loc='left')
    plt.tight_layout(); plt.show()
    if lettre == 'D':
        print()
        print('─' * 50)
        print('  CE FICHIER A ÉTÉ ÉCRIT À DEUX.')
        print('─' * 50)
        ordre = sorted(dists, key=dists.get)
        print(f'  {ordre[0]} en tête, {ordre[1]} juste derrière, {ordre[2]} nulle part.')
        print()
        print('  Le modèle voit les deux mains. Il ne nomme que la machine.')
        print('  "Assistant" ne veut pas dire "pas d humain".')
