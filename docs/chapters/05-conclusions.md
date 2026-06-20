---
description: "Ce travail de master s’intéresse à la transition énergétique et à l’utilisation des toitures pour produire de l’énergie solaire. L’objectif est de créer…"
---

# Conclusion {#chap:conclusion}

Ce travail de master s’intéresse à la transition énergétique et à l’utilisation des toitures pour produire de l’énergie solaire. L’objectif est de créer une méthode pour identifier les espaces libres sur les toitures du canton de Genève en utilisant le machine learning et la segmentation sémantique d’orthophotos.

## Synthèse des contributions {#synthèse-des-contributions}

Ce travail apporte plusieurs contributions à l’analyse automatisée des toitures pour évaluer leur potentiel solaire.

### Création d’un dataset de référence {#création-dun-dataset-de-référence}

La contribution principale est la création d’un dataset annoté pour segmenter les espaces libres sur les toitures. Ce dataset comprend :

- 530 images géoréférencées de pixels provenant des orthophotos 2019 de <a href="../glossary.html#gloss-sitg"><span data-acronym-label="sitg" data-acronym-form="singular+abbrv">sitg</span></a>

- Un échantillonnage stratifié par catégorie SIA et surface de toiture pour représenter la diversité architecturale du canton

- Des annotations manuelles précises réalisées en environ 180 heures pour distinguer les espaces libres des obstacles

- Une méthodologie de post-traitement évitant les fuites de données entre les datasets d’entraînement, validation et test

Ce dataset comble un vide dans la littérature. Jusqu’à présent, seul le dataset RID était disponible mais il se limitait au contexte rural allemand.

### Développement et évaluation de modèles performants {#développement-et-évaluation-de-modèles-performants}

L’évaluation de 93 configurations a permis d’identifier les meilleures architectures pour cette tâche :

- 89 modèles de Segmentation Models PyTorch (SMP) avec différentes combinaisons encodeur-décodeur

- 4 variantes de YOLOv12 adaptées pour la segmentation

- Une stratégie d’ensemble k-fold qui améliore les performances de 0,9% à 2,0%

- LinkNet + EfficientNet-B5 identifié comme la meilleure configuration (IoU de 0,741)

### Analyse du compromis performance-complexité {#analyse-du-compromis-performance-complexité}

L’analyse du front de Pareto montre que les gains deviennent négligeables au-delà de 25 millions de paramètres. Cette information aide à choisir des architectures efficientes pour un déploiement pratique en identifiant les configurations avec le meilleur rapport performance-complexité.

### Validation sur des données réelles {#validation-sur-des-données-réelles}

Les tests sur la zone de <a href="../glossary.html#gloss-hepia"><span data-acronym-label="hepia" data-acronym-form="singular+abbrv">hepia</span></a>, qui n’était pas dans les données d’entraînement, confirment la capacité de généralisation des modèles. Les résultats révèlent aussi les limites actuelles, notamment pour les toitures praticables, végétalisées ainsi que les zones très ombragées.

## Analyse comparative avec l’état de l’art {#analyse-comparative-avec-létat-de-lart}

### Positionnement par rapport aux travaux existants {#positionnement-par-rapport-aux-travaux-existants}

Ce travail se distingue des approches existantes par plusieurs aspects :

Par rapport aux travaux du Swiss Territorial Data Lab (<a href="../glossary.html#gloss-stdl"><span data-acronym-label="stdl" data-acronym-form="singular+abbrv">stdl</span></a>), cette approche de segmentation sémantique surpasse les méthodes testées par <a href="../glossary.html#gloss-stdl"><span data-acronym-label="stdl" data-acronym-form="singular+abbrv">stdl</span></a> :

- IoU de 0,741 contre 0,38-0,40 pour les segmentations <a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a> et d’images de <a href="../glossary.html#gloss-stdl"><span data-acronym-label="stdl" data-acronym-form="singular+abbrv">stdl</span></a>

- Temps de traitement significativement réduit comparé aux 12 minutes par 25 bâtiments de leur segmentation d’images

- Qualité visuelle des résultats supérieure, répondant mieux aux attentes des experts métier

Comparé à l’utilisation directe de SAM, l’approche proposée offre :

- Une meilleure gestion des ombrages, problème majeur identifié avec SAM

- Des temps de calcul considérablement réduits (quelques secondes contre 7 minutes par image)

- Une précision adaptée à la tâche spécifique sans nécessiter de post-traitement complexe

Par rapport aux méthodes de classification géomatique explorées, la segmentation sémantique s’avère plus fiable :

- Indépendance vis-à-vis de la complétude des couches vectorielles de superstructures

- Capacité à détecter des obstacles non répertoriés dans les données géomatiques

- Précision au niveau du pixel plutôt qu’au niveau du polygone entier

### Apports méthodologiques {#apports-méthodologiques}

La méthodologie développée introduit plusieurs innovations :

- Une stratégie d’échantillonnage stratifié multicritères pour assurer la représentativité du dataset

