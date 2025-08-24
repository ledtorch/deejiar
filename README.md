# Deejiar
Deejiar is a connection-driven map designed to help travelers explore places through the comments from their friends or influencers, instead of aimlessly searching. The platform is comprised of three main components and a data directory, each tailored to enhance user and administrative experiences.

## capacitor-ios
> Vue 3.5 and Vite 7.1.2
This is Deejiar's user-facing front-end, created with Vue 3.5 and Vite 7.1.2. It serves as the main interface for users to interact with the map and is accessible at deejiar.com and converted to iOS app through Capacitor 7.

## datacenter
> Vue 3.5 and Vite 7.1.2
This application provides a front-end UI for administrative tasks and management of the back-end. It's available at deejiar.com/admin.

## api
> This is the server-side component, developed with Python3 and FastAPI, using a PostgreSQL database. It handles the server logic and database operations for both the 'capacitor-ios' and the 'datacenter'.

## Server
The entire system is set up on an Ubuntu 22.04.2 LTS server with Nginx 1.18.

### Git Commit Message Convention
> This is adapted from [Vue's commit convention](https://github.com/vuejs/core/blob/main/.github/commit-convention.md).
All commits should be matched by the following regex:
```regexp
feat|fix|docs|dx|style|ui|refact|perf|test|workflow|build|ci|chore|types|wip
```

## License
Copyright (c) 2023-present, Jerry