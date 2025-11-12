#!/usr/bin/env bash

# Exportar el puerto proporcionado por Render
export PORT=${PORT:-5000}

# Iniciar el servidor Flask
python server.py