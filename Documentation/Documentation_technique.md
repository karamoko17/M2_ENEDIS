# Documentation Technique du Système de Prévision de Consommation Énergétique

## Aperçu Général

![alt text](architecture.jpeg)

Cette architecture est un système de prévision de la consommation énergétique et de classification des logements en fonction de leur performance énergétique (DPE). Elle intègre des sources de données externes, des modèles de machine learning pour la classification et la régression, une API pour l'interfaçage, et une interface utilisateur pour la visualisation.

## Composants Principaux

### 1. Source de Données
- **ENEDIS** : La source principale des données est Enedis, qui fournit des informations sur la consommation énergétique des logements. Ces données sont récupérées via une API et stockées dans une base de données centralisée pour l'analyse.

### 2. Stockage des Données
- **DATA** : Les données extraites d'Enedis sont stockées dans une base de données ou un système de stockage de fichiers. Ce stockage sert de source de données pour les modèles de machine learning de classification et de régression.

### 3. Modèles de Machine Learning
   - **Classification** : Ce modèle est utilisé pour classifier les logements selon leur étiquette DPE (Diagnostic de Performance Énergétique). Il utilise des algorithmes de machine learning pour déterminer l'étiquette énergétique de chaque logement, basée sur les caractéristiques extraites des données.
   - **Régression** : Ce modèle prédit la consommation énergétique des logements en utilisant des algorithmes de régression. La régression est appliquée pour obtenir une valeur continue de consommation énergétique, permettant une estimation précise pour chaque logement.

### 4. API Flask
- **API FLASK** : Une API développée avec Flask est utilisée pour exposer les modèles de machine learning en tant que services web. Cette API permet de faire des prédictions en temps réel via des appels API externes. Elle communique avec les modèles de classification et de régression, et renvoie les résultats de prédiction aux applications clientes.
   - **Endpoints** : L'API comporte différents endpoints pour :
     - Envoyer les données de logement et récupérer l'étiquette DPE prédite (classification).
     - Envoyer les caractéristiques d'un logement et obtenir une estimation de la consommation énergétique (régression).

### 5. Cartographie
- **Cartography** : Ce composant gère la géolocalisation des logements en fonction de leurs adresses. Les adresses sont transformées en coordonnées géographiques, permettant une visualisation géographique des performances énergétiques et de la consommation sur une carte.

### 6. Interface Utilisateur avec Streamlit
- **Streamlit** : Une interface utilisateur (UI) est développée avec Streamlit pour permettre aux utilisateurs finaux de visualiser les résultats des modèles et d'interagir avec les données de manière intuitive.
   - **Visualisation des Résultats** : L’interface affiche les prévisions et les classifications des logements sous forme de graphiques et de cartes interactives, facilitant la prise de décisions éclairées.
   - **Interactivité** : Les utilisateurs peuvent sélectionner des critères spécifiques pour explorer les données de consommation énergétique et les étiquettes DPE des logements dans leur région.

## Flux de Données

1. Les données sont récupérées depuis l'API d'Enedis et stockées dans une base de données centralisée.
2. Les données sont prétraitées et utilisées pour entraîner les modèles de classification et de régression.
3. Lorsqu'un utilisateur envoie une demande via l'interface Streamlit, l'API Flask est appelée pour obtenir une prédiction :
   - Le modèle de classification fournit une étiquette DPE.
   - Le modèle de régression prédit la consommation énergétique.
4. Les résultats sont renvoyés à l'interface utilisateur, où ils sont visualisés sur des cartes et des graphiques interactifs.

## Technologies Utilisées

- **Enedis API** : Source de données principale.
- **Python** : Langage principal pour le développement des modèles, l'API et l'interface.
- **Pandas, Scikit-Learn** : Pour le traitement des données et le développement des modèles de machine learning.
- **Flask** : Framework pour créer l’API RESTful.
- **Streamlit** : Outil pour développer une interface utilisateur interactive et accessible.
- **Cartographie (ex. Folium, Plotly)** : Pour la représentation géographique des logements sur une carte.

## Cas d’Utilisation

1. **Prédiction de l’étiquette DPE** : L’utilisateur entre des informations sur un logement, et l’API renvoie une classification DPE.
2. **Estimation de la consommation énergétique** : L’utilisateur fournit des caractéristiques du logement, et l’API renvoie une estimation de consommation.
3. **Visualisation Géographique** : L’utilisateur explore une carte interactive pour voir les performances énergétiques des logements par zone géographique.
