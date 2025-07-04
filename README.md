# Planazos Bot

Bot de Telegram para gestionar planes personales y de amigos.  
Permite añadir, listar y borrar planes por fecha.

## Comandos disponibles

- `/anadir DD/MM/YYYY descripción` - Añadir un plan nuevo.  
- `/proximos` - Mostrar planes futuros.  
- `/pasados [años]` - Mostrar planes pasados (por defecto 1 año).  
- `/delete DD/MM/YYYY` - Borrar un plan de una fecha específica.  
- `/help` - Mostrar ayuda.

## Configuración

- Añadir tu token de Telegram en `config.py`.  
- Lista de usuarios permitidos en `config.py`.

## Uso

1. Clona este repositorio.  
2. Instala las dependencias:  
   ```bash
   pip install python-telegram-bot --upgrade
