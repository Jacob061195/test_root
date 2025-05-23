#!/usr/bin/env python3
"""
Programme SMP Ultra-Optimisé - Version Finale
"""

import random
import os
import sys
import csv
import time
from pathlib import Path
from datetime import datetime

# Configuration
INPUT_DIR = "input_data"
OUTPUT_DIR = "output"
RESULTS_FILE = "results.csv"
MAX_N = 500
CHUNK_SIZE = 50  # Traitement par lots pour économiser la mémoire


def setup_dirs():
    """Initialise les répertoires de manière optimale"""
    Path(INPUT_DIR).mkdir(exist_ok=True)
    Path(OUTPUT_DIR).mkdir(exist_ok=True)


def optimized_prefs(n, seed):
    """Génération ultra-rapide des préférences"""
    random.seed(seed)
    ids = [f"m{i}" for i in range(1, n + 1)], [f"w{i}" for i in range(1, n + 1)]
    return (
        {m: random.sample(ids[1], n) for m in ids[0]},
        {w: random.sample(ids[0], n) for w in ids[1]}
    )


def process_chunk(start, end, seed_base):
    """Traitement par lots pour économiser la mémoire"""
    results = []
    for n in range(start, end + 1):
        try:
            # Génération
            men, women = optimized_prefs(n, seed_base + n)

            # Fichier input
            input_file = Path(INPUT_DIR) / f"in_{n}.txt"
            with input_file.open('w') as f:
                f.write(f"{n} m\n")
                f.writelines(f"{m} {' '.join(p)}\n" for m, p in sorted(men.items()))
                f.writelines(f"{w} {' '.join(p)}\n" for w, p in sorted(women.items()))

            # Exécution et mesure
            start_time = time.perf_counter_ns()
            matches = gale_shapley(men, women)
            exec_time = (time.perf_counter_ns() - start_time) // 1_000_000  # ms

            # Fichier output
            output_file = Path(OUTPUT_DIR) / f"out_{n}.txt"
            with output_file.open('w') as f:
                f.write(format_matches(matches, n, exec_time))

            results.append((n, input_file.name, output_file.name, exec_time))

        except Exception as e:
            print(f"Erreur n={n}: {str(e)}")
            results.append((n, input_file.name, "", 0))

    return results


def gale_shapley(men_prefs, women_prefs):
    """Algorithme GS optimisé"""
    # Implémentation directe pour éviter les appels système
    free_men = list(men_prefs.keys())
    engaged = {}
    proposals = {m: 0 for m in free_men}
    women_rank = {w: {m: i for i, m in enumerate(prefs)} for w, prefs in women_prefs.items()}

    while free_men:
        m = free_men[0]
        w = men_prefs[m][proposals[m]]
        proposals[m] += 1

        if w not in engaged:
            engaged[w] = m
            free_men.pop(0)
        else:
            current = engaged[w]
            if women_rank[w][m] < women_rank[w][current]:
                engaged[w] = m
                free_men.pop(0)
                free_men.append(current)

    return [(m, w) for w, m in engaged.items()]


def format_matches(matches, n, time_ms):
    """Formatage riche du output"""
    header = f"Résultats pour N={n} (Temps: {time_ms}ms)"
    sep = "=" * len(header)
    return f"{header}\n{sep}\n" + "\n".join(f"{m} ↔ {w}" for m, w in sorted(matches)) + "\n"


def save_stats(results):
    """Sauvegarde optimisée des stats"""
    with open(RESULTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['N', 'Fichier Entrée', 'Fichier Sortie', 'Temps (ms)'])
        writer.writerows(results)


def main():
    setup_dirs()

    # Saisie utilisateur
    while True:
        try:
            N = int(input(f"Entrez N (1-{MAX_N}): "))
            if 1 <= N <= MAX_N:
                break
            print(f"Valeur invalide. 1-{MAX_N} requis.")
        except ValueError:
            print("Entrez un nombre valide.")

    print(f"\nDébut du traitement pour N={N}...\n")

    # Traitement par lots
    all_results = []
    seed_base = int(time.time())

    for chunk_start in range(1, N + 1, CHUNK_SIZE):
        chunk_end = min(chunk_start + CHUNK_SIZE - 1, N)
        chunk_results = process_chunk(chunk_start, chunk_end, seed_base)
        all_results.extend(chunk_results)

        # Affichage progression
        progress = chunk_end / N * 100
        avg_time = sum(r[3] for r in chunk_results) / len(chunk_results) if chunk_results else 0
        print(f"\rProgression: {progress:.1f}% | Lot {chunk_start}-{chunk_end} | Temps moyen: {avg_time:.1f}ms", end='')

    # Sauvegarde finale
    save_stats(all_results)

    # Rapport
    total_time = sum(r[3] for r in all_results)
    print(f"\n\n{' STATISTIQUES FINALES ':=^50}")
    print(f"Fichiers générés: {N}")
    print(f"Temps total: {total_time / 1000:.2f}s")
    print(f"Temps moyen: {total_time / N:.1f}ms")
    print(f"\nRésultats sauvegardés dans:")
    print(f"- Inputs: {INPUT_DIR}/")
    print(f"- Outputs: {OUTPUT_DIR}/")
    print(f"- Stats: {RESULTS_FILE}")
    print("=" * 50)
if __name__ == "__main__":
    main()