"""
real_repo_check.py
~~~~~~~~~~~~~~~~~~
Does code stylometry actually work on a real repository?

Two measurements on a cloned Git repo:

  1. Single-authorship — what fraction of files have one dominant author?
  2. Attribution accuracy — held-out attribution between the top contributors.

The ten features are re-implemented here in plain numpy rather than imported
from `stylometry-python`, so that this script runs on a bare checkout with no
installation. They are the same ten features; `stylometry-python` is the
packaged, tested version of them.

Reference point: Caliskan et al. (2015) report 94% on 1,600 authors — but on
Google Code Jam submissions, where every file has exactly one author. This
script measures what happens when that assumption does not hold.

Usage:
    git clone https://github.com/psf/requests /tmp/requests
    python experiments/real_repo_check.py /tmp/requests
"""
from __future__ import annotations

import collections
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

MIN_LINES = 40          # ignore stubs
MIN_ADDED = 3_000       # lines a contributor must have added to be included
BLOCK_SIZES = [20, 40, 80, 160, 320]
N_TRIALS = 30
TRAIN_FRACTION = 0.6

FEATURES = [
    "camelCase", "snake_case", "comments", "type_hints", "docstrings",
    "list_comp", "eq_None", "range_len", "with_open", "block_length",
]


def git(repo: Path, *args: str, timeout: int = 300) -> str:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True,
                          timeout=timeout).stdout


def signature(source: str) -> list[float]:
    """The 10 stylometric features, same definitions as the talk demo."""
    lines = source.split("\n")
    non_empty = [l for l in lines if l.strip()]
    n = max(len(non_empty), 1)
    names = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]+)\b", source)
    n_names = max(len(names), 1)
    return [
        len(re.findall(r"[a-z][A-Z]", source)) / n_names,
        len([x for x in names if "_" in x and x == x.lower() and len(x) > 2]) / n_names,
        sum(1 for l in lines if l.strip().startswith("#")) / n,
        len(re.findall(r":\s*(int|str|float|bool|list|dict|tuple|Optional|Union|Any)", source)) / n,
        len(re.findall(r'"""', source)) / n,
        len(re.findall(r"\[.+for .+in .+\]", source)) / n,
        len(re.findall(r"==\s*None|!=\s*None", source)) / n,
        len(re.findall(r"range\s*\(\s*len\s*\(", source)) / n,
        len(re.findall(r"\bwith\s+open", source)) / n,
        min(n / 60, 1.0),
    ]


def measure_single_authorship(repo: Path) -> None:
    """How often does a file have one clear author?"""
    files = git(repo, "ls-files", "*.py").split()
    shares, author_counts = [], []

    for f in files:
        blame = git(repo, "blame", "--line-porcelain", "HEAD", "--", f, timeout=60)
        authors = re.findall(r"^author (.+)$", blame, re.M)
        if len(authors) < MIN_LINES:
            continue
        counts = collections.Counter(authors)
        shares.append(counts.most_common(1)[0][1] / len(authors))
        author_counts.append(len(counts))

    if not shares:
        print("  no files large enough to measure")
        return

    shares_arr = np.array(shares)
    print(f"  Python files over {MIN_LINES} lines : {len(shares)}")
    for threshold in (0.9, 0.8, 0.7, 0.5):
        n = int((shares_arr > threshold).sum())
        print(f"    dominant author > {threshold:.0%} of lines : "
              f"{n:>3}/{len(shares)}  ({n / len(shares):.0%})")
    print(f"  authors per file        : median {int(np.median(author_counts))}, "
          f"max {max(author_counts)}")
    print(f"  main contributor's share: median {np.median(shares_arr):.0%}")


def collect_authored_lines(repo: Path, author: str) -> list[str]:
    """Lines this author ADDED, across all non-merge commits."""
    diff = git(repo, "log", "--no-merges", f"--author={author}", "-p",
               "--unified=0", "--pretty=format:", "--", "*.py")
    out = []
    for line in diff.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            body = line[1:]
            if body.strip() and not body.strip().startswith(('"""', "'''")):
                out.append(body)
    return out


def top_contributors(repo: Path) -> list[str]:
    log = git(repo, "log", "--no-merges", "--numstat",
              "--pretty=format:@%aN", "--", "*.py")
    added: dict[str, int] = collections.defaultdict(int)
    current = None
    for line in log.split("\n"):
        if line.startswith("@"):
            current = line[1:]
        else:
            parts = line.split("\t")
            if len(parts) == 3 and parts[0].isdigit() and current:
                added[current] += int(parts[0])
    return [a for a, n in sorted(added.items(), key=lambda x: -x[1]) if n >= MIN_ADDED]


def measure_attribution(repo: Path, authors: list[str]) -> None:
    """Held-out attribution accuracy between the top contributors."""
    corpora = {a: collect_authored_lines(repo, a) for a in authors}
    for a in authors:
        print(f"    {a:22s} {len(corpora[a]):>7,} lines added")

    chance = 1 / len(authors)
    print(f"\n{'lines/block':>12} {'blocks/author':>14} {'accuracy':>10}"
          f"   (chance = {chance:.0%})")
    print("-" * 54)

    rng = np.random.default_rng(0)
    for size in BLOCK_SIZES:
        blocks = {a: ["\n".join(corpora[a][i:i + size])
                      for i in range(0, len(corpora[a]) - size + 1, size)]
                  for a in authors}
        k = min(len(blocks[a]) for a in authors)
        if k < 8:
            continue

        X = {a: np.array([signature(b) for b in blocks[a][:k]]) for a in authors}
        pooled = np.vstack([X[a] for a in authors])
        mu, sd = pooled.mean(axis=0), pooled.std(axis=0)
        sd[sd == 0] = 1.0
        Z = {a: (X[a] - mu) / sd for a in authors}

        n_train = max(2, int(k * TRAIN_FRACTION))
        scores = []
        for _ in range(N_TRIALS):
            idx = {a: rng.permutation(k) for a in authors}
            centroid = {a: Z[a][idx[a][:n_train]].mean(axis=0) for a in authors}
            correct = total = 0
            for a in authors:
                for i in idx[a][n_train:]:
                    d = {b: np.abs(Z[a][i] - centroid[b]).mean() for b in authors}
                    correct += min(d, key=d.get) == a
                    total += 1
            scores.append(correct / total)
        acc = float(np.mean(scores))
        print(f"{size:>12} {k:>14,} {acc:>9.1%}   {'#' * int(acc * 30)}")
    print("-" * 54)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    repo = Path(sys.argv[1])
    if not (repo / ".git").is_dir():
        print(f"{repo} is not a git repository")
        sys.exit(1)

    print(f"Repository: {repo.name}\n")
    print("1. SINGLE AUTHORSHIP")
    measure_single_authorship(repo)

    authors = top_contributors(repo)
    print(f"\n2. ATTRIBUTION — {len(authors)} contributors over "
          f"{MIN_ADDED:,} added lines")
    if len(authors) < 2:
        print("  not enough contributors to attribute")
        return
    measure_attribution(repo, authors)

    print("\nRead this together with Caliskan et al. (2015), who report 94% on")
    print("1,600 authors — on Google Code Jam, where every file has one author.")
    print("That assumption rarely survives contact with a shared repository.")


if __name__ == "__main__":
    main()
