# 🚀 Application de Gestion Transport & Planification

## 📘 Introduction
Cette application Angular permet la gestion de **sites**, **trajets**, **planification**, **collaborateurs** et **compagnies de transport**.  
Elle intègre plusieurs librairies et frameworks modernes pour offrir une interface riche et modulaire :

- **Angular** (framework principal)
- **PrimeNG** (UI components)
- **Google Maps API** (cartographie et trajets)
- **ngx-translate** (internationalisation)
- **ngx-permissions** (gestion des permissions et accès)
- **ng-circle-progress** (visualisation graphique)

---

## 📂 Structure du projet

src/app  
├── 📦 core/            # Services, modèles, interceptors, guards
├── 🧩 features/        # Composants métiers (login, sites, trajets, etc.)
├── ♻️ shared/          # Composants et pipes réutilisables
├── 🎨 assets/          # Fichiers statiques (traductions, images)
├── ⚙️ environments/    # Configurations (dev/prod)



## ⚙️ Installation & Démarrage

### Prérequis
- Node.js `>=18`
- Angular CLI (`npm install -g @angular/cli`)

### Installation
```bash
npm install
````

### Lancement en mode développement

```bash
ng serve
```

👉 L’application est accessible sur `http://localhost:4200`

### Build production

```bash
ng build --configuration production
```

---

## 🌍 Internationalisation

Le projet utilise **ngx-translate**.
Les traductions sont disponibles dans :

* `assets/i18n/en.json`
* `assets/i18n/fr.json`
* `assets/i18n/es.json`
* `assets/i18n/pt.json`

---

## 🛡️ Sécurité et Permissions

* **Authentification** : gérée par `AuthInterceptor`.
* **Protection des routes** : `PermissionGuard`.
* **Permissions par route** définies via `data.permissions`.

Exemple :

```ts
{
  path: 'site',
  component: SiteComponent,
  canActivate: [PermissionGuard],
  data: { permissions: ['VIEW_SITES'] }
}
```

---

## 📦 Dépendances principales

* **PrimeNG** : composants UI (table, dialog, menu, etc.)
* **Google Maps** : affichage et gestion des trajets
* **ngx-translate** : traductions multi-langues
* **ngx-permissions** : gestion avancée des droits
* **ng-circle-progress** : affichage de graphiques circulaires

---

## 🖼️ Composants principaux

* `LoginComponent` : page de connexion
* `HomeComponent` : tableau de bord / accueil
* `SiteComponent` : gestion des sites
* `RouteSectionComponent` : gestion des trajets et secteurs
* `TransportCompanyComponent` : gestion des compagnies de transport
* `CollaboratorComponent` : gestion des collaborateurs
* `PlanificationComponent` : gestion et visualisation de la planification
* `MapComponent` : intégration Google Maps (trajets, secteurs, points de ramassage)

---

## 🔗 Services principaux

* `auth.service.ts` → Authentification & Tokens
* `site.service.ts` → Gestion des sites
* `trip.service.ts` → Gestion des trajets
* `planification.service.ts` → Gestion de la planification
* `google-map.service.ts` → Intégration Google Maps

---

## 🧩 Shared (Réutilisables)

* **NavbarComponent** : barre de navigation
* **SidebarComponent** : menu latéral
* **DialogComponent** : boîte de dialogue générique
* **Pipes** :

  * `FormatDayOnlyPipe` → formatage date (jour uniquement)
  * `FormatDayNamePipe` → formatage du nom du jour
  * `TimeFormatPipe` → formatage horaire
  * `FilterByShiftPipe` → filtre selon le shift

---

## 🌐 Environnements

* `environment.ts` → configuration par défaut
* `environment.dev.ts` → environnement développement
* `environment.prod.ts` → environnement production

---

## 👨‍💻 Développement & Contribution

1. Créer une branche à partir de `main`
2. Développer votre fonctionnalité ou correctif
3. Faire un **Merge Request** en respectant les conventions de commit

