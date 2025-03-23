
# Elo Race

Elo Race es un proyecto que combina una API desarrollada con FastAPI y un bot de Discord para gestionar carreras de Elo en juegos. Los usuarios pueden registrarse, unirse a carreras y ver tablas de clasificación directamente desde Discord.

## Estructura

```
EloRace/
├── elorace/                # FAST API LAYER package
│   ├── __init__.py
│   ├── routers/            #
│   │   ├── __init__.py     #
│   │   ├── player.py       #
│   │   ├── races.py        #
│   │   └── summoner.py     #
│   ├── models.py           #
│   ├── database.py         #
│   ├── logger_config.py    #
│   └── main.py             #
├── discord_layer/          # DISCORD LAYER package
│   ├── __init__.py
│   ├── cogs/               # Comandos organizados por categorías
│   │   ├── __init__.py
│   │   ├── race.py         # Comandos relacionados con carreras
│   │   ├── player.py       # Comandos para gestionar jugadores
│   │   ├── summoner.py     # Comandos para gestionar invocadores
│   ├── views/              # Componentes interactivos de Discord
│   │   ├── __init__.py
│   │   ├── embeds.py       # Creación de embeds para respuestas
│   ├── events/             # Manejadores de eventos
│   │   ├── __init__.py
│   ├── config.py           # Configuración específica de Discord
│   └── main.py             # Punto de entrada del bot
├── riot_api/               # RIOT API package
│   ├── __init__.py         #
│   ├── riot_client.py      #
│   └── summoner.py         #
├── logs/                   #
│   └── elorace_20250309.log
├── .env                    #
├── .gitignore              #
├── elo_race.db             #
├── poetry.lock             #
├── pyproject.toml          #
└── README.md               #
```

## Instalación

1. Clona el repositorio:

   ```sh
   git clone https://github.com/tu_usuario/elo-race.git
   cd elo-race
   ```
2. Instala las dependencias usando Poetry:

   ```sh
   poetry install
   ```
3. Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:

   ```
   DISCORDAPITOKEN=tu_token_de_discord
   APPLICATION_ID=tu_application_id
   RIOTAPITOKEN=tu_token_de_riot
   ```
4. Inicia el servidor FastAPI:

   ```sh
   poetry run uvicorn elorace.main:app --reload
   ```
5. Inicia el bot de Discord:

   ```sh
   poetry run python discord_layer/main.py
   ```

## Uso

### Comandos de Discord

- `/join`: Regístrate como jugador.
- `/new_summoner`: Registra un nuevo invocador.
- `/new_race`: Registra una nueva carrera.
- `/join_race`: Únete a una carrera.
- `/leave_race`: Deja una carrera.
- `/leaderboard`: Muestra la tabla de clasificación.

### Endpoints de la API

- `POST /summoner/register`: Registra un nuevo invocador.
- `POST /summoner/current_elo`: Actualiza el ELO actual de un invocador.
- `POST /summoner/update`: Actualiza la información de un invocador.
- `POST /player/register`: Registra un nuevo jugador.
- `POST /race/create`: Crea una nueva carrera.
- `POST /race/update`: Actualiza la información de una carrera.
- `GET /race`: Obtiene una lista de carreras.
- `GET /race/{race_id}`: Obtiene la información de una carrera específica.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
