# Principes fondamentaux de machine learning {#chap:fondamentaux_ml}

Ce chapitre va permettre d’avoir les bases nécessaires pour comprendre ce qu’est le machine learning, ses limites et ses applications.

## Introduction au machine learning {#introduction-au-machine-learning}

L’apprentissage automatique (machine learning) est une branche de l’intelligence artificielle qui permet à un programme d’automatiser l’apprentissage à partir d’exemples, sans être explicitement programmé pour accomplir une tâche.

Les principaux algorithmes de machine learning peuvent se diviser en 2 catégories :

- Apprentissage supervisé : le modèle est entraîné avec des données étiquetées et il doit apprendre à reconnaître les patrons pour prédire les résultats futurs. Quelques exemples :

  - Réseaux de neurones : est comme une équipe de détectives qui examinent ensemble une image pour décider si elle représente un chien, un chat ou un arbre, en se basant sur les caractéristiques qu’ils ont appris à reconnaître.

  - Régression linéaire : vise à prédire une valeur continue (par exemple, la température) en fonction de variables explicites.

  - Les arbres de décision : un algorithme qui utilise des règles pour prendre des décisions en fonction de caractéristiques des données.

- Apprentissage non supervisé : le modèle est entraîné avec des données non étiquetées et il doit apprendre à identifier les groupes ou les tendances dans les données. Quelques exemples :

  - L’agrégation (cluster) : un algorithme qui vise à grouper les données en fonction de leurs similarités.

  - Autoencodeurs : réseau de neurones qui permettent la compression (encodeur) et décompression (décodeur) de données

  - Analyse en composantes principales (PCA) : permet de réduire une grande base de données de caractéristiques par exemple de vins (degré d’alcool, la couleur, l’acidité, etc.) à seulement deux ou trois caractéristiques les plus importantes qui expliquent le plus de variabilité dans les vins, pour faciliter leur comparaison et leur classification.

