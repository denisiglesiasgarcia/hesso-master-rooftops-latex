---
description: "La crise climatique et la crise énergétique poussent à une gestion plus efficace de l’espace territorial. L’utilisation des toits pour des installations…"
---

# Introduction {#chap:introduction}

## Contexte {#contexte}

La crise climatique &#91;[1](../bibliography.md#ref-lee_ipcc_2023)&#93; et la crise énergétique poussent à une gestion plus efficace de l’espace territorial. L’utilisation des toits pour des installations solaires et des espaces verts est une solution prometteuse pour la production d’énergie locale et la biodiversité urbaine, sans compromettre d’autres fonctions du territoire. Cependant, un défi majeur est le manque de données sur les surfaces disponibles des toits. Il n’y a pas de recensement fédéral des toits végétalisés et les installations solaires sont partiellement renseignées. La diversité des objets présents sur les toits comme par exemple gaines de ventilation, monoblocs ou antennes rend difficile l’établissement d’un inventaire précis.

L’Office cantonal de l’énergie de Genève (<a href="../glossary.html#gloss-ocen"><span data-acronym-label="ocen" data-acronym-form="singular+abbrv">ocen</span></a>) a réalisé plusieurs projets pour mieux évaluer le potentiel d’utilisation des toitures.

Un de ces projets &#91;[2](../bibliography.md#ref-herny_detection_2024)&#93; est mené par le <a href="../glossary.html#gloss-stdl"><span data-acronym-label="stdl" data-acronym-form="singular+short">stdl</span></a>, son objectif vise à détecter automatiquement les objets présents sur les toits pour identifier les surfaces disponibles pour des installations solaires ou des toitures végétalisées. Trois approches sont comparées. La première est une classification des pans de toit par algorithme random forest, la deuxième est une segmentation de nuages de points <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> , et la troisième est une segmentation d’orthophotos par deep learning (Segment Anything Model). La classification ressort comme la méthode la plus performante et applicable à grande échelle.

Le cadastre solaire du Grand Genève &#91;[3](../bibliography.md#ref-desthieux_solar_2018)&#93; est un autre projet important qui s’inscrit dans la même optique de valorisation des toitures pour la production d’énergie renouvelable. Ce cadastre est conçu pour évaluer le potentiel de production d’énergie solaire des toitures. Il prend en compte des paramètres cruciaux comme les ombrages proches et lointains, qui influencent significativement la quantité d’énergie qu’une installation solaire peut générer. Ce cadastre permet d’identifier les toitures propices à l’installation de panneaux solaires.

Les projets d’identification des toitures disponibles et le cadastre solaire du Grand Genève se complètent. L’identification des toits fournit une base pour repérer où installer des panneaux solaires. Ensuite, le cadastre solaire évalue le potentiel de production d’énergie de ces toitures. Ensemble, ils maximisent l’efficacité de la production d’énergie renouvelable locale, jouant un rôle clé dans la planification énergétique et environnementale d’un territoire.

## Objectifs {#objectifs}

Cette section présente les objectifs du travail de master (<a href="../glossary.html#gloss-tm"><span data-acronym-label="tm" data-acronym-form="singular+abbrv">tm</span></a>) :

- Analyse comparative des méthodologies existantes :

  - Examiner les techniques utilisées par le <a href="../glossary.html#gloss-stdl"><span data-acronym-label="stdl" data-acronym-form="singular+abbrv">stdl</span></a> pour l’identification des toitures.

  - Étudier les méthodes employées par le cadastre solaire du Grand Genève pour évaluer le potentiel de production d’énergie solaire.

  - Rechercher et analyser des projets similaires au niveau international.

- État de l’art :

  - Réaliser une revue de littérature approfondie pour identifier les méthodes et technologies récentes dans les domaines de la cartographie du potentiel solaire et de l’analyse de toitures.

- Développement d’un modèle personnalisé :

  - Finaliser le développement d’un modèle propre, en explorant des techniques telles que les réseaux de neurones convolutifs (CNN).

  - Collecter et étiqueter les données nécessaires à l’entraînement du modèle.

