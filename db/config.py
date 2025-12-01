"""Configuración de optimización para Firebase Firestore."""
import os

# Configuración de caché
ENABLE_CACHE = os.getenv('FIRESTORE_ENABLE_CACHE', 'true').lower() == 'true'
CACHE_TTL_SECONDS = int(os.getenv('FIRESTORE_CACHE_TTL', '5'))  # 5 segundos por defecto

# Configuración de batch operations
BATCH_SIZE = 500  # Máximo permitido por Firestore

# Configuración de timeout
READ_TIMEOUT = int(os.getenv('FIRESTORE_READ_TIMEOUT', '10'))  # 10 segundos
WRITE_TIMEOUT = int(os.getenv('FIRESTORE_WRITE_TIMEOUT', '10'))  # 10 segundos

# Modo debug
DEBUG_FIRESTORE = os.getenv('DEBUG_FIRESTORE', 'false').lower() == 'true'

