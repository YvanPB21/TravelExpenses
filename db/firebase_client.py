"""Helpers para inicializar y obtener recursos de Firebase Firestore."""
from __future__ import annotations

import os
import json
from dataclasses import dataclass
from typing import Optional

import firebase_admin
from firebase_admin import credentials, firestore


@dataclass
class FirebaseConfig:
    """Configuración de Firebase."""
    credentials_path: Optional[str] = None
    project_id: Optional[str] = None


_initialized = False


def initialize_firebase(config: FirebaseConfig | None = None):
    """Inicializa Firebase Admin SDK."""
    global _initialized

    if _initialized:
        return

    config = config or FirebaseConfig()

    # Opción 1: Credenciales desde variable de entorno JSON (FIREBASE_CREDENTIALS)
    # Útil para Render, Railway, etc. donde es más fácil copiar/pegar JSON
    firebase_creds_json = os.environ.get('FIREBASE_CREDENTIALS')
    if firebase_creds_json:
        try:
            creds_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred)
            print("🔥 Firebase inicializado desde variable FIREBASE_CREDENTIALS")
            _initialized = True
            return
        except json.JSONDecodeError as e:
            print(f"⚠️ Error: FIREBASE_CREDENTIALS no es JSON válido: {e}")

    # Opción 2: Credenciales desde archivo (ruta explícita en config)
    if config.credentials_path and os.path.exists(config.credentials_path):
        cred = credentials.Certificate(config.credentials_path)
        firebase_admin.initialize_app(cred)
        print(f"🔥 Firebase inicializado desde {config.credentials_path}")
        _initialized = True
        return

    # Opción 3: Emulador local (para desarrollo)
    if config.project_id:
        os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8080'
        firebase_admin.initialize_app(options={'projectId': config.project_id})
        print(f"🔥 Firebase inicializado con emulador (proyecto: {config.project_id})")
        _initialized = True
        return

    # Opción 4: GOOGLE_APPLICATION_CREDENTIALS (variable de entorno estándar)
    cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print(f"🔥 Firebase inicializado desde GOOGLE_APPLICATION_CREDENTIALS")
        _initialized = True
        return

    # Opción 5: Application Default Credentials (Cloud Run, GCP)
    try:
        firebase_admin.initialize_app()
        print("🔥 Firebase inicializado con Application Default Credentials")
        _initialized = True
    except Exception as e:
        print(f"\n❌ Error al inicializar Firebase: {e}")
        print("\n💡 Configura las credenciales de una de estas formas:")
        print("   1. Variable de entorno FIREBASE_CREDENTIALS con el JSON completo")
        print("   2. Variable de entorno GOOGLE_APPLICATION_CREDENTIALS con ruta al archivo")
        print("   3. Archivo firebase-credentials.json en el directorio del proyecto")
        raise


def get_firestore_client(config: FirebaseConfig | None = None):
    """Obtiene cliente de Firestore."""
    initialize_firebase(config)
    return firestore.client()


