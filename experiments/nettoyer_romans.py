#!/usr/bin/env python3
"""
nettoyer_romans.py — retire des quatre romans ce qui n'est pas de leur auteur.

Les extraits venaient du Projet Gutenberg avec leur preambule : note du
producteur, catalogue de l'editeur, table des matieres. Chez Verne, c'etaient
3 957 mots de licence EN ANGLAIS, soit 11 % du « corpus Verne ». C'est le piege 2
du talk — le label — dans son propre corpus : l'etiquette dit Verne, le texte
est un avocat americain.

Regle : chaque fichier commence a la premiere phrase du recit. Le script est
idempotent ; relance sur des fichiers deja propres, il ne fait rien.

Usage :  python3 experiments/nettoyer_romans.py
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUT = {
    'zola_germinal':            "Dans la plaine rase, sous la nuit sans etoiles",
    'maupassant_boule_de_suif': "Pendant plusieurs jours de suite des lambeaux d'armee",
    'flaubert_madame_bovary':   "Nous etions a l'Etude, quand le Proviseur entra",
    'verne_tour_du_monde':      "En l'annee 1872, la maison portant le numero 7",
}
mots = lambda t: len(re.findall(r'[a-zA-Z]+', t))
fr = lambda n: f'{n:,}'.replace(',', ' ')          # 36 333, pas 36,333


def main() -> int:
    for nom, marque in DEBUT.items():
        p = os.path.join(RACINE, 'corpus', nom + '.txt')
        L = open(p, encoding='utf-8').read().split('\n')
        tete, corps = [l for l in L if l.startswith('#')], '\n'.join(l for l in L if not l.startswith('#'))
        k = corps.find(marque)
        if k < 0:
            sys.exit(f'{nom} : premiere phrase introuvable — fichier modifie ?')
        retire = mots(corps[:k])
        if retire == 0:
            print(f'  {nom:26s} deja propre, {fr(mots(corps)):>6} mots')
            continue
        corps = corps[k:]
        tete = [tete[0], f'# Extrait de {fr(mots(corps))} mots, accents retires. '
                         f'Preambule de l editeur retire ({fr(retire)} mots) : experiments/nettoyer_romans.py']
        open(p, 'w', encoding='utf-8').write('\n'.join(tete) + '\n' + corps)
        print(f'  {nom:26s} {fr(retire):>5} mots retires, il en reste {fr(mots(corps)):>6}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
