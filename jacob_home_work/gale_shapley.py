def gale_shapley(men_preferences, women_preferences):
    """
    Implémente l'algorithme de Gale-Shapley pour trouver un appariement stable.
    
    :param men_preferences: Dictionnaire des préférences des hommes (homme : liste des femmes)
    :param women_preferences: Dictionnaire des préférences des femmes (femme : liste des hommes)
    :return: Dictionnaire représentant l'appariement stable (homme : femme)
    """
    # Initialisation
    S = {}  # Appariement stable (homme : femme)
    free_men = list(men_preferences.keys())  # Hommes libres
    next_proposal_index = {man: 0 for man in free_men}  # Index de la prochaine proposition pour chaque homme
    current_matches = {}  # Appariements actuels (femme : homme)

    while free_men:
        m = free_men[0]  # Prendre le premier homme libre
        if next_proposal_index[m] >= len(men_preferences[m]):
            break  # L'homme a proposé à toutes les femmes

        w = men_preferences[m][next_proposal_index[m]]  # Prochaine femme sur la liste de m
        next_proposal_index[m] += 1  # Mettre à jour l'index de la prochaine proposition

        if w not in current_matches:  # Si la femme est libre
            S[m] = w
            current_matches[w] = m
            free_men.pop(0)  # L'homme n'est plus libre
        else:
            m_prime = current_matches[w]  # Partenaire actuel de w
            if women_preferences[w].index(m) < women_preferences[w].index(m_prime):  # Si w préfère m à m'
                S[m] = w
                current_matches[w] = m
                free_men.pop(0)  # L'homme n'est plus libre
                free_men.append(m_prime)  # m_prime redevient libre
            # Sinon, w rejette m

    return S


# Exemple d'utilisation
if __name__ == "__main__":
    # Préférences des hommes
    men_preferences = {
        'm1': ['w1', 'w2', 'w3'],
        'm2': ['w2', 'w1', 'w3'],
        'm3': ['w3', 'w1', 'w2']
    }

    # Préférences des femmes
    women_preferences = {
        'w1': ['m2', 'm1', 'm3'],
        'w2': ['m1', 'm2', 'm3'],
        'w3': ['m3', 'm1', 'm2']
    }

    # Appliquer l'algorithme de Gale-Shapley
    stable_matching = gale_shapley(men_preferences, women_preferences)

    # Afficher l'appariement stable
    print("Appariement stable :")
    for man, woman in stable_matching.items():
        print(f"{man} est apparié avec {woman}")