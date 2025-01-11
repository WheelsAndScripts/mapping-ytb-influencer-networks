# Documentation : Relations entre chaînes YouTube (idées)

## 1. Relations basées sur les collaborations
**Idée**  
Deux chaînes sont liées si elles collaborent sur des vidéos ou mentionnent l'une l'autre dans leurs descriptions ou titres.  

**Données à collecter**  
- Identifiants des vidéos (`videoId`) publiées par une chaîne.  
- Titres et descriptions des vidéos (chercher des mentions d'autres chaînes ou noms explicites).  
- Collaborateurs explicitement ajoutés (via `snippet.channelId` dans les réponses de vidéos).

---

## 2. Relations basées sur les abonnés communs
**Idée**  
Deux chaînes sont liées si elles partagent des abonnés.  

**Données à collecter**  
- Liste des abonnés (limité, car l'API n'expose pas directement ces données pour toutes les chaînes).  
- Si possible, liste des chaînes auxquelles une chaîne est abonnée.

---

## 3. Relations basées sur les thèmes (tags ou catégories de contenu)
**Idée**  
Deux chaînes sont liées si elles produisent des vidéos sur des thèmes similaires.  

**Données à collecter**  
- Tags des vidéos (`tags` dans `snippet`).  
- Catégories des vidéos (`categoryId` dans `snippet`).  
- Titres et descriptions des vidéos (analyse de mots-clés).

---

## 4. Relations basées sur les recommandations croisées
**Idée**  
Deux chaînes sont liées si l'une recommande l'autre dans sa section "Chaînes en vedette".  

**Données à collecter**  
- Liste des chaînes en vedette d'une chaîne (`brandingSettings.channel.featuredChannelsUrls` dans `channels.list`).

---

## 5. Relations basées sur les mentions dans les commentaires (à réfléchir)
**Idée**  
Deux chaînes sont liées si leurs vidéos ont des interactions via des commentaires mentionnant d'autres chaînes.  

**Données à collecter**  
- Commentaires sous les vidéos publiées par une chaîne (via `commentThreads`).  
- Identifiants des utilisateurs/commentateurs (`authorChannelId` dans les commentaires).



# Résumé des données clés à extraire avec l'API YouTube

| **Donnée**                           | **Endpoint API YouTube**       | **Champs clés à récupérer**                                |
|--------------------------------------|--------------------------------|-----------------------------------------------------------|
| Informations de base sur une chaîne  | `channels.list`               | `id`, `snippet.title`, `statistics`                      |
| Vidéos d'une chaîne                  | `search.list`                 | `videoId`, `snippet.title`, `snippet.description`         |
| Détails des vidéos                   | `videos.list`                 | `snippet`, `statistics`, `topicDetails`                  |
| Commentaires des vidéos              | `commentThreads.list`         | `snippet.topLevelComment`, `authorChannelId`             |
| Chaînes recommandées                 | `channels.list`               | `brandingSettings.channel.featuredChannelsUrls`          |
