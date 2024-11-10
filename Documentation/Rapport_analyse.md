# Rapport d’étude du projet

## I. Introduction
Ce rapport explore en profondeur les données fournies par Enedis pour évaluer l’impact de la classe de Diagnostic de Performance Énergétique (DPE) sur la consommation électrique des logements. Dans le cadre de ce projet, l’application **GreenTech Solutions** a été développée comme un outil d’analyse avancé pour optimiser la performance énergétique des habitations. Elle permet de prédire la consommation énergétique et de classifier chaque logement selon son étiquette DPE, offrant aux utilisateurs des informations claires et accessibles sur leur efficacité énergétique. Avec une interface intuitive, cette application facilite une prise de décision éclairée, rendant les données facilement exploitables pour des modèles de prédiction futurs.

## II. Présentation des données
Les données utilisées dans ce projet proviennent de l'API d'ENEDIS et se concentrent exclusivement sur le département du Rhône (69). Deux fichiers principaux ont été extraits : `existant_69.csv`, qui contient les informations des logements anciens, et `neufs_69.csv`, qui rassemble celles des nouveaux logements.

### Types de données
- **Object** : Colonnes contenant des descriptions qualitatives des biens immobiliers, telles que le type de local (maison, appartement, etc.).
- **Float** : Données numériques décimales, par exemple, la surface habitable des logements.
- **Int** : Données numériques entières, comme les codes INSEE des communes.

Ce projet s'appuie sur ces données pour évaluer l'impact du DPE sur la consommation énergétique.

## III. Prétraitement des données
Le prétraitement des données est une étape cruciale dans le processus d’analyse, car il permet de transformer les données brutes en un format exploitable, assurant ainsi leur qualité et leur cohérence pour des résultats fiables.

### A. Chargement et Prévisualisation des Données
Les données ont été chargées et explorées pour obtenir un aperçu général de leur structure et de leur contenu. Grâce aux bibliothèques **Pandas** et **Numpy**, nous avons importé les données depuis les fichiers CSV, puis prévisualisé les premières lignes à l'aide de `data.head()`. Cette inspection initiale a permis de vérifier la structure des colonnes, les types de données et de détecter des valeurs manquantes ou des anomalies.

### B. Analyse Exploratoire des Données
Cette étape permet de comprendre la structure et les caractéristiques des données, d'identifier d'éventuels problèmes, et d'analyser la distribution de chaque variable. Afin de distinguer les logements anciens des nouveaux, une colonne "logement" a été ajoutée avec les valeurs "ancien" pour les logements existants et "neuf" pour les logements neufs. Une colonne "Année_construction" a aussi été ajoutée, avec la valeur "2024" pour les logements neufs.

#### a. Colonnes communes et concaténation
Une jointure a été réalisée pour permettre la prédiction à partir des deux datasets en vérifiant les colonnes communes, puis en concaténant les DataFrames `dpe_existant` et `dpe_neuf` en utilisant seulement les colonnes communes (`join='inner'`, `ignore_index=True`). Des colonnes additionnelles comme "Annee_reception_DPE", "Somme_coûts", "Coût chauffage en %", "passoire_energetique" ont été ajoutées pour enrichir l’analyse.

#### b. Statistiques descriptives
Les statistiques descriptives (moyenne, écart-type, minimum, maximum, quartiles) ont été calculées pour identifier des anomalies, comme des valeurs extrêmes, et mieux comprendre la variabilité des données.

#### c. Valeurs manquantes
Pour identifier les colonnes nécessitant un traitement spécifique, la proportion de valeurs manquantes dans chaque colonne a été calculée. Cela a permis de déterminer si un remplacement, une imputation, ou une suppression était nécessaire avant de continuer.

#### d. Nettoyage des colonnes
Les colonnes contenant plus de 20 % de valeurs manquantes (seuil de 0.8) ont été supprimées. Après le nettoyage, les données concaténées ont été stockées dans un fichier Excel, `data69rhone.csv`, pour les étapes suivantes de classification et de régression.

## IV. Modèle de prédiction
Dans cette section, nous détaillons le processus de développement des modèles de prédiction de l’étiquette DPE et de la consommation énergétique.

### A. Prédiction de l’étiquette DPE
1. **Nettoyage des données de classification**  
   Les valeurs manquantes ont été imputées (mode pour les qualitatives, médiane pour les quantitatives), et la distribution de la variable cible, `Étiquette_DPE`, a été analysée.

2. **Sélection des variables explicatives**  
   Les colonnes qualitatives et quantitatives ont été séparées, les valeurs manquantes remplacées, et les variables qualitatives encodées à l’aide de `OrdinalEncoder()`.

3. **Échantillonnage et modèles utilisés**  
   Les données ont été divisées en 70 % pour l’entraînement et 30 % pour le test. Les modèles utilisés incluent l’Arbre de décision, KNN, SMOTE, Random Forest, et la régression logistique. Le modèle **Random Forest** a donné la meilleure précision (99 %).


### B. Prédiction de la consommation

1. **Nettoyage des données de régression**  
   La première étape dans l'élaboration de notre modèle a été le nettoyage des données cibles, c'est-à-dire les consommations. Ce nettoyage s'est fait en deux étapes :
   - Suppression des valeurs manquantes
   - Élimination des valeurs situées en dehors des 15ᵉ et 95ᵉ percentiles pour éviter les valeurs extrêmes qui pourraient biaiser le modèle.
 
   ![Distribution des données](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/distribution.png)

2. **Normalisation des données numériques**  
   Nos données numériques étant exprimées dans des unités différentes, nous avons procédé à une normalisation pour ramener toutes les valeurs à la même échelle.

3. **Encodage des variables catégorielles**  
   Nous avons utilisé le label encoding pour transformer les variables catégorielles, facilitant ainsi leur exploitation dans le modèle.

4. **Sélection des variables explicatives**  
   Nous avons utilisé la corrélation pour sélectionner les variables explicatives pertinentes.

   ![Corrélation des variables](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/correlationRegression.png)

5. **Sélection des modèles**  
   Nous avons testé plusieurs modèles pour prédire la consommation :

   - **Régression linéaire**  
     Le premier modèle testé a été la régression linéaire, qui nous a donné une **RMSE de 218**.  
     ![Graphique de la régression linéaire](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/regression.png)  
     ![Score de la régression linéaire](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/scorerrEGRESSION.png)

   - **Arbre de décision**  
     ![Arbre de décision](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/arbreDecision.png)  
     ![Score de l'arbre de décision](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/scoreArbre.png)

   - **Random Forest Regressor**  
     ![Random Forest](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/randomForesst.png)  
     ![Score du Random Forest](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/scoreForest.png)

6. **Modèle sélectionné et variables retenues**  
   Au vu des scores des différents modèles, nous avons opté pour le Random Forest. Nous avons également sélectionné les 10 variables les plus pertinentes pour optimiser la prédiction.  

   ![Importance des variables](https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/assets/ImportanceVarible.png)

## VI. Conclusions et Recommandations
L’analyse montre que certaines variables influencent fortement l'étiquette DPE, avec le **RandomForestClassifier** offrant la meilleure précision. Des recommandations incluent l’optimisation des dépenses énergétiques et des politiques de rénovation. Les limitations incluent la qualité des données et les choix de modèles. Les améliorations possibles englobent l’utilisation de nouveaux algorithmes et un tuning plus approfondi des hyperparamètres.