La figure [6.1](#fig:A1_01_resume_machine_learning_supervise){reference-type="ref" reference="fig:A1_01_resume_machine_learning_supervise"} permet d’avoir un aperçu des phases de création d’un modèle de machine learning à partir d’un algorithme supervisé.

<figure id="fig:A1_01_resume_machine_learning_supervise" data-latex-placement="H">
<img src="../assets/figures/A1/A1_01_resume_machine_learning_supervise.webp" style="width:100.0%" />
<figcaption>Résumé du machine learning supervisé</figcaption>
</figure>

Un détail important pour la compréhension de la Figure [6.1](#fig:A1_01_resume_machine_learning_supervise){reference-type="ref" reference="fig:A1_01_resume_machine_learning_supervise"} est la différence entre modèle et algorithme :

- Un modèle est une implémentation spécifique d’un algorithme, adaptée à un jeu de données ou un problème particulier.

- Un algorithme est un ensemble d’instructions ou une procédure utilisée pour entraîner un modèle.

Une bonne manière de faire la différence est de voir l’algorithme comme la recette de cuisine et le modèle comme le gâteau. La recette (algorithme) fournit les instructions pour combiner les ingrédients, mais le gâteau (modèle) est le résultat physique de la mise en œuvre de la recette.

La Figure [6.1](#fig:A1_01_resume_machine_learning_supervise){reference-type="ref" reference="fig:A1_01_resume_machine_learning_supervise"} va servir de fil conducteur pour expliquer les principales phases :

1.  Tâche : Le machine learning n’a pas de sens s’il n’y avait pas un problème à résoudre. Par exemple classer des images de chat et chien

2.  Choix algorithme : une fois la tâche déterminée, il faut choisir l’algorithme adéquat pour résoudre le problème. Par exemple choisir un algorithme de classification d’image

3.  Sélection des données adaptées à l’algorithme : la création du modèle nécessite des données appropriées à l’algorithme utilisé. Par exemple, des images de chats ou de chiens pour un algorithme de classification d’images.

4.  Ces données sont des exemples qui serviront à entraîner le modèle à effectuer des tâches spécifiques. Si les données ne sont pas étiquetées (également appelées annotées), il sera nécessaire de le faire. Dans le cas présent, il faudra rechercher des données déjà annotées de chats et de chiens, ou bien procéder à cette annotation soi-même. Ces données annotées constituent un ensemble de données (dataset ou jeu de données).

5.  Ces données doivent être divisée en plusieurs parties :

    1.  Données d’entraînement : elles serviront à l’entraînement du modèle et représentent environ 60% du dataset.

    2.  Données de validation : lors de l’entraînement ces données servent à valider que le modèle apprend correctement et qu’il ne mémorise pas les données d’entraînement. Les données de validation représentent environ 20% du dataset

    3.  Données de test : ces données ne sont pas utilisées lors de l’entraînement et servent à vérifier les performances finales du modèle sur des données qu’il n’a jamais vues auparavant. Les données de test représentent environ 20% du dataset.

6.  Entraînement du modèle : on va appliquer l’algorithme sur les données  
    d’entraînement pour développer le modèle spécifique pour résoudre le problème de la première phase. Dans l’exemple, le modèle va apprendre les différentes caractéristiques d’un chien (museau, poil, etc.) et d’un chat.

7.  Validation des performances du modèle : le modèle est utilisé pour vérifier ses performances sur les données de validation. S’il arrive à bien classifier les chats ou les chiens, l’entraînement peut se terminer. Dans le cas où il n’arrive pas encore à bien les classifier, l’entraînement doit continuer.

8.  Test des performances du modèle : l’objectif de cette phase est d’évaluer les performances du modèle sur des données qu’il n’a jamais vues lors de l’entraînement. Les données utilisées sont les données de test. Si le modèle parvient à bien classifier les images de chats et de chiens (par exemple dans 85% des cas), le modèle est considéré comme “OK” et peut passer en production. Cependant, si les performances ne sont pas satisfaisantes (cas “KO”), il faut vérifier que les données sont adéquates, bien annotées et qu’il n’y a pas de problème de répartition entre les différentes classes. Une deuxième cause de mauvais résultats peut être le choix de variables (hyperparamètres) inadéquates pour l’entraînement.

9.  Mise en production : cette phase implique que le modèle fonctionne correctement et il peut maintenant réaliser la tâche pour laquelle il a été créé sur des données qu’il n’a jamais vues. Par exemple, classifier des images de chats et de chiens. La mise en production est complexe et souvent réalisée par des professionnels du DevOps qui ont d’excellentes connaissances des systèmes informatiques (“Ops”) ainsi que du développement informatique (“Dev”). Dans notre exemple, un site web pourrait accueillir l’interface dans laquelle l’utilisateur ou l’utilisatrice va soumettre une photo et le modèle va classifier l’image en chat ou en chien.

Le développement de modèles de machine learning supervisé est assez complexe et il se peut que cela ne fonctionne pas du premier coup (cas “KO” sur Figure [6.1](#fig:A1_01_resume_machine_learning_supervise){reference-type="ref" reference="fig:A1_01_resume_machine_learning_supervise"}). Les causes les plus habituelles sont les suivantes :

- Pas assez de données pour apprendre. Possible solution :

  - Collecter plus de données

- Équilibre des classes entre les données. Est-ce qu’une classe représente la majorité des données ? Est-ce que les chiens représentent par exemple plus de 80% du dataset ? Si les données ne sont pas équilibrées, le modèle ne va pas bien apprendre les spécificités de chaque classe. Plusieurs solutions :

  - Collecter plus de données de la ou les classe(s) moins représentée(s)

  - S’il y a suffisamment de données, c’est possible d’enlever une partie des donnes jusqu’à ce que les classes soient équilibrées

- Mauvais choix de modèle : c’est possible qu’un modèle soit trop complexe (réseau de neurones avec des milliards de paramètres) ou trop simple (régression linéaire). Possibles solutions :

  - Vérifier que l’algorithme choisi est adapté à la tâche qu’il doit réaliser, il ne doit pas être trop simple ni trop complexe

  - Si l’algorithme est complexe, c’est possible de le faire fonctionner avec plus de données mais ce n’est pas intelligent ni efficient d’un point de vue énergétique. Un gros modèle (beaucoup de paramètres) aura un entraînement plus long et va utiliser plus d’énergie lors de son utilisation

La réponse dans beaucoup de cas semble être d’acquérir plus de données. Cette démarche exige tout de même une certaine réflexion et dans certains cas ce n’est pas la meilleure :

- Coût de l’acquisition : l’acquisition de données supplémentaires peut être très coûteuse. Avoir plus de données va probablement impliquer la labellisation de celles-ci, ce qui peut engendrer des coûts non négligeables

- Rareté de la donnée : dans le domaine médical c’est difficile d’avoir plus de données sur des maladies rares par exemple

- Contraintes légales : des lois peuvent ne pas permettre l’accès à certaines données privées

- Qualité des données : la qualité de données collectées va avoir un impact sur le modèle, avoir des données de bonne qualité doit être une priorité par rapport à la quantité

### Applications {#applications}

Le machine learning a des applications très variées et il est utilisé dans de nombreux domaines tels que :

- Vision par ordinateur (“computer vision”)

  - Reconnaissance de caractères dans une image

  - Générer automatiquement une description d’une image

  - Conduite autonome d’un véhicule

  - Aide au diagnostic de maladies dans le cadre de l’imagerie médicale

- Traitement automatique du langage (“natural language processing”)

  - Reconnaissance de voix automatique et transcription de ce qui est dit

  - Traduction automatique de texte

  - Classification de texte, par exemple classifier un courriel en “spam” ou un message dans un réseau social en “language inapproprié”

  - Modèles de language tel que GPT3.5 (ChatGPT) qui permettent de saisir des questions en texte et le modèle va générer une réponse dans le même format

- Séries temporelles

  - Planification prédictive du nombre de travailleurs nécessaires pour une entreprise

  - Maintenance préventive de machines pour optimiser le nombre d’heures de fonctionnement

  - Prédiction de météo et d’événements extrêmes tel que ouragans ou tremblements de terre

  - Applications au domaine financier (ventes prévues d’une entreprise, aide à la décision dans les transactions boursières, etc.)

  - Prédiction des embouteillages et aide à la gestion du trafic routier

  - Aide à la gestion du réseau électrique en prédisant les pics de consommation

### Neurones artificiels {#neurones-artificiels}

Les réseaux de neurones sont très souvent utilisés en machine learning car ils permettent de résoudre des problèmes complexes et ils été une révolution dans le domaine.

Un réseau de neurones est un modèle mathématique inspiré de la structure et du fonctionnement du cerveau humain.

L’idée a été inspirée par le fonctionnement des neurones biologiques. C’est-à-dire que chaque neurone (voir Figure [6.2](#fig:A1_02_neurone_humaine){reference-type="ref" reference="fig:A1_02_neurone_humaine"}) reçoit des signaux d’entrée de ses dendrites et produit des signaux de sortie le long de son axone. L’axone se ramifie ensuite et se connecte via des synapses aux dendrites d’autres neurones, formant ainsi un réseau neuronal.

<figure id="fig:A1_02_neurone_humaine" data-latex-placement="H">
<img src="../assets/figures/A1/A1_02_neurone_humaine.webp" style="width:85.0%" />
<figcaption>Neurone humaine <span class="citation" data-cites="noauthor_neurone_2025">[<a href="../bibliography.html#ref-noauthor_neurone_2025" role="doc-biblioref">95</a>]</span></figcaption>
</figure>

Le premier neurone artificiel &#91;[96](../bibliography.md#ref-mcculloch_logical_1943)&#93; a été créée en 1943 par Warren Sturgis McCulloch et Walter Pitts. La Figure [6.3](#fig:A1_03_neurone_artificielle_mcculloch){reference-type="ref" reference="fig:A1_03_neurone_artificielle_mcculloch"} permet de voir les similarités avec une neurone biologique. Le neurone de McCulloch-Pitts est une unité binaire avec un seuil d’activation qui reçoit une ou plusieurs entrées, effectue un calcul et produit une sortie.

<figure id="fig:A1_03_neurone_artificielle_mcculloch">
<img src="../assets/figures/A1/A1_03_neurone_artificielle_mcculloch.webp" style="width:100.0%" />
<figcaption>Neurone artificielle proposée par McCulloch-Pitts <span class="citation" data-cites="zahn_cours_2024">[<a href="../bibliography.html#ref-zahn_cours_2024" role="doc-biblioref">97</a>]</span></figcaption>
</figure>

Le neurone est constitué des parties suivantes :

- *x*<sub>1</sub>, *x*<sub>2</sub>, sont les entrées du neurone (signal), ce sont des signaux binaire qui prennent les valeurs de 0 ou 1

- *w*<sub>1</sub>, *w*<sub>2</sub> sont les poids (“weights”) qui vont donner de l’importance au signal. Ils prennent les valeurs -1 (réduire le signal) ou +1 (augmenter le signal)

- *θ* est le seuil d’activation, c’est-à-dire la valeur minimum pour produire une sortie *y*

- *y* est la valeur de sortie du neurone, c’est une valeur binaire

- *H* est la formule d’activation

L’activation utilise la fonction de Heaviside :

<span id="eq:heaviside"></span>

$$\begin{equation}
    H(z) = 
    \begin{cases}
        0, & z &lt; 0 \\
        1, & z \geq 0
    \end{cases}
    \label{eq:heaviside}
\end{equation}$$

<p class="thesis-caption"><em>(1)</em></p>

L’utilité de ce neurone est remarquable car il permet de créer des opérateurs logiques.

<span id="eq:operateurs_logiques"></span>

$$\begin{equation}
    \begin{aligned}
        ET: \quad & y = H(x_1 + x_2 - 2) \\
        OU: \quad & y = H(x_1 + x_2 - 1) \\
        XOR: \quad & y = H(H(x_1 + x_2 - 1) + H(1 - x_1 - x_2))
    \end{aligned}
    \label{eq:operateurs_logiques}
\end{equation}$$

<p class="thesis-caption"><em>(2)</em></p>

Un exemple d’application de l’opérateur “ET” de l’Équation [&#91;eq:operateurs\_logiques&#93;](#eq:operateurs_logiques){reference-type="ref" reference="eq:operateurs_logiques"} permet de vérifier qu’il fonctionne correctement :

<span id="eq:exemple_ET"></span>

$$\begin{equation}
    \begin{aligned}
        ET \quad \quad \quad & y = H(x_1 + x_2 - 2) \\
        \begin{cases}
            x_1 = 0 \\
            x_2 = 1
        \end{cases} \quad & y = H(0 + 1 - 2) \quad y = H(-1) = 0 \\
        \begin{cases}
            x_1 = 1 \\
            x_2 = 1
        \end{cases} \quad & y = H(1 + 1 - 2) \quad y = H(0) = 1
    \end{aligned}
    \label{eq:exemple_ET}
\end{equation}$$

<p class="thesis-caption"><em>(3)</em></p>

Ce modèle a certaines limitations :

- Ses poids (*w*) et seuil (*θ*) sont fixes

- Sa sortie binaire ne permet pas de nuance, elle indique juste “vrai” (1) ou “faux” (0)

- Pas d’actualisations des poids selon les besoins

- Une seule couche ne permet pas de réaliser des calculs complexes

En 1958, Frank Rosenblatt &#91;[98](../bibliography.md#ref-rosenblatt_perceptron_1958)&#93; publie un article ou il propose le perceptron, un nouveau type de neurone artificiel.

<figure id="fig:enter-label" data-latex-placement="H">
<img src="../assets/figures/A1/A1_04_perceptron.webp" style="width:100.0%" />
<figcaption>Schéma du perceptron <span class="citation" data-cites="zahn_cours_2024">[<a href="../bibliography.html#ref-zahn_cours_2024" role="doc-biblioref">97</a>]</span>, neurone artificielle proposée par Frank Rosenblatt.</figcaption>
</figure>

Celui-ci se distingue du neurone de McCulloch-Pitts car elle permet d’utiliser des nombres réels pour les entrées, poids et biais. L’équation [&#91;eq:perceptron&#93;](#eq:perceptron){reference-type="ref" reference="eq:perceptron"} &#91;[98](../bibliography.md#ref-rosenblatt_perceptron_1958)&#93; du perceptron est la suivante:
<span id="eq:perceptron"></span>

$$\begin{equation}
    y = H\left(\sum_{k=1}^{n} w_k \cdot x_k + b\right) \quad \text{pour } x_k, w_k, b \in \mathbb{R}
    \label{eq:perceptron}
\end{equation}$$

<p class="thesis-caption"><em>(4)</em></p>

Dans l’équation [&#91;eq:perceptron&#93;](#eq:perceptron){reference-type="ref" reference="eq:perceptron"}, *H* représente la fonction d’activation de Heaviside, *w*<sub>*k*</sub> les poids, *x*<sub>*k*</sub> les entrées, *b* le biais, et *n* le nombre d’entrées.

L’évolution la plus remarquable par rapport au neurone de McCulloch-Pitts, est que le perceptron peut “apprendre” des données et actualiser les poids et biais.

On dispose d’un ensemble de données étiquetées {(**x**<sup>(*i*)</sup>, *y*<sup>(*i*)</sup>)\|*i* = 1, ...*N*}, où **x**<sup>(*i*)</sup> sont des vecteurs *n*-dimensionnels. Pour la mise à jour des poids et du biais il faut suivre les étapes suivantes :

1.  Initialiser le vecteur des poids **x**<sup>(*i*)</sup> et le biais b avec des valeurs nulles (ou des valeurs aléatoires proches de 0)

2.  Itérer en mettant à jour le vecteur de poids **w** le biais b selon les règles suivantes :

    1.  Choisir un échantillon arbitraire : (**x**<sup>(*i*)</sup>, *y*<sup>(*i*)</sup>)

    2.  Calculer la valeur prédite *ŷ*<sup>(*i*)</sup> = *H*(**w** ⋅ **x**<sup>(*i*)</sup> + *b*)

    3.  Utiliser la mise à jour des paramètres (équation [&#91;eq:perceptron\_maj1&#93;](#eq:perceptron_maj1){reference-type="ref" reference="eq:perceptron_maj1"} et [&#91;eq:perceptron\_maj2&#93;](#eq:perceptron_maj2){reference-type="ref" reference="eq:perceptron_maj2"} ci-dessous) :
        <span id="eq:perceptron_maj1"></span><span id="eq:perceptron_maj2"></span>

$$\begin{align}
                    \bm{w} &\leftarrow \bm{w} - \alpha \cdot (\hat{y}^{(i)} - y^{(i)}) \cdot \bm{x}^{(i)}
                    \label{eq:perceptron_maj1}\\
                    b &\leftarrow b - \alpha \cdot (\hat{y}^{(i)} - y^{(i)})
                    \label{eq:perceptron_maj2}
        \end{align}$$

<p class="thesis-caption"><em>(5)</em></p>

Le taux d’apprentissage *α* (“learning rate”) est un paramètre de l’algorithme, cette valeur doit être positive. Une valeur de départ tel que *α* = 0.1 semble judicieuse pour démarrer.

L’actualisation du vecteur de poids et le biais a lieu seulement si la valeur prédite et celle connues sont différentes *ŷ*<sup>(*i*)</sup> = *H*(**w** ⋅ *x*<sup>(*i*)</sup> + *b*) ≠ *y*<sup>(*i*)</sup>.

En résumé, les neurones artificielles sont des modèles mathématiques inspirés du cerveau humain. Le neurone de McCulloch-Pitts (1943) est une unité binaire avec un seuil d’activation, mais il présente des limitations. Le perceptron de Rosenblatt (1958) améliore ce modèle en utilisant des nombres réels et en permettant l’apprentissage et la mise à jour des poids et biais.

### Réseau de neurones {#réseau-de-neurones}

La combinaison de plusieurs perceptrons va créer un réseau de neurones. Cela va créer un réseau de neurones d’une seule couche où les perceptrons sont tous connectés à l’entrée (Figure [6.5](#fig:A1_05_reseau_neurones_simple){reference-type="ref" reference="fig:A1_05_reseau_neurones_simple"}).

<figure id="fig:A1_05_reseau_neurones_simple" data-latex-placement="H">
<img src="../assets/figures/A1/A1_05_reseau_neurones_simple.webp" style="width:80.0%" />
<figcaption>Réseau de neurones avec plusieurs perceptrons interconnectés <span class="citation" data-cites="zahn_cours_2024">[<a href="../bibliography.html#ref-zahn_cours_2024" role="doc-biblioref">97</a>]</span></figcaption>
</figure>

C’est aussi possible de connecter plusieurs couches de perceptron entre eux, tel qu’illustré dans la Figure [6.6](#fig:A1_06_perceptron_multicouche){reference-type="ref" reference="fig:A1_06_perceptron_multicouche"}.

<figure id="fig:A1_06_perceptron_multicouche" data-latex-placement="H">
<img src="../assets/figures/A1/A1_06_perceptron_multicouche.webp" style="width:75.0%" />
<figcaption>Perceptron multicouche <span class="citation" data-cites="zahn_cours_2024">[<a href="../bibliography.html#ref-zahn_cours_2024" role="doc-biblioref">97</a>]</span></figcaption>
</figure>

Pour améliorer les performances du perceptron, la fonction d’activation de Heaviside (Équation [&#91;eq:heaviside&#93;](#eq:heaviside){reference-type="ref" reference="eq:heaviside"}) est remplacée par la fonction d’activation de sigmoid (Equation [&#91;eq:sigmoid&#93;](#eq:sigmoid){reference-type="ref" reference="eq:sigmoid"}).

<span id="eq:sigmoid"></span>

$$\begin{equation}
\sigma(z) = \frac{1}{1 + e^{-z}}
\label{eq:sigmoid}
\end{equation}$$

<p class="thesis-caption"><em>(6)</em></p>

Cette fonction (Figure [6.7](#fig:A1_07_fonction_activation_sigmoid){reference-type="ref" reference="fig:A1_07_fonction_activation_sigmoid"}) va permettre au perceptron de retourner des valeurs entre 0 et 1, ce qui va augmenter considérablement les capacités du perceptron.

<figure id="fig:A1_07_fonction_activation_sigmoid" data-latex-placement="H">
<img src="../assets/figures/A1/A1_07_fonction_activation_sigmoid.webp" style="width:75.0%" />
<figcaption>Fonction d’activation sigmoid</figcaption>
</figure>

Le perceptron multicouche est suffisamment sophistiqué pour réaliser de la reconnaissance de caractères sur le dataset MNIST &#91;[99](../bibliography.md#ref-lecun_gradient-based_1998)&#93;.

<figure id="fig:A1_08_dataset_mnist" data-latex-placement="H">
<img src="../assets/figures/A1/A1_08_dataset_mnist.webp" style="width:75.0%" />
<figcaption>Dataset MNIST <span class="citation" data-cites="lecun_gradient-based_1998">[<a href="../bibliography.html#ref-lecun_gradient-based_1998" role="doc-biblioref">99</a>]</span></figcaption>
</figure>

Ce dataset (Figure [6.8](#fig:A1_08_dataset_mnist){reference-type="ref" reference="fig:A1_08_dataset_mnist"}) consiste en 70’000 images de chiffres écrits à la main (60k entraînement et 10k test) labellisés. Chaque image a une taille de 28x28 pixels en noir et blanc.

Ces évolutions posent la fondation pour les réseaux de neurones modernes qui sont l’état de l’art dans le domaine.

### Évaluation de la performance d’un modèle {#subsec:evaluation_performance_modele}

L’évaluation des performances d’un modèle est primordiale pour savoir si le modèle fonctionne comme il devrait. Cela est réalisé sur la base de données déjà annotées.

Le Tableau [6.1](#tab:metriques_ml){reference-type="ref" reference="tab:metriques_ml"} résume les principales métriques. L’exemple est la détection de pirates qui pourraient essayer de dévier un avion de sa trajectoire.

| **Terme** | **Définition** | **Exemple** | **Formule** |
|:---|:---|:---|:--:|
| True Positive (TP) | La classe prédite spécifiquement recherchée (positive) est identique à la classe annotée. | Le modèle a détecté un pirate. C’est un pirate. |  |
| True Negative (TN) | La classe prédite non souhaitée (négative) est identique à la classe annotée. | Le modèle a détecté qu’il ne s’agit pas d’un pirate. Ce n’est pas un pirate. |  |
| False Positive (FP) | La classe prédite spécifiquement recherchée (positive) est différente à la classe annotée. | Le modèle a détecté un pirate. Ce n’est pas un pirate. La personne n’est pas contente d’être fouillée. |  |
| False Negative (FN) | La classe prédite non souhaitée (négative) est différente à la classe annotée. | Le modèle a détecté qu’il ne s’agit pas d’un pirate. C’est un pirate. |  |
| Accuracy (ACC) | L’accuracy mesure la proportion d’images correctement classées parmi toutes les images de l’ensemble de test. |  | $\displaystyle\frac{TP + TN}{TP + TN + FP + FN}$ |
| Precision (P) | La précision mesure la proportion de vrais positifs (TP) parmi toutes les prédictions positives faites par l’algorithme. |  | $\displaystyle\frac{TP}{TP + FP}$ |
| Recall (R) | Le recall mesure la proportion de vrais positifs parmi toutes les instances positives réelles. |  | $\displaystyle\frac{TP}{TP + FN}$ |
| F1-score | Le F1-score est la moyenne harmonique de la précision (P) et du recall (R). Il fournit une mesure équilibrée de ces deux éléments. |  | $\displaystyle\frac{2 \cdot P \cdot R}{P + R}$ |

<span id="tab:metriques_ml"></span>

<p class="thesis-caption"><em>Résumé des principales métriques utilisées en machine learning pour évaluer la performance</em></p>
La matrice de confusion est un outil qui permet d’évaluer les performances d’un modèle.

<table id="tab:matrice_confusion">
<caption>Matrice de confusion</caption>
<thead>
<tr>
<th style="text-align: center;"><span>3-4</span></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>Prédiction</strong></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><span>3-5</span></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>Positif</strong></td>
<td style="text-align: center;"><strong>Négatif</strong></td>
<td style="text-align: center;"><strong>Total</strong></td>
</tr>
<tr>
<td rowspan="2" style="text-align: center;"><strong>Réalité</strong></td>
<td style="text-align: center;"><strong>Positif</strong></td>
<td style="text-align: center;"><strong>TP</strong></td>
<td style="text-align: center;">FN</td>
<td style="text-align: center;">FN + TP</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Négatif</strong></td>
<td style="text-align: center;">FP</td>
<td style="text-align: center;"><strong>TN</strong></td>
<td style="text-align: center;">FP + TN</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>Total</strong></td>
<td style="text-align: center;">TP + FP</td>
<td style="text-align: center;">FN + TN</td>
<td style="text-align: center;">N</td>
</tr>
<tr>
<td style="text-align: center;"><span>2-5</span></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>
</table>

Le Tableau [6.3](#tab:matrice_confusion_exemple){reference-type="ref" reference="tab:matrice_confusion_exemple"} illustre un exemple pratique de toutes les métriques pour la détection d’un chat (positif) sur une image.

<table id="tab:matrice_confusion_exemple">
<caption>Matrice de confusion</caption>
<thead>
<tr>
<th style="text-align: center;"><span>3-4</span></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>Prédiction</strong></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><span>3-5</span></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>Positif</strong></td>
<td style="text-align: center;"><strong>Négatif</strong></td>
<td style="text-align: center;"><strong>Total</strong></td>
</tr>
<tr>
<td rowspan="2" style="text-align: center;"><strong>Réalité</strong></td>
<td style="text-align: center;"><strong>Positif</strong></td>
<td style="text-align: center;"><strong>TP</strong>=5</td>
<td style="text-align: center;">FN=3</td>
<td style="text-align: center;">FN+TP=3+5=8</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Négatif</strong></td>
<td style="text-align: center;">FP=2</td>
<td style="text-align: center;"><strong>TN</strong>=17</td>
<td style="text-align: center;">FP+TN=2+17=19</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>Total</strong></td>
<td style="text-align: center;">TP+FP=5+2=7</td>
<td style="text-align: center;">FN+TN=3+17=20</td>
<td style="text-align: center;">N=7+20=8+19=27</td>
</tr>
<tr>
<td style="text-align: center;"><span>2-5</span></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>
</table>

<span id="eq:metriques_exemple"></span>

$$\begin{align}
    ACC &= \frac{TP + TN}{TP + TN + FP + FN} = \frac{23}{27} = 0.85 \\
    P &= \frac{TP}{TP + FP} = \frac{5}{7} = 0.71 \\
    R &= \frac{TP}{TP + FN} = \frac{5}{8} = 0.63 \\
    F1 &= \frac{2 \cdot P \cdot R}{P + R} = \frac{2 \cdot 0.71 \cdot 0.63}{0.71 + 0.63} = 0.67
    \label{eq:metriques_exemple}
\end{align}$$

<p class="thesis-caption"><em>(7)</em></p>

Dans ce cas on voit que l’accuracy est de 85%, le modèle classifie correctement (TP + TN) 85% de toutes les images (TP + TN + FP + FN).

Sa précision est de 71%, le modèle classifie correctement (TP) 71% des images de chat qu’il a détecté en tant que chat (TP + FP).

Son recall est de 63%, le modèle classifie correctement (TP) 63% des images parmi toutes les images de chat (FN + TP).

Le F1-score est de 67% ce qui indique un modèle qui n’est pas très performant. Les différentes métriques doivent être prise en compte car c’est possible qu’un modèle ait une bonne accuracy mais un recall mauvais. Le F1-score représente un bon indicateur de performance globale du modèle.

Ces métriques peuvent être appliquées à des modèles avec plusieurs classes, l’idée est que l’on compare la classe qui nous intéresse (positive) par rapport au reste qui devient la classe négative. Le Tableau [6.4](#tab:matrice_confusion_multiclasse){reference-type="ref" reference="tab:matrice_confusion_multiclasse"} représente un exemple avec 3 classes.

<table id="tab:matrice_confusion_multiclasse">
<caption>Matrice de confusion avec un exemple de plusieurs classes</caption>
<thead>
<tr>
<th style="text-align: center;"><span>3-5</span></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>Prédiction</strong></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><span>3-6</span></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>Chat</strong></td>
<td style="text-align: center;"><strong>Chien</strong></td>
<td style="text-align: center;"><strong>Lapin</strong></td>
<td style="text-align: center;"><strong>Total</strong></td>
</tr>
<tr>
<td rowspan="3" style="text-align: center;"><strong>Réalité</strong></td>
<td style="text-align: center;"><strong>Chat</strong></td>
<td style="text-align: center;">5</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">8</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Chien</strong></td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">3</td>
<td style="text-align: center;">1</td>
<td style="text-align: center;">6</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Lapin</strong></td>
<td style="text-align: center;">0</td>
<td style="text-align: center;">2</td>
<td style="text-align: center;">11</td>
<td style="text-align: center;">13</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>Total</strong></td>
<td style="text-align: center;">7</td>
<td style="text-align: center;">8</td>
<td style="text-align: center;">12</td>
<td style="text-align: center;">27</td>
</tr>
<tr>
<td style="text-align: center;"><span>2-6</span></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>
</table>

Si l’on souhaite connaître les métriques de la classe chat, on peut de manière intuitive prendre les données des chats et les considérer comme positives. Les autres classes seront quant à elles, considérées comme négatives.

<table id="tab:matrice_confusion_multiclasse_reduction">
<caption>Matrice de confusion</caption>
<thead>
<tr>
<th style="text-align: center;"><span>3-4</span></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"><strong>Prédiction</strong></th>
<th style="text-align: center;"></th>
<th style="text-align: center;"></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><span>3-5</span></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>Positif</strong></td>
<td style="text-align: center;"><strong>Négatif</strong></td>
<td style="text-align: center;"><strong>Total</strong></td>
</tr>
<tr>
<td rowspan="2" style="text-align: center;"><strong>Réalité</strong></td>
<td style="text-align: center;"><strong>Positif</strong></td>
<td style="text-align: center;"><strong>TP</strong>=5</td>
<td style="text-align: center;">FN=3</td>
<td style="text-align: center;">FN+TP=3+5=8</td>
</tr>
<tr>
<td style="text-align: center;"><strong>Négatif</strong></td>
<td style="text-align: center;">FP=2</td>
<td style="text-align: center;"><strong>TN</strong>=17</td>
<td style="text-align: center;">FP+TN=2+17=19</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"><strong>Total</strong></td>
<td style="text-align: center;">TP+FP=5+2=7</td>
<td style="text-align: center;">FN+TN=3+17=20</td>
<td style="text-align: center;">N=7+20=8+19=27</td>
</tr>
<tr>
<td style="text-align: center;"><span>2-5</span></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>
</table>

Dans le Tableau [6.5](#tab:matrice_confusion_multiclasse_reduction){reference-type="ref" reference="tab:matrice_confusion_multiclasse_reduction"} on observe que la somme des colonnes chien et lapin correspond bien à la colonne négative. Ainsi les mêmes formules qu’avant peuvent être utilisées.

## Données {#données-12}

Les données sont très importantes pour élaborer des modèles performants. Dans le contexte du machine learning, les données sont généralement stockées dans un dataset ou jeu de données contenant des exemples étiquetés. Ce chapitre va explorer les principaux types de données que l’on retrouve fréquemment en machine learning ainsi que dans le domaine de la géomatique.

Il y a une grande variété de données qui peuvent être utilisées en machine learning :

- Texte

- Images

- Audio

- Vidéo

- Données qui évoluent en fonction du temps (séries temporelles) tel que la température, cotation en bourse, etc.

Le type de données qui sont en lien avec la géomatique et qui seront traités dans ce chapitre sont :

- Images

- Orthophotos

- Nuage de points <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>

- Données vectorielles

### Images {#images}

Les images sont des données très utilisées dans la “computer vision” qui est une des disciplines du machine learning.

Un exemple de dataset d’images est le “CIFAR-10” &#91;[100](../bibliography.md#ref-krizhevsky_learning_2009)&#93;.

<figure id="fig:A1_09_cifar" data-latex-placement="H">
<img src="../assets/figures/A1/A1_09_cifar.webp" style="width:90.0%" />
<figcaption>Dataset d’images CIFAR-10 <span class="citation" data-cites="krizhevsky_cifar-10_nodate">[<a href="../bibliography.html#ref-krizhevsky_cifar-10_nodate" role="doc-biblioref">101</a>]</span></figcaption>
</figure>

Ce dataset a les caractéristiques suivantes :

- 60000 images en couleur (partagées en 50000 d’entraînement et 10000 de test)

- 10 classes

- 6000 images par classe

- Images de taille 32x32 pixels en RVB (rouge, vert, bleu)

Ce dataset est très utilisé pour apprendre à créer des réseaux de neurones simples, efficients qui arrivent à obtenir d’excellentes performances.

### Orthophotos {#subsec:annexe_ortophotos}

En géomatique, une orthophoto est un type de photographie aérienne qui offre une représentation rectifiée d’une zone géographique.

Les orthophotos sont créées en utilisant des images satellitales ou aériennes de haute résolution, souvent acquises par des systèmes tels que les caméras embarquées sur des avions ou des drones. Pour obtenir une orthophoto de qualité, il est nécessaire de suivre un processus complexe comprenant plusieurs étapes :

- Acquisition des images : Les images sont prises à partir d’un appareil photo aérien ou satellitaire, généralement à partir d’une altitude élevée.

- Rectification géométrique : Les images sont rectifiées pour corriger les distorsions liées à la perspective et aux mouvements de l’appareil photo pendant la prise de vue.

- Mosaïque des images : Les images sont assemblées (mises en mosaïque) pour former une image unique et continue, qui couvre la zone géographique souhaitée.

- Correction de la topographie : La surface du terrain est corrigée pour prendre en compte les élévations et les dénivellations, ce qui permet d’obtenir une représentation tridimensionnelle exacte.

- Traitement des données : Les images sont traitées pour éliminer les bruits, les artefacts et les imperfections, ce qui améliore la qualité de l’image finale.

Il existe 3 types différents d’orthophotos &#91;[102](../bibliography.md#ref-barrette_different_2022)&#93; :

- Orthophoto dynamique

- Orthomosaïque

- “True orthophoto”

#### Orthophoto dynamique {#orthophoto-dynamique}

Les orthophotos dynamiques sont générés de manière dynamique à partir d’images sources, en utilisant un modèle numérique de terrain comme référence.

<figure id="fig:A1_10_ortophoto_dynamique1" data-latex-placement="H">
<img src="../assets/figures/A1/A1_10_ortophoto_dynamique1.webp" style="width:100.0%" />
<figcaption>Exemple d’orthophoto dynamique <span class="citation" data-cites="barrette_different_2022">[<a href="../bibliography.html#ref-barrette_different_2022" role="doc-biblioref">102</a>]</span></figcaption>
</figure>

<figure id="fig:A1_11_orthophoto_dynamique2" data-latex-placement="H">
<img src="../assets/figures/A1/A1_11_orthophoto_dynamique2.webp" style="width:100.0%" />
<figcaption>Deuxième exemple d’orthophoto dynamique <span class="citation" data-cites="barrette_different_2022">[<a href="../bibliography.html#ref-barrette_different_2022" role="doc-biblioref">102</a>]</span></figcaption>
</figure>

Les avantages sont :

- Génération rapide des orthophotos

- Permet de visualiser une zone avec plusieurs perspectives différentes

Le principal inconvénient est que les objets non-terrain (bâtiments par exemple), peuvent apparaître inclinés (voir Figures [6.10](#fig:A1_10_ortophoto_dynamique1){reference-type="ref" reference="fig:A1_10_ortophoto_dynamique1"} et [6.11](#fig:A1_11_orthophoto_dynamique2){reference-type="ref" reference="fig:A1_11_orthophoto_dynamique2"}). Les caractéristiques aériennes peuvent sembler se déplacer lorsque l’image est déplacée en raison de la visualisation des objets depuis différentes directions.

#### Orthomosaïque {#orthomosaïque}

Les orthomosaïques sont créés en fusionnant plusieurs images en une seule image cohérente. La Figure [6.12](#fig:A1_12_orthomosaique){reference-type="ref" reference="fig:A1_12_orthomosaique"} de la page suivante représente un exemple d’orthomosaïque.

Les principaux avantages des orthomosaïques sont :

- Image plus compacte, ce qui permet un affichage plus rapide

- Génération rapide, en particulier si un modèle numérique de terrain est disponible

- Peuvent être créés à partir d’images avec moins de recouvrement, ce qui peut réduire les exigences de capture de données

Les principaux inconvénients des orthomosaïques sont :

- Pas précis pour les objets hors sol qui peuvent sembler inclinés loin de la caméra.

- Peuvent avoir des artefacts visuels causés par les angles de caméra.

- Les lignes de séparation utilisées lors de la génération de l’image peuvent être visibles (voir Figure [6.13](#fig:A1_13_orthomosaique_lignes){reference-type="ref" reference="fig:A1_13_orthomosaique_lignes"} de la page suivante)

<figure id="fig:A1_12_orthomosaique" data-latex-placement="H">
<img src="../assets/figures/A1/A1_12_orthomosaique.webp" style="width:100.0%" />
<figcaption>Exemple d’orthomosaïque <span class="citation" data-cites="barrette_different_2022">[<a href="../bibliography.html#ref-barrette_different_2022" role="doc-biblioref">102</a>]</span></figcaption>
</figure>

<figure id="fig:A1_13_orthomosaique_lignes" data-latex-placement="H">
<img src="../assets/figures/A1/A1_13_orthomosaique_lignes.webp" style="width:100.0%" />
<figcaption>Exemple d’orthomosaïque avec lignes de séparation <span class="citation" data-cites="barrette_different_2022">[<a href="../bibliography.html#ref-barrette_different_2022" role="doc-biblioref">102</a>]</span></figcaption>
</figure>

#### “True orthophoto” {#true-orthophoto}

Les true orthophotos sont créés en utilisant un modèle numérique de surface très détaillé pour générer une orthophoto de sortie précise pour tous les pixels (Figure [6.14](#fig:A1_14_true_orthophoto){reference-type="ref" reference="fig:A1_14_true_orthophoto"}).

<figure id="fig:A1_14_true_orthophoto" data-latex-placement="H">
<img src="../assets/figures/A1/A1_14_true_orthophoto.webp" style="width:100.0%" />
<figcaption>Exemple de true orthophoto <span class="citation" data-cites="barrette_different_2022">[<a href="../bibliography.html#ref-barrette_different_2022" role="doc-biblioref">102</a>]</span></figcaption>
</figure>

Les avantages des true orthophotos sont les suivants :

- Fournissent des images cohérentes de haute qualité qui sont idéales pour la digitalisation de la localisation et de la taille des empreintes de bâtiment.

- Peuvent être générés de manière entièrement automatique, sans nécessiter de lignes de soudure ou de lignes de rupture manuelles.

- Peuvent éliminer automatiquement les objets en mouvement, les reflets ou les couleurs incohérentes.

- Peuvent améliorer la radiométrie et la résolution en utilisant la redondance de plusieurs images.

- Sont idéaux pour la détection de changement, car les images sont cohérentes d’une année à une autre.

Les principaux inconvénients des true orthophotos sont :

- Plus coûteux en termes de calcul.

- Nécessitent un recouvrement suffisant entre les images pour extraire un modèle numérique de surface détaillé.

Dans le cadre du machine learning, le type d’orthophoto la plus intéressante est la true orthophoto.

Le Tableau [6.6](#tab:comparatif_orthophotos){reference-type="ref" reference="tab:comparatif_orthophotos"} ci-dessous synthétise les avantages et inconvénients de chacun des types d’orthophotos.

| **Type d’orthophoto** | **Génération** | **Précision objets hors sol** | **Données** | **Espace de stockage** | **Complexité de traitement** |
|:---|:---|:---|:---|:---|:---|
| Orthophoto dynamique | Généré en temps réel, moins précis pour les objets non-terrain. | \+ | \+ | \+ | \+ |
| Orthomosaïque | Créé en fusionnant plusieurs images ortho | ++ | ++ | ++ | ++ |
| True orthophoto | Créé en utilisant un modèle numérique de surface très détaillé | +++ | +++ | +++ | +++ |

<span id="tab:comparatif_orthophotos"></span>

<p class="thesis-caption"><em>Comparatif des 3 types d’orthophotos</em></p>
#### Fournisseurs d’orthophotos {#fournisseurs-dorthophotos}

Au niveau mondial, il y a plusieurs fournisseurs d’orthophotos &#91;[103](../bibliography.md#ref-stdl_recherche_2024)&#93;, voici quelques exemples :

| 2-4 | **Sentinel-2** | **Pléiades Neo** | **WorldView Legion** |
|:---|:---|:---|:---|
| Entreprise/entité | Agence spatiale européenne | Airbus | Maxar |
| Prix | Gratuit | Payant | Payant |
| Fréquence de renouvellement | 5 jours | Plusieurs fois par jour | Jusqu’à 15x par jour |
| Résolution | 10m/pixel (RGB/IR) | 30cm/pixel (RGB) 1.2m/pixel (IR) | 30cm/pixel (RGB) 1.2m/pixel (IR) |
| Couleur/infrarouge | RGB/IR | RGB/IR | RGB/IR |

<span id="tab:fournisseurs_orthophotos"></span>

<p class="thesis-caption"><em>Comparatif de 3 fournisseurs d’orthophoto mondiaux</em></p>
En ce qui concerne la Suisse, Swisstopo &#91;[104](../bibliography.md#ref-swisstopo_swissimage_nodate)&#93; met librement à disposition des orthophotos de tout le pays. Les détails techniques sont les suivants :

- Systèmes de coordonnées : CH1903+/MN95 (EPSG:2056)

- Résolution au sol : 0.1 m ou 0.25 m selon la région

- Écart type pour la précision de la position : +/- 0.15 m pour la résolution au sol de 0.1 m.

- Spécifications pour le téléchargement gratuit :

  - Format: Cloud Optimized Geotiff (COG), RGB (3 x 8 bit), compression JPEG 95.

  - Découpage : ∼ 42 700 tuiles de 1 km sur 1 km.

  - Résolutions disponibles et taille des fichiers

    - 0.1m : ∼ 55 Mo / tuile, 2.4 To / une couverture complète

    - 2m : ∼ 2.8 Mo / tuile, 120 Go / une couverture complète

Selon les zones géographiques, les orthophotos ont été réalisées entre 2019 et 2023. La fréquence d’actualisation est de 3 ans.

Swisstopo dispose d’autres produits tel que :

- Orthophotos “RGB” avec Infrarouge (4 canaux)

- Orthophotos historiques

Dans le Canton de Genève, <a href="../glossary.html#gloss-sitg"><span data-acronym-label="sitg" data-acronym-form="singular+abbrv">sitg</span></a> &#91;[105](../bibliography.md#ref-sitg_chiffre-cle_2025)&#93; dispose d’une grande quantité de données. En ce qui concerne les orthophotos du Canton de Genève disponibles librement :

- Orthophotos historiques (1932-2021)

- Orthophoto avec infrarouge (2021)

- Orthophotos réalisées par Swisstopo (2023)

  - Résolution de 10 cm par pixel

- Orthophoto haute résolution (2019)

  - Résolution de 5 cm par pixel

  - True orthophotos

### Nuage de points <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> {#nuage-de-points-lidar}

Laser Imaging Detection And Ranging (<a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>) &#91;[106](../bibliography.md#ref-esri_quoi_2025)&#93; est une technique de télédétection optique qui utilise la lumière laser pour échantillonner la surface de la Terre et produire des mesures “x, y, z” d’une grande précision.

Les données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> sont principalement utilisées dans des applications de cartographie laser aéroportées et commencent à s’imposer en tant qu’alternative rentable face aux techniques d’arpentage traditionnelles, telles que la photogrammétrie.

Les données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> produisent des jeux de données de nuages de points cotés qui peuvent être gérés, visualisés, analysés à l’aide d’outils GIS (Qgis, ArcGIS, etc.).

La Figure [6.15](#fig:A1_15_lidar_exemple){reference-type="ref" reference="fig:A1_15_lidar_exemple"} représente des objets d’exemple et la Figure [6.16](#fig:A1_16_lidar_exemple2){reference-type="ref" reference="fig:A1_16_lidar_exemple2"} permet de voir comment ces objets sont vus par le <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>

<figure id="fig:A1_15_lidar_exemple" data-latex-placement="H">
<img src="../assets/figures/A1/A1_15_lidar_exemple1.webp" style="width:100.0%" />
<figcaption>Objets pour le nuage de points LIDAR <span class="citation" data-cites="cadden_lidar_2021">[<a href="../bibliography.html#ref-cadden_lidar_2021" role="doc-biblioref">107</a>]</span></figcaption>
</figure>

<figure id="fig:A1_16_lidar_exemple2" data-latex-placement="H">
<img src="../assets/figures/A1/A1_16_lidar_exemple2.webp" style="width:100.0%" />
<figcaption>Nuage de points LIDAR sur des objets <span class="citation" data-cites="cadden_lidar_2021">[<a href="../bibliography.html#ref-cadden_lidar_2021" role="doc-biblioref">107</a>]</span></figcaption>
</figure>

#### Composants matériels d’un système <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> {#composants-matériels-dun-système-lidar}

Les composants matériels principaux d’un système <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> incluent un véhicule de collecte (avion, hélicoptère, véhicule et trépied), un système de scanner laser, un système de positionnement par satellite (GPS) et un système de navigation à inertie (INS). Un système INS mesure le roulis, le tangage et la direction du système <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>.

#### Le capteur <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> {#le-capteur-lidar}

Le <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> est un capteur optique actif qui transmet des faisceaux laser vers une cible tout en parcourant des itinéraires d’étude spécifiques. La réflexion du laser à partir de la cible est détectée et analysée par des récepteurs dans le capteur <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>.

Ces récepteurs enregistrent la période précise qui s’écoule entre le moment où l’impulsion laser quitte le système et celui où elle est renvoyée pour calculer la distance entre le capteur et la cible.

Alliées aux informations de positionnement (GPS et INS), ces mesures de distance sont transformées en mesures de points tridimensionnels réels de la cible réflectrice dans l’espace objet.

#### Post-traitement des données ponctuelles {#post-traitement-des-données-ponctuelles}

Les données ponctuelles sont post-traitées après l’étude de la collecte des données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> en coordonnées x, y, z très précises en analysant la plage de temps du laser, l’angle de balayage laser, la position GPS et les informations INS.

#### Retours <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> {#retours-lidar}

Les impulsions laser émises par un système <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> se reflètent sur des objets placés à la fois sur la surface du sol et au-dessus : végétation, bâtiments, ponts et ainsi de suite. Une impulsion laser émise peut revenir au capteur <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> sous forme d’un ou plusieurs retours. Les impulsions laser émises qui rencontrent plusieurs surfaces de réflexion lors de leur voyage vers le sol sont fractionnées en autant de retours qu’il existe de surfaces réfléchissantes.

#### Attributs de point <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> {#attributs-de-point-lidar}

Des informations complémentaires sont stockées avec chaque valeur de position x, y et z. Les attributs de point <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> suivants sont conservés pour chaque impulsion laser enregistrée : intensité, numéro de retour, nombre de retours, valeurs de classification des points, points situés à la limite de la ligne de vol, valeurs RVB (rouge, vert et bleu), heure GPS, angle de balayage et direction du balayage.

#### Données de nuages de points {#données-de-nuages-de-points}

Les données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> spatiales post-traitées sont connues comme des données de nuages de points. Les nuages de points initiaux sont des ensembles volumineux de points d’altitude 3D qui incluent des valeurs x, y et z, ainsi que des attributs supplémentaires, tels que des horodatages GPS. Les entités de surface spécifiques que le laser rencontre sont classées après le post-traitement du nuage de points <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> initial. Les altitudes du sol, des bâtiments, du couvert forestier, des ponts au-dessus des autoroutes et de tout ce que le faisceau laser peut rencontrer au cours de l’étude constituent des données de nuages de points.

La rugosité et l’intensité sont deux informations différentes mais complémentaires fournies par les nuages de points <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>.

La rugosité mesure la variation locale de l’altitude des points dans un voisinage donné. Elle est calculée à partir des coordonnées 3D (X, Y, Z) des points et reflète la texture et l’irrégularité de la surface. Une rugosité élevée indique la présence d’obstacles ou de variations d’altitude. Cette mesure est indépendante des propriétés de réflectance des matériaux et est utilisée pour distinguer les surfaces planes des surfaces encombrées.

L’intensité, quant à elle, mesure la quantité d’énergie réfléchie par la surface et enregistrée par le capteur <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>. C’est une valeur scalaire associée à chaque point, en plus des coordonnées 3D. L’intensité dépend des propriétés de réflectance des matériaux à la longueur d’onde du laser. Elle varie selon le type de surface : elle est forte pour les surfaces réfléchissantes et faible pour les surfaces absorbantes. L’intensité peut aider à distinguer différents matériaux ou objets, mais elle est sensible aux conditions d’acquisition, telles que la distance et l’angle d’incidence.

#### Fournisseur de données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> {#fournisseur-de-données-lidar}

Au niveau mondial, il n’y a pas de données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> disponibles qui couvrent le globe entier. C’est probablement dû à des raisons de coût.

En ce qui concerne la Suisse, Swisstopo &#91;[108](../bibliography.md#ref-swisstopo_acquisition_2024)&#93; met à disposition des données qui couvrent l’intégralité du territoire. Dans la Figure [6.17](#fig:A1_17_swisstopo_lidar){reference-type="ref" reference="fig:A1_17_swisstopo_lidar"}, on peut voir les 6 campagnes d’acquisition de données qui ont été menées. Les données sont disponibles en moyenne environ 12 mois après le survol.

<figure id="fig:A1_17_swisstopo_lidar" data-latex-placement="H">
<img src="../assets/figures/A1/A1_17_swisstopo_lidar.webp" style="width:100.0%" />
<figcaption>Données LIDAR disponibles en Suisse <span class="citation" data-cites="swisstopo_acquisition_2024">[<a href="../bibliography.html#ref-swisstopo_acquisition_2024" role="doc-biblioref">108</a>]</span></figcaption>
</figure>

Les caractéristiques des données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> disponibles sont les suivantes :

- Densité de points : minimum 5 pts/m², moyenne autour de 15-20 pts/m²

- Classification :

  - Non classifiés

  - Sol

  - Végétation

  - Bâtiments

  - Eau

  - Ponts

- Précision planimétrique : 20 cm

- Précision altimétrique : 10 cm

Swisstopo va continuer à mettre à jour ses données dans les années suivantes (Figure [6.18](#fig:A1_18_swisstopo_prevision_lidar){reference-type="ref" reference="fig:A1_18_swisstopo_prevision_lidar"}). La prévision est que la mise à jour de ces données sera finalisée en 2030.

<figure id="fig:A1_18_swisstopo_prevision_lidar" data-latex-placement="H">
<img src="../assets/figures/A1/A1_18_swisstopo_prevision_lidar.webp" style="width:100.0%" />
<figcaption>Prévision d’acquisition de données LIDAR en Suisse <span class="citation" data-cites="swisstopo_acquisition_2024">[<a href="../bibliography.html#ref-swisstopo_acquisition_2024" role="doc-biblioref">108</a>]</span></figcaption>
</figure>

En ce qui concerne le canton de Genève, les dernières données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> &#91;[109](../bibliography.md#ref-sitg_nuages_2021)&#93; &#91;[110](../bibliography.md#ref-sitg_nuages_2023)&#93; disponibles sont:

<table id="tab:lidar_geneve_compact">
<caption>Données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> disponibles dans le canton de Genève</caption>
<thead>
<tr>
<th style="text-align: left;"><span>2-3</span></th>
<th style="text-align: left;"><strong>2021</strong></th>
<th style="text-align: left;"><strong>2023</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">Densité de points</td>
<td style="text-align: left;">175-220 pts/m²</td>
<td style="text-align: left;">100 pts/m²</td>
</tr>
<tr>
<td style="text-align: left;">Classification</td>
<td style="text-align: left;"><ul>
<li><p>Non classifié</p></li>
<li><p>Sol</p></li>
<li><p>Basse végétation (&lt;50cm)</p></li>
<li><p>Haute végétation (&gt;50cm)</p></li>
<li><p>Bâtiments</p></li>
<li><p>Points bas ou isolés</p></li>
<li><p>Eau</p></li>
<li><p>Ponts, passerelles</p></li>
<li><p>Sol (points complémentaires)</p></li>
<li><p>Bruit</p></li>
<li><p>Points mesurés hors périmètre</p></li>
</ul></td>
<td style="text-align: left;"><ul>
<li><p>Non classifié</p></li>
<li><p>Sol</p></li>
<li><p>Basse végétation (&lt;50cm)</p></li>
<li><p>Moyenne végétation (0.5-3m)</p></li>
<li><p>Haute végétation (&gt;3m)</p></li>
<li><p>Bâtiments</p></li>
<li><p>Points bas ou isolés/erreurs</p></li>
<li><p>Eau</p></li>
<li><p>Piles de matériel naturelle</p></li>
<li><p>Ponts, passerelles</p></li>
<li><p>Câbles</p></li>
<li><p>Mâts, antennes</p></li>
<li><p>Ponts, passerelles</p></li>
<li><p>Bruit</p></li>
<li><p>Voitures</p></li>
<li><p>Façades</p></li>
<li><p>Grues, objets temporaires</p></li>
<li><p>Objets sur les toits</p></li>
<li><p>Murs</p></li>
<li><p>Points de sol additionnels</p></li>
</ul></td>
</tr>
<tr>
<td style="text-align: left;">Précision planimétrique</td>
<td style="text-align: left;">8 cm</td>
<td style="text-align: left;">20 cm</td>
</tr>
<tr>
<td style="text-align: left;">Précision altimétrique</td>
<td style="text-align: left;">4 cm</td>
<td style="text-align: left;">10 cm</td>
</tr>
</tbody>
</table>

<figure id="fig:A1_19_geneve_lidar" data-latex-placement="H">
<img src="../assets/figures/A1/A1_19_geneve_lidar.webp" style="width:75.0%" />
<figcaption>Représentation à partir des données LIDAR d’une partie du canton de Genève <span class="citation" data-cites="sitg_nuages_2023">[<a href="../bibliography.html#ref-sitg_nuages_2023" role="doc-biblioref">110</a>]</span></figcaption>
</figure>

La représentation ci-dessus (Figure [6.19](#fig:A1_19_geneve_lidar){reference-type="ref" reference="fig:A1_19_geneve_lidar"}) permet d’avoir une idée à quoi ressemble le nuage de points <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>.

### Données vectorielles {#subsec:annexe_donnees_vectorielles}

Les données vectorielles sont un moyen de représenter des informations géométriques à l’aide de valeurs numériques. Contrairement aux données matricielles, qui représentent les informations sous la forme d’une grille de valeurs de pixels, les données vectorielles utilisent des points, des lignes et des polygones pour définir les formes et les limites. Chaque point, ligne ou polygone est représenté par un ensemble de coordonnées (x, y et parfois z) qui définissent son emplacement dans l’espace.

Il existe plusieurs types de données vectorielles :

- Les points : Représentés par un seul jeu de coordonnées (x, y, z), les points sont souvent utilisés pour représenter des emplacements spécifiques, tels que des adresses ou des points de repère.

- Les lignes : Représentées par une série de points connectés, les lignes sont souvent utilisées pour représenter des frontières, des routes ou d’autres caractéristiques linéaires.

- Polygones : Représentés par une série de points connectés qui forment une forme fermée, les polygones sont souvent utilisés pour représenter des zones, telles que des bâtiments, des parcelles ou des limites de zonage.

Les données vectorielles sont largement utilisées en géomatique pour diverses applications, notamment :

- SIG : Les données vectorielles sont utilisées pour créer, éditer et analyser des données géospatiales dans les logiciels SIG.

- Analyse spatiale : Les données vectorielles sont utilisées pour effectuer des analyses spatiales, telles que le calcul de distances, de zones tampons et d’intersections.

- Cartographie : Les données vectorielles sont utilisées pour créer des cartes et visualiser des données géospatiales.

- L’urbanisme : Les données vectorielles sont utilisées pour planifier et concevoir des infrastructures urbaines, telles que des routes, des bâtiments et des parcs.

<figure id="fig:A1_20_donnees_vectorielles_exemple" data-latex-placement="H">
<img src="../assets/figures/A1/A1_20_donnees_vectorielles_exemple.webp" style="width:100.0%" />
<figcaption>Exemple de données vectorielles de <a href="../glossary.html#gloss-sitg"><span data-acronym-label="sitg" data-acronym-form="singular+abbrv">sitg</span></a>. Rue de la Prairie 8 à Genève</figcaption>
</figure>

La Figure [6.20](#fig:A1_20_donnees_vectorielles_exemple){reference-type="ref" reference="fig:A1_20_donnees_vectorielles_exemple"} montre un exemple de données vectorielles extraites de <a href="../glossary.html#gloss-sitg"><span data-acronym-label="sitg" data-acronym-form="singular+abbrv">sitg</span></a>, le portail de géodonnées du canton de Genève. En plus des points, lignes et polygones il est possible d’associer des données en forme de tableau (Figure [6.21](#fig:A1_21_donnees_vectorielles_tableau){reference-type="ref" reference="fig:A1_21_donnees_vectorielles_tableau"}).

<figure id="fig:A1_21_donnees_vectorielles_tableau" data-latex-placement="H">
<img src="../assets/figures/A1/A1_21_donnees_vectorielles_tableau.webp" style="width:75.0%" />
<figcaption>Exemple de données tabulaires associées a un polygone. Rue de la Prairie 8 à Genève. Données de <a href="../glossary.html#gloss-sitg"><span data-acronym-label="sitg" data-acronym-form="singular+abbrv">sitg</span></a></figcaption>
</figure>

Les données sont organisées en couches vectorielles. Dans ces deux figures d’exemple, la couche des bâtiments hors sol est représentée. Chaque couche regroupe en général une thématique comme les bâtiments, les arbres, etc.

Il existe une très grande quantité de données vectorielles tant au niveau Suisse et genevois.

<a href="../glossary.html#gloss-sitg"><span data-acronym-label="sitg" data-acronym-form="singular+abbrv">sitg</span></a> dispose de plus de 1575 couches de données &#91;[105](../bibliography.md#ref-sitg_chiffre-cle_2025)&#93;, dont environ 200 couches raster et plus de 1375 couches vectorielles, ce qui représente une très grande quantité de données.

Les données de l’administration publique suisse sont regroupées sur un site web[^1] pour simplifier l’accès à ces données publiques. Le site compte plus de 10000 couches (vectorielles, raster, etc.) qui sont produites par les communes, cantons, confédération et autres entités publiques. Les thématiques traitées sont très diverses par exemple, l’environnement, l’économie, la santé, etc.

Swisstopo met à disposition du publique un site[^2] pour visualiser toutes les données disponibles dans une interface conviviale.

## Machine learning appliqué aux images {#machine-learning-appliqué-aux-images-1}

L’analyse d’images est un domaine important du machine learning, qui permet aux machines d’analyser, de comprendre et de déduire des informations à partir d’images. La Figure [6.22](#fig:A1_22_schema_ml){reference-type="ref" reference="fig:A1_22_schema_ml"} ci-dessous illustre les principales applications.

<figure id="fig:A1_22_schema_ml" data-latex-placement="H">
<img src="../assets/figures/A1/A1_22_schema_ml.webp" style="width:100.0%" />
<figcaption>Exemple de classification, détection, segmentation, suivi et analyse de pose <span class="citation" data-cites="ultralytics_classer_nodate">[<a href="../bibliography.html#ref-ultralytics_classer_nodate" role="doc-biblioref">111</a>]</span></figcaption>
</figure>

Les principales applications sont :

- Classification d’images

- Détection d’objets

- Segmentation d’images

Il existe d’autres applications tel que le suivi (compter des objets dans une vidéo) et l’estimation de pose (évaluer la position du corps), mais ils ne seront pas traités dans ce rapport car leur application à la géomatique est très limitée.

La Figure [6.23](#fig:A1_23_image_exemple){reference-type="ref" reference="fig:A1_23_image_exemple"} ci-dessous va permettre d’illustrer les différentes applications.

<figure id="fig:A1_23_image_exemple" data-latex-placement="H">
<img src="../assets/figures/A1/A1_23_image_exemple.webp" style="width:100.0%" />
<figcaption>Orthophoto de la haute école du paysage, d’ingénierie et architecture de Genève (hepia), situé à la rue de la Prairie 4</figcaption>
</figure>

### Classification d’images {#classification-dimages}

Cette tâche consiste à classer une image dans l’une des catégories prédéfinies. Par exemple, classer une image en fonction de son contenu (par exemple, chat, chien, voiture, etc.). Les modèles utilisés pour la classification d’images sont généralement entraînés sur des données étiquetées où chaque image est associée à une seule catégorie.

Dans la Figure [6.23](#fig:A1_23_image_exemple){reference-type="ref" reference="fig:A1_23_image_exemple"} d’exemple, la classification va identifier dans l’image les deux classes soit “rooftop” et “solar-panel”. L’image en soi n’aura pas d’annotation particulière, car la classification identifie ce qu’il y a sur l’image mais pas la position exacte. Le modèle va retourner les classes et la probabilité qu’estime le modèle que la classe soit présente. La classe sélectionnée sera celle qui a la probabilité la plus élevée.

La Figure [6.24](#fig:A1_24_classification){reference-type="ref" reference="fig:A1_24_classification"} représente un deuxième exemple de classification d’images.

<figure id="fig:A1_24_classification" data-latex-placement="H">
<img src="../assets/figures/A1/A1_24_classification.webp" style="width:100.0%" />
<figcaption>Exemple de classification d’image <span class="citation" data-cites="ultralytics_classer_nodate">[<a href="../bibliography.html#ref-ultralytics_classer_nodate" role="doc-biblioref">111</a>]</span></figcaption>
</figure>

### Détection d’objets {#détection-dobjets}

La détection va identifier les différentes classes sur l’image, ainsi que leur position. Les modèles utilisés pour la détection d’objets sont généralement entraînés sur des données étiquetées où chaque objet est associé à une boîte englobante et une étiquette de classe.

<figure id="fig:A1_25_detection_hepia" data-latex-placement="H">
<img src="../assets/figures/A1/A1_25_detection_hepia.webp" style="width:100.0%" />
<figcaption>Orthophoto d’exemple de détection</figcaption>
</figure>

Dans la Figure [6.25](#fig:A1_25_detection_hepia){reference-type="ref" reference="fig:A1_25_detection_hepia"} on observe que la détection permet de savoir quelle classe est présente sur l’image, sa position mais pas le contour exact de l’objet. Le chiffre indiqué après la classe indique la probabilité estimée par le modèle que l’objet détecté appartienne à une certaine classe.

### Segmentation d’image {#subsec:segmentation_image}

Il y a principalement 3 types de segmentation d’image qui sont couramment utilisés :

- Segmentation sémantique

- Segmentation instance

- Segmentation panoptique

<figure id="fig:types_segmentation" data-latex-placement="H">
<figure id="fig:A1_26_segmentation_image_exemple">
<img src="../assets/figures/A1/A1_26_segmentation_image_exemple.webp" />
<figcaption>Image d’exemple</figcaption>
</figure>
<figure id="fig:A1_27_segmentation_semantique">
<img src="../assets/figures/A1/A1_27_segmentation_semantique.webp" />
<figcaption>Segmentation sémantique</figcaption>
</figure>
<figure id="fig:A1_28_segmentation_instance">
<img src="../assets/figures/A1/A1_28_segmentation_instance.webp" />
<figcaption>Segmentation instance</figcaption>
</figure>
<figure id="fig:A1_29_segmentation_panoptique">
<img src="../assets/figures/A1/A1_29_segmentation_panoptique.webp" />
<figcaption>Segmentation panoptique</figcaption>
</figure>
<figcaption>Comparaison des différents types de segmentation d’image <span class="citation" data-cites="jung_benchmarking_2022">[<a href="../bibliography.html#ref-jung_benchmarking_2022" role="doc-biblioref">112</a>]</span></figcaption>
</figure>

La segmentation sémantique (Figure [6.27](#fig:A1_27_segmentation_semantique){reference-type="ref" reference="fig:A1_27_segmentation_semantique"}) va assigner une classe à chaque pixel de l’image. Ce genre de segmentation est utile pour distinguer par exemple les routes des immeubles, mais ce n’est pas assez sophistiqué pour distinguer les routes entre elles.

La segmentation instance (Figure [6.28](#fig:A1_28_segmentation_instance){reference-type="ref" reference="fig:A1_28_segmentation_instance"}) va permettre d’identifier les différents éléments d’une image, mais ne va pas lui assigner une classe.

La segmentation panoptique (Figure [6.29](#fig:A1_29_segmentation_panoptique){reference-type="ref" reference="fig:A1_29_segmentation_panoptique"}) est la combinaison des segmentations sémantique et instance. C’est la plus sophistiquée car elle permet d’assigner une classe à chaque pixel de l’image et en plus, fait la différence entre les différents objets appartenant à une même classe.

Le Tableau [6.9](#tab:comparatif_segmentation){reference-type="ref" reference="tab:comparatif_segmentation"} ci-dessous résume les différences.

| 2-4 | **Segm. sémantique** | **Segm. instance** | **Segm. panoptique** |
|:---|:---|:---|:---|
| Définition | Chaque pixel est assigné à une classe connue | Détecte les contours des objets, lui assigne un identifiant unique (“objet\_1”) à chaque objet. Ne lui attribue pas de classe. | Mélange de segmentation sémantique et instance. Chaque pixel a une classe et il peut différencier entre plusieurs objets de la même classe. |
| Sortie | Contours avec une classe attribuée | Contour par objet segmenté | Contour par objet segmenté avec un label |
| Sépare les objets de la même classe | Non | Oui, mais ne distingue pas les classes | Oui |

<span id="tab:comparatif_segmentation"></span>

<p class="thesis-caption"><em>Comparatif des différents types de segmentation d’image</em></p>
<figure id="fig:A1_30_segmentation_semantique_hepia" data-latex-placement="H">
<img src="../assets/figures/A1/A1_30_segmentation_semantique_hepia.webp" style="width:100.0%" />
<figcaption>Orthophoto d’exemple de segmentation</figcaption>
</figure>

La Figure [6.31](#fig:A1_30_segmentation_semantique_hepia){reference-type="ref" reference="fig:A1_30_segmentation_semantique_hepia"} est un exemple de segmentation sémantique, en plus de connaître la classe présente dans l’image, on connaît aussi le contour exact de l’objet. Comme pour la détection, le chiffre indiqué après la classe indique la probabilité estimée par le modèle que l’objet segmenté appartient à une certaine classe. Les chiffres sont identiques dans la Figure [6.25](#fig:A1_25_detection_hepia){reference-type="ref" reference="fig:A1_25_detection_hepia"} et la Figure [6.31](#fig:A1_30_segmentation_semantique_hepia){reference-type="ref" reference="fig:A1_30_segmentation_semantique_hepia"}.

### Évaluation des performances {#subsec:evaluation_des_performances}

L’évaluation des performances dans le domaine de la vision par ordinateur (« computer vision ») a nécessité de développer des métriques spécifiques :

- Intersection sur l’union (IoU) et moyenne de l’intersection sur l’union (mIoU)

- Average precision (AP)

- Mean average precision (mAP)

- Pixel accuracy (PA)

#### Intersection sur l’union (IoU) et moyenne de l’intersection sur l’union (mIoU) {#intersection-sur-lunion-iou-et-moyenne-de-lintersection-sur-lunion-miou}

L’intersection sur l’Union (IoU) mesure le chevauchement entre le masque de segmentation prédit et le masque de vérité terrain. Elle est calculée comme la zone d’intersection divisée par la zone d’union entre les deux masques. La Figure [6.32](#fig:A1_31_iou_concept){reference-type="ref" reference="fig:A1_31_iou_concept"} illustre ce concept. Plus le masque prédit par le modèle est proche de la valeur annotée (vérité terrain), plus le IoU sera élevé. Un IoU élevé indique que le modèle prédit bien.

<figure id="fig:A1_31_iou_concept" data-latex-placement="H">
<img src="../assets/figures/A1/A1_31_iou_concept.webp" style="width:50.0%" />
<figcaption>Intersection sur l’union <span class="citation" data-cites="rosebrock_intersection_2016">[<a href="../bibliography.html#ref-rosebrock_intersection_2016" role="doc-biblioref">113</a>]</span></figcaption>
</figure>

<figure id="fig:iou_exemples" data-latex-placement="H">
<figure id="fig:A1_32_iou_exemple1">
<img src="../assets/figures/A1/A1_32_iou_exemple1.webp" />
<figcaption>Exemple de bon IoU <span class="citation" data-cites="mechea_panoptic_2019">[<a href="../bibliography.html#ref-mechea_panoptic_2019" role="doc-biblioref">114</a>]</span></figcaption>
</figure>
<figure id="fig:A1_33_iou_exemple2">
<img src="../assets/figures/A1/A1_33_iou_exemple2.webp" />
<figcaption>Exemple de mauvais IoU <span class="citation" data-cites="mechea_panoptic_2019">[<a href="../bibliography.html#ref-mechea_panoptic_2019" role="doc-biblioref">114</a>]</span></figcaption>
</figure>
<figcaption>Exemples de IoU <span class="citation" data-cites="mechea_panoptic_2019">[<a href="../bibliography.html#ref-mechea_panoptic_2019" role="doc-biblioref">114</a>]</span></figcaption>
</figure>

Dans la Figure [6.35](#fig:iou_exemples){reference-type="ref" reference="fig:iou_exemples"}, on peut voir deux exemples de IoU. La Figure [6.33](#fig:A1_32_iou_exemple1){reference-type="ref" reference="fig:A1_32_iou_exemple1"} représente un IoU de 0.8, ce qui indique que le modèle a détecté un chat (cadre magenta) proche de la vérité terrain (cadre noir), cette détection devient un true positive (TP).

Dans la Figure [6.34](#fig:A1_33_iou_exemple2){reference-type="ref" reference="fig:A1_33_iou_exemple2"}, on observe que le modèle a détecté un chat (cadre magenta) là où il n’y en avait pas, cette détection devient un false positive (FP). Le modèle n’a pas vu le chat (cadre noir), cela comptera comme un false negative (FN).

L’intersection moyenne sur l’union (mIoU) est la moyenne de l’IoU pour toutes les classes.

#### Average precision (AP) {#average-precision-ap}

L’average precision (AP) se base sur le graphique precision-recall (Figure [6.36](#fig:A1_34_precision_recall){reference-type="ref" reference="fig:A1_34_precision_recall"}), ce graphique a dans l’axe des abscisses (x) le recall et dans l’axe des ordonnées (y) la precision. C’est un graphique qui va permettre de visualiser le lien entre la precision et le recall.

<figure id="fig:A1_34_precision_recall" data-latex-placement="H">
<img src="../assets/figures/A1/A1_34_precision_recall.webp" style="width:100.0%" />
<figcaption>Exemple de courbe precision-recall. Average precision (AP) et mean average precision (mAP) calculés dans la légende.</figcaption>
</figure>

Le choix du seuil de classification permet d’ajuster le compromis entre la precision et le recall. Un seuil bas maximise le recall au détriment de la precision, tandis qu’un seuil élevé maximise la precision au détriment du recall.

La courbe precision-recall visualise ce compromis. Une courbe proche du coin supérieur droit (precision = 1, recall = 1) indique de meilleures performances globales.

L’aire sous la courbe precision-recall, appelée Average Precision (AP), est une métrique résumée pour comparer les modèles.

Les étapes pour calculer l’average precision (AP) sont les suivantes :

1.  Prendre les seuils de classification générés par le modèle. Ceux-ci indiquent à quel point le modèle est sûr qu’un pixel appartient bien à une certaine classe. Ce sont des chiffres entre 0 et 1. Plus le chiffre est proche de 1, plus le modèle estime que la probabilité que le pixel appartient à une classe est élevée

2.  Calculer la precision et le recall pour les différents seuils de classification

3.  Tracer la courbe precision-recall

4.  L’average precision s’obtient en calculant l’aire sous la courbe (intégration ou approximation numérique via des trapèzes par exemple)

#### Mean average precision (mAP) {#mean-average-precision-map}

Dans les cas multi-classes, on calcule la moyenne des AP de l’ensemble des classes et on obtient le mean average precision (mAP). Sur la légende de la Figure [6.36](#fig:A1_34_precision_recall){reference-type="ref" reference="fig:A1_34_precision_recall"}, on peut voir un exemple de calcul de mAP, si l’on prend le AP des deux classes « rooftop » et « solar-panel », la moyenne est égale à 0.513.

Le mAP peut aussi être utilisé avec un seuil minimum de IoU, ce qui va indiquer la capacité du modèle à localiser de manière précise un objet. Les plus communs sont :

- mAP@0.5 (IoU supérieur ou égal à 0.5)

- mAP@0.95 (IoU supérieur ou égal à 0.95)

- mAP@&#91;0.5:0.95&#93; (mAP sur plusieurs seuils de l’IoU entre 0.5 et 0.95)

#### Pixel accuracy (PA) {#pixel-accuracy-pa}

Le Pixel Accuracy (PA) mesure le pourcentage de pixels correctement classés sur l’ensemble de l’image.

#### Panoptic Quality (PQ) {#panoptic-quality-pq}

La panoptic quality (PQ) &#91;[115](../bibliography.md#ref-kirillov_panoptic_2019)&#93; est utilisée dans la segmentation panoptique.

Le PQ permet d’avoir une métrique unique pour la détection du contour des objets (segmentation instance), mais aussi pour assigner une classe aux différents pixels (segmentation sémantique). L’équation se divise en deux parties :

- Segmentation quality (SQ)

- Recognition quality (RQ)

La segmentation quality (SQ) &#91;[115](../bibliography.md#ref-kirillov_panoptic_2019)&#93; évalue la qualité des masques de segmentation produits par un modèle de segmentation panoptique (Équation [&#91;eq:segmentation\_quality&#93;](#eq:segmentation_quality){reference-type="ref" reference="eq:segmentation_quality"}). Elle est calculée comme la moyenne de l’intersection sur l’union (mIoU) entre les segments prédits et les segments de la vérité de terrain qui ont été mis en correspondance.

<span id="eq:segmentation_quality"></span>

$$\begin{equation}
SQ = \frac{\sum_{(p,g) \in TP} IoU(p,g)}{|TP|}
\label{eq:segmentation_quality}
\end{equation}$$

<p class="thesis-caption"><em>(8)</em></p>

La recognition quality (RQ) &#91;[115](../bibliography.md#ref-kirillov_panoptic_2019)&#93; évalue l’accuracy des classes attribuées aux régions segmentées par un modèle de segmentation panoptique (Équation [&#91;eq:recognition\_quality&#93;](#eq:recognition_quality){reference-type="ref" reference="eq:recognition_quality"}). Elle est basée sur le score F1, qui est une moyenne harmonique de la precision et du recall.

<span id="eq:recognition_quality"></span>

$$\begin{equation}
RQ = \frac{|TP|}{|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}
\label{eq:recognition_quality}
\end{equation}$$

<p class="thesis-caption"><em>(9)</em></p>

Finalement, la panoptic quality (PQ) &#91;[115](../bibliography.md#ref-kirillov_panoptic_2019)&#93; (Équation [&#91;eq:panoptic\_quality&#93;](#eq:panoptic_quality){reference-type="ref" reference="eq:panoptic_quality"}) est la multiplication de SQ (Équation [&#91;eq:segmentation\_quality&#93;](#eq:segmentation_quality){reference-type="ref" reference="eq:segmentation_quality"}) et RQ (Équation [&#91;eq:recognition\_quality&#93;](#eq:recognition_quality){reference-type="ref" reference="eq:recognition_quality"})

<span id="eq:panoptic_quality"></span>

$$\begin{equation}
PQ = SQ \cdot RQ = \frac{\sum_{(p,g) \in TP} IoU(p,g)}{|TP|} \cdot \frac{|TP|}{|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}
\label{eq:panoptic_quality}
\end{equation}$$

<p class="thesis-caption"><em>(10)</em></p>

#### Métriques par application {#métriques-par-application}

Le Tableau [6.10](#tab:metrics_by_application){reference-type="ref" reference="tab:metrics_by_application"} ci-dessous met en lien les métriques et les différentes applications.

<table id="tab:metrics_by_application">
<caption>Métriques par application</caption>
<thead>
<tr>
<th style="text-align: left;"><span>2-6</span></th>
<th style="text-align: left;"><strong>Classification</strong></th>
<th style="text-align: left;"><strong>Détection</strong></th>
<th style="text-align: left;"><strong>Segmentation sémantique</strong></th>
<th style="text-align: left;"><strong>Segmentation instance</strong></th>
<th style="text-align: left;"><strong>Segmentation panoptique</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><strong>Principales métriques</strong></td>
<td style="text-align: left;"><ul>
<li><p>Accuracy</p></li>
<li><p>Precision</p></li>
<li><p>Recall</p></li>
<li><p>F1-Score</p></li>
<li><p>Matrice de confusion</p></li>
</ul></td>
<td style="text-align: left;"><ul>
<li><p>Intersection sur Union (IoU)</p></li>
<li><p>Average Precision (AP)</p></li>
<li><p>Mean average precision (mAP)</p></li>
</ul></td>
<td style="text-align: left;"><ul>
<li><p>Pixel accuracy (PA)</p></li>
<li><p>Moyenne intersection sur Union (mIoU)</p></li>
</ul></td>
<td style="text-align: left;"><ul>
<li><p>Average Precision (AP)</p></li>
<li><p>Mean average precision (mAP)</p></li>
</ul></td>
<td style="text-align: left;"><ul>
<li><p>Panoptic quality (PQ)</p></li>
</ul></td>
</tr>
</tbody>
</table>

[^1]: [https://opendata.swiss/fr](https://opendata.swiss/fr)

[^2]: [https://map.geo.admin.ch/](https://map.geo.admin.ch/)