- Un processus de gestion des chevauchements entre tuiles pour éviter les fuites de données

- Une approche d’ensemble k-fold optimisant l’utilisation des données annotées limitées

- Une évaluation multi-métrique permettant une analyse fine des performances selon différents critères

## Limites et perspectives d’amélioration {#limites-et-perspectives-damélioration}

### Limites identifiées {#limites-identifiées}

Malgré des performances satisfaisantes, plusieurs limites apparaissent :

#### Limites du dataset {#limites-du-dataset}

- Les toitures végétalisées et terrasses praticables sont sous-représentées

- Le déséquilibre entre exemples positifs et négatifs ressort particulièrement dans les cas d’IoU nul

- Certaines images contiennent moins de 1% de surface de toiture, ce qui complique l’apprentissage

- Les critères d’annotation restent parfois flous pour certaines surfaces (serres, terrasses)

#### Limitations techniques {#limitations-techniques}

- Les performances chutent sous ombrage intense, avec des variations selon les combinaisons encodeur-décodeur

- La distinction entre surfaces praticables et non praticables reste difficile

- Les modèles sont sensibles aux variations d’éclairage et de contraste

### Perspectives d’amélioration {#perspectives-damélioration-1}

#### Enrichissement du dataset {#enrichissement-du-dataset}

Le dataset pourrait être amélioré sur plusieurs points :

- Ajouter plus d’exemples de toitures végétalisées et terrasses praticables

- Diversifier les exemples négatifs pour diminuer les faux positifs

- Inclure des images prises sous différents éclairages pour mieux gérer les ombrages

- Ajout d’un deuxième annotateur expert métier pour valider les annotations existantes

#### Améliorations techniques {#améliorations-techniques}

- Développer un pré-traitement adaptatif pour normaliser l’éclairage

- Intégrer des données complémentaires (<a href="../glossary.html#gloss-lidar"><span data-acronym-label="lidar" data-acronym-form="singular+short">lidar</span></a>, modèles 3D) pour mieux discriminer les surfaces

- Créer des architectures d’ensemble combinant plusieurs modèles aux forces complémentaires

#### Extension fonctionnelle {#extension-fonctionnelle}

- Connecter directement avec les calculs de potentiel solaire du cadastre genevois

- Créer une interface pour la validation et correction semi-automatique

- Adapter la méthode à d’autres régions et types d’architecture

- Étendre l’analyse à d’autres surfaces comme les couverts

## Conclusion générale {#conclusion-générale}

Ce travail démontre que la segmentation sémantique fonctionne bien pour identifier automatiquement les espaces libres sur les toitures. Avec un IoU de 0,741 pour la meilleure configuration, les résultats montrent que la méthodologie est assez robuste pour une utilisation pratique.

### Impact et applications {#impact-et-applications}

Ce travail a plusieurs retombées :

#### Impact scientifique {#impact-scientifique}

La création d’un dataset de référence et l’évaluation de nombreuses architectures font avancer les connaissances en analyse automatisée d’orthophotos. Les conclusions sur le rapport performance-complexité et l’efficacité des différentes approches sont très utiles.

#### Applications pratiques {#applications-pratiques}

- Amélioration du cadastre solaire genevois grâce à une meilleure identification des surfaces disponibles

- Gain de temps pour l’évaluation des projets d’installation solaire

- Aide à la planification énergétique territoriale et aux objectifs de transition énergétique

- Outil de décision pour les propriétaires et professionnels du solaire

#### Impact environnemental {#impact-environnemental}

En facilitant l’identification des surfaces pour le solaire, ce travail aide indirectement au déploiement des énergies renouvelables et participe aux objectifs de décarbonation et de transition énergétique.

### Perspectives futures {#perspectives-futures}

Ce travail ouvre plusieurs pistes :

#### Recherche académique {#recherche-académique}

- Extension aux façades pour évaluer tout le potentiel solaire des bâtiments

- Utilisation de données historiques pour suivre l’évolution des toitures

- Développement d’approches semi-automatisées pour réduire le travail d’annotation

#### Transfert technologique {#transfert-technologique}

- Intégration dans les outils de planification énergétique existants

- Adaptation à d’autres régions suisses et européennes

### Réflexion finale {#réflexion-finale}

Les 180 heures passées sur l’annotation montrent qu’il faut développer des approches semi-automatiques pour étendre cette méthode à d’autres territoires. Les résultats obtenus justifient cet effort et montrent que le machine learning peut aider concrètement la transition énergétique.

Ce travail montre aussi l’importance de combiner géomatique, informatique et énergétique pour créer des solutions aux défis environnementaux actuels. La méthode rigoureuse et les bons résultats obtenus forment une base solide pour continuer dans cette direction.

Ce travail apporte une contribution pratique aux outils disponibles pour accélérer la transition énergétique. Il montre que le machine learning peut servir des objectifs environnementaux tout en répondant aux besoins concrets des acteurs du territoire.
