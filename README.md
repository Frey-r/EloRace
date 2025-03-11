## Estructura

```
EloRace/
├── elorace/				#
│   ├── init.py
│   ├── routers/			#
│   │   ├── init.py			#
│   │   ├── player			#
│   │   ├── races.py			#
│   │   └── summoner.py			#
│   ├── models.py			#
│   ├── database.py			#
│   ├── logger_config.py		#
│   └── main.py				#
├── discord/				#
│   ├── __init__.py
│   ├── cogs/                   	# Comandos organizados por categorías
│   │   ├── __init__.py
│   │   ├── race_commands.py    	# Comandos relacionados con carreras
│   │   ├── player_commands.py  	# Comandos para gestionar jugadores
│   │   ├── admin_commands.py   	# Comandos administrativos
│   │   └── utils_commands.py   	# Comandos de utilidad
│   ├── utils/                  	# Utilidades para el bot
│   │   ├── __init__.py
│   │   ├── embeds.py           	# Creación de embeds para respuestas
│   │   ├── validators.py       	# Validación de entradas de usuario
│   │   └── formatters.py       	# Formateo de mensajes
│   ├── views/                  	# Componentes interactivos de Discord
│   │   ├── __init__.py
│   │   ├── race_views.py      		# Botones/menús para carreras
│   │   └── leaderboard_views.py 	# Vistas para tablas de clasificación
│   ├── events/                 	# Manejadores de eventos
│   │   ├── __init__.py
│   │   ├── on_message.py  		#
│   │   └── on_reaction.py		#
│   ├── config.py               	# Configuración específica de Discord
│   └── main.py                 	# Punto de entrada del bot
├── riot_api
│   ├── __init__.py			#
│   ├── riot_client.py			#
│   └── summoner.py			#
├── logs/				#
│   └── elorace_20250309.log
├── .env				#
├── .gitignore				#
├── elo_race.db				#
├── poetry.lock				#
├── pyproject.toml			#
└── README.md				#

```
