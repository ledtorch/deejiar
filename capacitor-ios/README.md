# Deejiar App
This is Deejiar's user-facing front-end, developed using Vue 3.4 and Vite 5. It serves as the primary interface for users to interact with the map, accessible at deejiar.com.

## 🛠 Prerequisites
- Node.js
- Yarn
- Vite
- Vue3
- Mapbox token <a href="https://docs.mapbox.com/help/getting-started/access-tokens/">Tutorial</a>

```zsh
openssl req -x509 -newkey rsa:2048 -keyout localhost.key -out localhost.crt -days 365 -nodes
```

```zsh
yarn
```

```zsh
yarn dev
```

## Main Components
- Map.vue
  - BottomSheet.vue
- Details.vue
- Account.vue

### Map.vue
This component acts as the core of the application, enabling the main functionalities. It handles UI with the map, fetching stores data from a JSON file and passing this data to **BottomSheet**, which then displays the information about the selected store.

### BottomSheet.vue
A child component of **Map**, **BottomSheet** plays a role in providing users with a quick overview of store information. Dragging this component upwards leads users to a detailed page for the store, rendered by **Details**.

### Details.vue
This component fetches store data directly from a JSON file by decoding the URL. It ensures that store pages are directly accessible, maintaining functionality even when users do not navigate through clicking on the map but rather enter a URL or directly access a store's detail page.

### Account.vue
This page allows users to manage their settings and provides contact information for the author, along with links to related social media profiles.

```regexp
feat|fix|docs|dx|style|refactor|perf|test|workflow|build|ci|chore|types|wip
```