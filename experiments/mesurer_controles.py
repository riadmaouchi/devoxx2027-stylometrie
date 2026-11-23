#!/usr/bin/env python3
"""Controles : (1) le commentaire mesure sur les fichiers BRUTS,
(2) la meme analyse de tokens entre DEUX HUMAINS — est-ce que ca sort aussi
un lexique ? (3) les features syntaxiques fichier par fichier : l'IA est-elle
hors de l'intervalle humain, ou seulement au-dessus de la moyenne ?"""
import re, os
import numpy as np
from collections import Counter
import pathlib
os.chdir(pathlib.Path(__file__).resolve().parents[1])  # racine du repo

FICH = {f'Dev {i} (prod)': f'corpus/devs/dev_{i}.py' for i in (1, 2, 3)}
FICH.update({f'Humain neuf {i}': f'corpus/neuf/humain_{i}.py' for i in (1, 2, 3)})

def brut(p):
    """Tout le fichier, sauf les lignes d'en-tete que J'AI ajoutees."""
    L = open(p, encoding='utf-8').read().split('\n')
    garde = []
    for l in L:
        if l.startswith('# Lignes ajoutees') or l.startswith('# Extraites') \
           or l.startswith('# Code genere') or l.startswith('# Domaine :') \
           or l.startswith('# Ce fichier') or l.startswith('# Le meme code') \
           or l.startswith('# conserve dans') or l.startswith('# Genere par') \
           or l.startswith('# 37 fonctions') or l.startswith('# ATTENTION') \
           or l.startswith('# Les features'):
            continue
        garde.append(l)
    return '\n'.join(garde)

TXT = {k: brut(v) for k, v in FICH.items()}
TXT['IA'] = brut('corpus/ia/assistant.py')

print('='*72)
print('1. COMMENTAIRES — sur les fichiers bruts, indentation comprise')
print('='*72)
for k, t in TXT.items():
    L = [l for l in t.split('\n') if l.strip()]
    c = sum(1 for l in L if l.strip().startswith('#'))
    print(f'  {k:<18}{len(L):>6} lignes   {c:>5} commentaires   {100*c/len(L):>5.1f} %')
print()

TOK = lambda s: re.findall(r'[A-Za-z_]+|[^\sA-Za-z_]', s)

def surutilises(a, b, na, nb, seuil=40, n=10):
    ca, cb = Counter(TOK(a)), Counter(TOK(b))
    ta, tb = max(len(TOK(a)), 1), max(len(TOK(b)), 1)
    out = []
    for w in set(ca) | set(cb):
        if ca[w] + cb[w] < seuil: continue
        # lissage +1 sur les COMPTES. Un lissage a 1e-6 sur les frequences fait
        # sortir « x1547 » des qu'un mot vaut 48 contre 0 : ce chiffre ne mesure rien.
        out.append((w, ((ca[w]+1)/ta) / ((cb[w]+1)/tb), ca[w], cb[w]))
    out.sort(key=lambda x: (-x[1], x[0]))   # ex aequo : ordre alphabetique
    print(f'  ce que {na} surutilise par rapport a {nb} :')
    print('   ', '  '.join(f'{w}({r:.0f}x)' for w, r, _, _ in out[:n]))
    print(f'  ce que {na} sous-utilise :')
    print('   ', '  '.join(f'{w}({r:.2f}x)' for w, r, _, _ in out[-n:][::-1]))
    print()

print('='*72)
print('2. LA MEME ANALYSE, ENTRE DEUX HUMAINS DU MEME DEPOT')
print('='*72)
surutilises(TXT['Dev 1 (prod)'], TXT['Dev 2 (prod)'], 'Dev 1', 'Dev 2')
surutilises(TXT['Humain neuf 2'], TXT['Humain neuf 3'], 'Humain neuf 2', 'Humain neuf 3')
hum = '\n'.join(TXT[k] for k in FICH)
surutilises(TXT['IA'], hum, "l'IA", 'les 6 humains')

print('='*72)
print('3. FEATURES SYNTAXIQUES, FICHIER PAR FICHIER')
print('='*72)
def feats(t):
    L = [l for l in t.split('\n') if l.strip()]
    n = max(len(L), 1)
    nf = max(len(re.findall(r'\bdef\s', t)), 1)
    noms = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]+)\b', t)
    return {
        'lignes/fonction': n/nf,
        'ternaire /100l': 100*len(re.findall(r'=\s*[^\n=]+\bif\b[^\n]+\belse\b', t))/n,
        'comprehension /100l': 100*(len(re.findall(r'\[[^\]\n]+\bfor\b[^\]\n]+\bin\b[^\]\n]+\]', t))
                                    + len(re.findall(r'\{[^}\n]+\bfor\b[^}\n]+\bin\b[^}\n]+\}', t)))/n,
        'type hints /100l': 100*len(re.findall(r':\s*(?:int|str|float|bool|list|dict|tuple)\b', t))/n,
        'except /100l': 100*len(re.findall(r'\bexcept\b', t))/n,
        'commentaires %': 100*sum(1 for l in L if l.strip().startswith('#'))/n,
        'noms 1-2 car. %': 100*sum(1 for x in noms if len(x) <= 2)/max(len(noms), 1),
    }
F = {k: feats(t) for k, t in TXT.items()}
cols = list(F['IA'])
print(f"  {'feature':<22}" + ''.join(f'{k.split()[0][:7]:>9}' for k in FICH) + f"{'IA':>9}   {'humains min-max':>18}")
for c in cols:
    vals = [F[k][c] for k in FICH]
    ligne = f'  {c:<22}' + ''.join(f'{F[k][c]:>9.1f}' for k in FICH) + f'{F["IA"][c]:>9.1f}'
    dedans = min(vals) <= F['IA'][c] <= max(vals)
    print(ligne + f"   {min(vals):>7.1f} - {max(vals):<6.1f} {'DANS' if dedans else '>>> HORS'}")
