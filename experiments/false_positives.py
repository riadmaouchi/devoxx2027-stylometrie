#!/usr/bin/env python3
"""
false_positives.py
~~~~~~~~~~~~~~~~~~
A quelle frequence un « score Copilot » se declenche-t-il sur du code humain ?

Le score recompense les type hints, les docstrings et les identifiants en
camelCase. Ce sont des habitudes de LLM — mais aussi celles de n'importe quel
ingenieur soigneux. Ce script mesure la confusion sur du code ecrit AVANT que
Copilot existe : par construction, chaque positif y est un faux positif.

« Avant Copilot » n'est pas suppose, il est construit : le script ne lit pas
les fichiers du dossier, il lit l'etat du depot au DERNIER COMMIT AVANT une date
(par defaut le 2021-06-01 ; la preversion de Copilot est annoncee le 2021-06-29).
Sur un clone recent, le dossier contient aussi du code ecrit depuis.

Le score est reimplemente ici en numpy + stdlib, comme tout le reste du depot :
aucune installation, rien a croire sur parole, tout est relisible.

Usage :
    git clone https://github.com/psf/requests /tmp/requests      # clone COMPLET
    python3 experiments/false_positives.py /tmp/requests
    python3 experiments/false_positives.py ~/votre-depot --avant 2021-06-01
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import numpy as np

SEUIL = 0.60       # la valeur utilisee dans le talk
AVANT = "2021-06-01"   # par defaut : avant la preversion de Copilot
COPILOT = "2021-06-29" # annonce de la preversion (github.blog, 29 juin 2021)
MIN_LIGNES = 30

# Les trois signaux, avec le seuil a partir duquel ils comptent.
# Ce sont des habitudes de LLM — et c'est tout le probleme du script.
SIGNAUX = {
    "type_hints":  0.10,
    "docstrings":  0.08,
    "camel_case":  0.05,
}


def features(source: str) -> dict[str, float]:
    """Les trois signaux, calcules exactement comme dans le talk."""
    lignes = source.split("\n")
    non_vides = [l for l in lignes if l.strip()]
    n = max(len(non_vides), 1)
    noms = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]+)\b", source)
    nn = max(len(noms), 1)
    camel = [x for x in noms if re.search(r"[a-z][A-Z]", x)]
    return {
        "type_hints": len(re.findall(
            r":\s*(int|str|float|bool|list|dict|tuple|Optional|Union|Any)", source)) / n,
        "docstrings": len(re.findall(r'"""', source)) / n,
        "camel_case": len(camel) / nn,
    }


def copilot_score(source: str) -> float:
    """Score dans [0, 1]. Plus haut = plus « type et documente ».

    Ce n'est PAS un detecteur d'IA, et le talk le demontre : sur un depot
    anterieur a Copilot, il se declenche quand meme sur du code humain soigne.
    """
    f = features(source)
    score = total = 0.0
    for nom, seuil in SIGNAUX.items():
        total += 1.0
        if f[nom] >= seuil:
            score += min(f[nom] / (seuil * 2), 1.0)
    return min(score / max(total, 1.0), 1.0)


def git(depot: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(depot), *args], check=True, capture_output=True).stdout


def fichiers_au_commit(depot: Path, commit: str):
    """(nom, source) de chaque .py du depot tel qu'il etait a ce commit."""
    liste = git(depot, "ls-tree", "-r", "-z", commit).split(b"\0")
    blobs = []
    for entree in liste:
        if not entree:
            continue
        meta, chemin = entree.split(b"\t", 1)
        mode, typ, sha = meta.split()
        chemin = chemin.decode("utf-8", "replace")
        if typ != b"blob" or not chemin.endswith(".py"):
            continue
        if any(p.startswith(".") for p in chemin.split("/")):
            continue
        blobs.append((chemin, sha.decode()))
    for chemin, sha in blobs:
        yield chemin, git(depot, "cat-file", "blob", sha).decode("utf-8", "replace")


def main() -> None:
    argv = sys.argv[1:]
    avant = AVANT
    if "--avant" in argv:
        i = argv.index("--avant")
        if i + 1 >= len(argv) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", argv[i + 1]):
            sys.exit("--avant attend une date AAAA-MM-JJ")
        avant = argv[i + 1]
        del argv[i:i + 2]
    if len(argv) != 1 or argv[0].startswith("--"):
        print(__doc__)
        sys.exit(1)
    depot = Path(argv[0])

    try:
        commit = git(depot, "rev-list", "-1", f"--before={avant}", "HEAD").decode().strip()
    except subprocess.CalledProcessError:
        sys.exit(f"{depot} n'est pas un depot git.")
    if not commit:
        sys.exit(f"Aucun commit avant le {avant} : rien ne garantit que ce code est humain.\n"
                 f"Sans code anterieur a l'IA, un positif n'est pas forcement un faux positif.")
    if git(depot, "rev-parse", "--is-shallow-repository").decode().strip() == "true":
        print("ATTENTION : clone partiel (--depth). Le dernier commit avant la date peut manquer.\n")
    date = git(depot, "log", "-1", "--format=%cd", "--date=short", commit).decode().strip()

    notes = []
    for chemin, source in fichiers_au_commit(depot, commit):
        if len([l for l in source.split("\n") if l.strip()]) < MIN_LIGNES:
            continue
        notes.append((chemin.split("/")[-1], copilot_score(source)))

    if not notes:
        print("aucun fichier assez gros pour etre score")
        return

    notes.sort(key=lambda x: (-x[1], x[0]))
    print(f"Score Copilot sur du code ecrit par des humains — {depot.resolve().name}")
    print(f"etat du depot au {date} (commit {commit[:10]}), dernier commit avant le {avant}\n")
    for nom, s in notes[:12]:
        drapeau = '  <-- classe « IA »' if s >= SEUIL else ""
        print(f"  {nom:30s} {s:.2f}{drapeau}")

    v = np.array([s for _, s in notes])
    nb = int((v >= SEUIL).sum())
    print(f"\n  fichiers scores  : {len(v)}")
    print(f"  score median     : {np.median(v):.2f}")
    if avant <= COPILOT:
        print(f"  >= seuil {SEUIL:.2f}   : {nb}/{len(v)} = {nb / len(v):.0%} de faux positifs")
        print(f"\n  Ici, tout positif est faux : c'est l'etat du depot avant le {avant}.")
        print("  Le score ne detecte pas l'IA. Il detecte du code documente et des noms en camelCase.")
    else:
        print(f"  >= seuil {SEUIL:.2f}   : {nb}/{len(v)} = {nb / len(v):.0%} de fichiers classes « IA »")
        print(f"\n  ATTENTION : le {avant} est posterieur a Copilot ({COPILOT}). Ces positifs ne sont")
        print("  pas forcement faux : ce chiffre n'est PAS un taux de faux positifs.")


if __name__ == "__main__":
    main()
