# Océana & Heiwa - Ecosistema de Bienestar (E-commerce)

Este proyecto es una plataforma de comercio electrónico avanzada desarrollada con **Django**, diseñada para gestionar un ecosistema de dos marcas distintas (**Océana** y **Heiwa**) bajo una única infraestructura técnica. Combina una experiencia de usuario premium con herramientas internas de vanguardia, como la integración de IA para asistencia en el desarrollo.

## 🚀 Propósito y Razonamiento

La arquitectura del proyecto nació de la necesidad de ofrecer dos identidades visuales y de producto diferentes (Biocosmética y Neurobotánica) sin duplicar el esfuerzo de gestión ni la base de datos. 

### Decisiones de Diseño Técnico:
- **Tematización Dinámica**: Implementación de un sistema de middleware que detecta la marca activa y swapea tokens de CSS y contenido en tiempo real.
- **Filtrado de Catálogo Basado en Marca**: Lógica personalizada en el ORM de Django para asegurar que los usuarios solo vean productos y categorías relevantes a la "tienda" en la que se encuentran.
- **Robustez en Producción**: Integración con **AWS SES** para el envío de correos transaccionales y **MercadoPago** para el procesamiento de pagos, garantizando una operación profesional.

## ✨ Características Principales

- **Multi-Tenant / Multi-Brand**: Una sola instalación de Django sirve a `oceana/` y `heiwa/` con estilos, manifiestos y catálogos diferenciados.
- **Diseño Mobile-First**: Cabeceras adaptativas, carritos de compra optimizados para pantallas táctiles y tipografía de alta legibilidad.
- **Gestión de Ofertas**: Sistema automático de detección de "Tesoros en Oferta" con banners dinámicos y categorías inteligentes.
- **Panel Administrativo Personalizado**: Interfaz para que el vendedor gestione stock, combos/kits y galería de imágenes de forma intuitiva.
- **🤖 Asistente de IA Interno**: Herramienta de línea de comandos integrada con **Google Gemini** para que los desarrolladores puedan realizar análisis de código y sugerencias de refactorización directamente sobre los archivos del proyecto.

## 🛠️ Stack Tecnológico

- **Backend**: Python / Django
- **Base de Datos**: PostgreSQL (Producción) / SQLite (Desarrollo)
- **Frontend**: HTML5, Vanilla CSS (Custom Properties), JavaScript
- **Email**: AWS SES (Simple Email Service)
- **IA**: Google AI Studio (Gemini 1.5/2.0 Flash)
- **Infraestructura**: Docker, Coolify

## 📦 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/GerardodeMartini/Tienda-Oceana.git
   ```
2. **Crear y activar entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/Scripts/activate  # Windows
   ```
3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar variables de entorno**:
   Crear un archivo `.env` basado en `.env.example` e incluir:
   - `SECRET_KEY`, `DEBUG`, `DB_NAME`, etc.
   - `GOOGLE_API_KEY` (para las herramientas de IA).
   - Credenciales de AWS y MercadoPago.

5. **Migrar y Correr**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## 🤖 Uso del Asistente de IA

El proyecto incluye una herramienta en `dev_tools/` para asistir en el desarrollo:

```bash
python dev_tools/ask_ai.py --file store/views.py "Optimiza esta consulta al ORM"
```

---
*Este proyecto es parte de mi portfolio personal, demostrando habilidades en desarrollo Fullstack, arquitectura de software y adopción de tecnologías de IA.*
