#!/usr/bin/env python3
"""
part_mots_fonction.py — quelle part d'un texte les mots-fonction occupent-ils ?

Le speech (1.2) dit qu'une grande partie de ce qu'on ecrit n'est pas choisie : ce sont
des mots-fonction. Ce script le mesure sur les quatre romans du depot, avec la liste
de 65 mots-fonction du Live 2 (FONCTIONNELS, cellule 23 du notebook).

La liste est volontairement courte : « comme », « cette », « avait »… n'y sont pas.
La part reelle est donc un peu PLUS haute que celle affichee ici.

Usage :  python3 experiments/part_mots_fonction.py
"""
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FONCTIONNELS = set(('le la les un une des de du et ou mais donc ni car que qui dans sur '
                    'avec sans pour par il elle ils elles je tu nous vous ne pas plus tres '
                    'bien tout tous rien ce se son sa ses leur a au aux en y d l s c n j m t '
                    'qu est etait sont ete avoir etre fait').split())
AUTEURS = {'Zola': 'corpus/zola_germinal.txt', 'Maupassant': 'corpus/maupassant_boule_de_suif.txt',
           'Flaubert': 'corpus/flaubert_madame_bovary.txt', 'Verne': 'corpus/verne_tour_du_monde.txt'}

tot = fn = 0
print(f'{len(FONCTIONNELS)} mots-fonction dans la liste\n')
for a, p in AUTEURS.items():
    txt = '\n'.join(l for l in open(p, encoding='utf-8').read().split('\n') if not l.startswith('#'))
    w = re.findall(r'[a-zA-Z]+', txt.lower())
    n = sum(1 for x in w if x in FONCTIONNELS)
    print(f'  {a:11s} {n / len(w) * 100:5.1f} %   ({n:,} mots sur {len(w):,})')
    tot += len(w); fn += n
print(f'\n  ensemble    {fn / tot * 100:5.1f} %')
