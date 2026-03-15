# Océana & Heiwa: Arquitectura Multi-Marca de Alto Rendimiento

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Este ecosistema digital representa una solución **Fullstack robusta**, diseñada para gestionar dos marcas de bienestar de alta gama bajo una infraestructura unificada. El proyecto no solo resuelve la complejidad de la coexistencia de identidades visuales contrapuestas, sino que integra flujos de **Developer Experience (DX)** potenciados por Inteligencia Artificial para optimizar el ciclo de vida del desarrollo.

---

## 🏗️ Desafíos Arquitectónicos y Soluciones

### 1. Sistema de Tematización Dinámica (Middleware-Based)
A diferencia de las soluciones tradicionales basadas en lógica de plantillas pesadas, este proyecto utiliza un **Middleware de Marca personalizado**. 
- **Razonamiento**: Desacoplar la lógica de presentación del flujo de las vistas. El middleware intercepta cada request, inyecta el contexto de marca en la sesión y conmuta dinámicamente el `data-theme` en el DOM, permitiendo una transición fluida entre **Océana** y **Heiwa** sin recargas de configuración pesada.

### 2. Multi-Tenant Lógico en Catálogo
Se implementó un filtrado a nivel de **ORM (Querysets)** que garantiza el aislamiento de datos entre marcas.
- **Resultado**: Los usuarios solo interactúan con el stock y las categorías correspondientes a su contexto actual, optimizando el rendimiento mediante consultas `distinct()` y precarga selectiva de relaciones.

### 3. Developer Experience (DX) & AI Productivity
Para acelerar la iteración técnica, se integró un **asistente de IA interno** basado en la API de **Google Gemini**.
- **Impacto**: Reducción del tiempo de refactorización y auditoría de código complejo. El asistente tiene acceso al contexto de los archivos locales, permitiendo una depuración asistida por IA directamente desde la terminal del desarrollador.

---

## 🛠️ Stack Tecnológico

### Core Engine
- **Backend**: Python 3.10+ / Django (Arquitectura MVT)
- **Base de Datos**: PostgreSQL (Escalabilidad en Producción) / SQLite (Desarrollo Ágil)
- **Process Manager**: Docker & Coolify para despliegue continuo (CI/CD)

### Integraciones de Terceros
- **Pagos**: MercadoPago SDK (Checkouts seguros y flujos de webhook)
- **Email**: AWS SES vía Django-Anymail (Entregabilidad de alta reputación)
- **IA**: Google AI Studio (Gemini 2.0 Flash / 1.5 Pro)

### Frontend & UX
- **Styling**: Vanilla CSS con Arquitectura de Variables (Custom Properties) para tematización atómica.
- **UI/UX**: Responsive Design estricto, optimización de assets y micro-animaciones para una sensación premium.

---

## 🔧 Guía de Instalación Profesional

Este proyecto requiere Python 3.10 o superior. Siga estos pasos para replicar el entorno de desarrollo:

### 1. Preparación del Entorno
```bash
# Clonar con submódulos si aplica
git clone https://github.com/GerardodeMartini/Tienda-Oceana.git
cd tienda-oceana

# Aislamiento de dependencias
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/macOS
```

### 2. Gestión de Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configuración de Entorno
Cree un archivo `.env` en la raíz (ver `.env.example` para referencia):
```env
DEBUG=True
SECRET_KEY=tu_clave_secreta
DB_NAME=oceana_db
# Integraciones
GOOGLE_API_KEY=tu_key_de_gemini
AWS_ACCESS_KEY_ID=tu_aws_key
MERCADOPAGO_ACCESS_TOKEN=tu_token
```

### 4. Inicialización de la Base de Datos
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Para acceder al panel /admin
```

### 5. Lanzamiento del Servidor
```bash
python manage.py runserver
```

---

## 🤖 Uso de la Tool de Productividad (AI Assistant)

El script de asistencia interna está localizado en `dev_tools/`. Úselo para auditar cualquier archivo del sistema:

```bash
# Ejemplo de análisis de lógica de negocio
python dev_tools/ask_ai.py --file store/views.py "Analiza la eficiencia de la función product_list"
```

---

**Gerardo de Martini** - *Fullstack Developer enfocado en soluciones escalables y experiencias de usuario de alto impacto.*
