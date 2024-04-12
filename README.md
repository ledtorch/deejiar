Deejair, aimed at assisting users in locating stores and places via a map interface. The product is composed of 3 main elements and 1 data directory:

- 'App': This is Deejair's user-facing front end, created with Vue 3.4 and Vite 5.2 It serves as the main interface for users to interact with the map and is accessible at deejiar.com.
- 'Datacenter': Also built with Vue 3.4 and Vite 5, this application provides a front-end UI for administrative tasks and management of the backend. It's available at deejiar.com/admin.
- 'Flask': This is the server-side component, developed with Python3 and Flask framework, using a PostgreSQL database. It handles the server logic and database operations for both the 'App' and the 'Datacenter'.
- 'Data directory': The directory that stores static files like stores.json

The entire system is set up on an Ubuntu 22.04.2 LTS server.
