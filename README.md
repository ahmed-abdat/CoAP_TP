# Implémentation du Protocole CoAP - TP

Ce projet contient l'implémentation d'un serveur CoAP et plusieurs clients pour démontrer les différents aspects du protocole CoAP (Constrained Application Protocol).

## 📋 Prérequis

- Python 3.x
- Port UDP 5683 disponible
- Wireshark (optionnel, pour l'analyse du trafic réseau)

## 📁 Structure du Projet

```
.
├── coap_basic_server1.py    # Serveur CoAP avec ressource /time
├── coap_empty_msg.py        # Client pour tester les messages vides
├── coap_get_time1.py        # Premier client GET (avec ACK simple)
├── coap_get_time2.py        # Client GET avec attente du second message
├── coap_get_time3.py        # Client GET avec acquittement complet
├── coap_get_time4.py        # Client GET avec token
└── coap_get_time_non.py     # Client GET non-confirmable
```

## 🚀 Installation et Exécution

1. Vérifiez que le port 5683 est disponible :

```bash
netstat -ano | findstr :5683
```

2. Démarrez d'abord le serveur :

```bash
python coap_basic_server1.py
```

3. Dans un autre terminal, exécutez l'un des clients :

```bash
python coap_empty_msg.py        # Pour tester les messages vides
python coap_get_time1.py        # Pour le GET simple
python coap_get_time2.py        # Pour le GET avec second message
python coap_get_time3.py        # Pour le GET avec ACK complet
python coap_get_time4.py        # Pour le GET avec token
python coap_get_time_non.py     # Pour le GET non-confirmable
```

## 📝 Description des Programmes

### Serveur CoAP (`coap_basic_server1.py`)

- Implémente un serveur CoAP basique
- Fournit une ressource `/time` qui renvoie l'heure actuelle
- Simule un délai de traitement de 5 secondes
- Gère les requêtes confirmables (CON) et non-confirmables (NON)

### Clients CoAP

1. **Message Vide** (`coap_empty_msg.py`)

   - Envoie un message CoAP vide
   - Démontre la structure de base d'un message CoAP
   - Le serveur répond avec un message RST

2. **GET Simple** (`coap_get_time1.py`)

   - Envoie une requête GET confirmable
   - Reçoit uniquement l'ACK initial
   - Ne gère pas la réponse séparée

3. **GET avec Second Message** (`coap_get_time2.py`)

   - Amélioration du GET simple
   - Attend la réponse séparée après l'ACK
   - Ne gère pas l'acquittement de la réponse

4. **GET avec ACK Complet** (`coap_get_time3.py`)

   - Version complète avec gestion des acquittements
   - Acquitte la réponse du serveur
   - Évite les retransmissions

5. **GET avec Token** (`coap_get_time4.py`)

   - Ajoute un token pour lier requête et réponse
   - Démontre la gestion des tokens dans CoAP
   - Utile pour les requêtes multiples

6. **GET Non-Confirmable** (`coap_get_time_non.py`)
   - Utilise le mode non-confirmable (NON)
   - Pas d'acquittement nécessaire
   - Plus rapide mais moins fiable

## 🔍 Analyse avec Wireshark

Pour analyser le trafic CoAP :

1. Lancez Wireshark
2. Appliquez le filtre : `udp.port==5683`
3. Observez les échanges entre client et serveur

## 🚨 Structure des Messages CoAP

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ver| T |  TKL  |      Code     |          Message ID           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Token (si présent) ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Options (si présentes) ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## ⚠️ Dépannage

1. Si le port est déjà utilisé :

```bash
taskkill /F /PID [NUMERO_PID]
```

2. Si pas de réponse du serveur :
   - Vérifiez que le serveur est en cours d'exécution
   - Vérifiez l'adresse IP du serveur dans les clients
   - Utilisez Wireshark pour déboguer
