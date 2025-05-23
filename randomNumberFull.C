#include <iostream>
#include <vector>
#include "TRandom3.h"
#include "TH1F.h"
#include "TCanvas.h"

void randomNumberFull(int min_range = 10, int max_range = 50, int num_samples = 100) {
    // Générateur aléatoire
    TRandom3 randGen(0);

    // Stockage des nombres générés
    std::vector<int> numbers;
    numbers.reserve(num_samples);

    // Histogramme ROOT
    TH1F *histo = new TH1F("histo", "Histogramme de nombres aleatoires;Valeur;Frequence",
                           max_range - min_range + 1, min_range - 0.5, max_range + 0.5);

    // Génération + remplissage
    std::cout << "Nombres aleatoires entre " << min_range << " et " << max_range << " :\n";

    for (int i = 0; i < num_samples; ++i) {
        int value = randGen.Integer(max_range - min_range + 1) + min_range;
        numbers.push_back(value);
        histo->Fill(value);
        std::cout << value << " ";
    }

    std::cout << std::endl;

    // Affichage du graphique
    TCanvas *c1 = new TCanvas("c1", "Histogramme Aleatoire", 800, 600);
    histo->SetFillColor(kAzure + 7);
    histo->Draw();
}