- Calcul du potentiel solaire :

  - Estimer le potentiel de production d’énergie solaire des toitures disponibles détectées par le modèle développé et celui de <a href="../glossary.html#gloss-stdl"><span data-acronym-label="stdl" data-acronym-form="singular+abbrv">stdl</span></a>.

- Implémentation et comparaison des modèles :

  - Appliquer les différents modèles à l’échelle du Canton de Genève.

  - Comparer les méthodologies utilisées et les résultats obtenus.

- Exploration de méthodes alternatives :

  - Étudier l’utilisation d’autres méthodes ou outils de traitement d’images et de segmentation pour améliorer l’exactitude et la vitesse d’identification des surfaces utiles sur les toits.

- Comparaison avec des outils existants :

  - Comparer les performances de la méthodologie utilisée pour le Cadastre Solaire du Grand Genève avec d’autres outils de cartographie solaire existants.

  - Identifier les forces et les faiblesses de chaque approche.

- Visualisation interactive des résultats :

  - Créer une visualisation interactive pour illustrer l’influence des différents facteurs sur le potentiel de production d’énergie solaire des toitures.

  - Faciliter la compréhension et l’interprétation des résultats par les décideurs et les professionnels de la planification territoriale.

- Documentation et partage des connaissances :

  - Documenter les connaissances acquises lors du développement du nouveau modèle.

  - Fournir des instructions détaillées et un code réutilisable pour permettre à d’autres personnes d’utiliser le modèle développé.

## Organisation de ce rapport {#organisation-de-ce-rapport}

Ce rapport est organisé en cinq chapitres principaux et deux annexes techniques. La structure suit une progression logique depuis la présentation du problème jusqu’aux résultats obtenus.

Le Chapitre 2 présente l’état de l’art en trois parties. Il commence par analyser les méthodes existantes pour évaluer le potentiel solaire des toitures, notamment les approches basées sur les données <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> et cadastrales. Il examine ensuite les avancées en machine learning appliqué aux images, en particulier les modèles de segmentation. Pour finir, il détaille les travaux combinant machine learning et évaluation du potentiel solaire, incluant ceux du <a href="../glossary.html#gloss-stdl"><span data-acronym-label="stdl" data-acronym-form="singular+short">stdl</span></a>, et liste les datasets disponibles.

Le Chapitre 3 décrit la méthodologie développée pour créer un modèle de segmentation sémantique. Il couvre tout le processus : sélection et préparation des données du <a href="../glossary.html#gloss-sitg"><span data-acronym-label="sitg" data-acronym-form="singular+short">sitg</span></a>, création du dataset annoté et développement des modèles. Le processus de labellisation, qui a demandé 180 heures de travail manuel, est décrit en détail. Le chapitre présente aussi les pistes explorées mais abandonnées pour montrer le cheminement complet.

Le Chapitre 4 présente l’évaluation des 93 configurations de modèles testées. L’analyse quantitative sur le dataset de test identifie les meilleures architectures selon plusieurs métriques (IoU, mAP, F1-score). L’étude du rapport performance-complexité aide à choisir les modèles pour une utilisation pratique. La validation qualitative sur la zone de <a href="../glossary.html#gloss-hepia"><span data-acronym-label="hepia" data-acronym-form="singular+short">hepia</span></a>, non utilisée pour l’entraînement, montre que les modèles généralisent bien mais révèle aussi leurs limites.

Le Chapitre 5 résume les contributions principales et les compare à l’état de l’art. Il identifie les limites actuelles, notamment pour les toitures végétalisées et les zones très ombragées, et propose des améliorations. Les possibilités d’application et d’extension à d’autres territoires sont discutées.

Deux annexes complètent le document. L’Annexe A présente les bases du machine learning et de la segmentation d’images. L’Annexe B explique les concepts d’énergie solaire et leur utilisation dans les cadastres solaires.
