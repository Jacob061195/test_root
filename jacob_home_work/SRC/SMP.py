def stable_matching(_, proposer, proposer_prefs, receiver_prefs):
    # Initialisation des variables
    free_proposers = list(proposer_prefs.keys())
    engaged = {}
    proposals = {proposer: 0 for proposer in free_proposers}

    # Création d'un dictionnaire inversé pour les préférences des receveurs
    reverse_prefs = {
        receiver: {proposer: rank for rank, proposer in enumerate(prefs)}
        for receiver, prefs in receiver_prefs.items()
    }

    while free_proposers:
        proposer = free_proposers[0]

        # Vérification que le proposant a encore des préférences à proposer
        if proposals[proposer] >= len(proposer_prefs[proposer]):
            raise ValueError(f"Invalid preference list for {proposer}, missing preferences.")

        # Sélection de la receveuse suivante dans la liste des préférences du proposant
        receiver = proposer_prefs[proposer][proposals[proposer]]
        proposals[proposer] += 1

        if receiver not in engaged:
            # Si la receveuse n'est pas engagée, on l'engage avec le proposant
            engaged[receiver] = proposer
            free_proposers.pop(0)
        else:
            # Si la receveuse est déjà engagée, on compare les préférences
            current_partner = engaged[receiver]
            if reverse_prefs[receiver][proposer] < reverse_prefs[receiver][current_partner]:
                # Si le nouveau proposant est préféré, on met à jour l'engagement
                engaged[receiver] = proposer
                free_proposers.pop(0)
                free_proposers.append(current_partner)

    # Tri des résultats selon l'ordre des proposants
    proposers_order = list(proposer_prefs.keys())
    return sorted([(proposer, receiver) for receiver, proposer in engaged.items()], key=lambda pair: proposers_order.index(pair[0]))


def main():
    import sys

    try:
        # Lire toutes les lignes d'entrée
        lines = sys.stdin.read().splitlines()
        if not lines:
            raise ValueError("Aucune entrée fournie.")

        # Initialiser l'index de ligne
        line_index = 0

        # Boucle pour traiter chaque test
        for _ in range(5):  # 5 tests
            if line_index >= len(lines):
                break  # Pas assez de données pour ce test

            # Lire N et qui propose en premier
            first_line = lines[line_index].strip().split()
            if len(first_line) != 2:
                line_index += 1
                continue  # Ignorer ce test si la première ligne est mal formatée
            n = int(first_line[0])
            proposer = first_line[1]
            if proposer not in {'m', 'w'}:
                line_index += 1
                continue  # Ignorer ce test si le genre des proposants est invalide

            line_index += 1

            # Lire les préférences des hommes
            men_prefs = {}
            for _ in range(n):
                if line_index >= len(lines):
                    break  # Pas assez de données pour ce test
                line = lines[line_index].strip().split()
                if not line or len(line) != n + 1:
                    line_index += 1
                    continue  # Ignorer cette ligne si elle est mal formatée
                man = line[0]
                prefs = line[1:]
                men_prefs[man] = prefs
                line_index += 1

            # Lire les préférences des femmes
            women_prefs = {}
            for _ in range(n):
                if line_index >= len(lines):
                    break  # Pas assez de données pour ce test
                line = lines[line_index].strip().split()
                if not line or len(line) != n + 1:
                    line_index += 1
                    continue  # Ignorer cette ligne si elle est mal formatée
                woman = line[0]
                prefs = line[1:]
                women_prefs[woman] = prefs
                line_index += 1

            # Vérifier que tous les hommes et femmes figurent dans les préférences
            all_men = set(men_prefs.keys())
            all_women = set(women_prefs.keys())

            # Ignorer ce test si des préférences sont manquantes
            if any(woman not in all_women for man, prefs in men_prefs.items() for woman in prefs):
                continue
            if any(man not in all_men for woman, prefs in women_prefs.items() for man in prefs):
                continue

            # Appeler la fonction stable_matching si les données sont valides
            if men_prefs and women_prefs:
                try:
                    if proposer == 'm':
                        result = stable_matching(n, proposer, men_prefs, women_prefs)
                    else:
                        result = stable_matching(n, proposer, women_prefs, men_prefs)
                    # Afficher les résultats sans en-tête
                    for proposer, receiver in result:
                        print(f"{proposer} {receiver}")
                except ValueError:
                    continue  # Ignorer ce test en cas d'erreur
            else:
                continue  # Ignorer ce test si les données sont manquantes ou invalides

    except Exception:
        pass  # Ignorer toute erreur inattendue


if __name__ == "__main__":
    main()