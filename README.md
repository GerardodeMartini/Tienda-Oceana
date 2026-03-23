# Océana & Heiwa: Arquitectura Multi-Marca de Alto Rendimiento

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Este ecosistema digital es una plataforma de reclutamiento y comercio electrónico **Fullstack**, diseñada para gestionar dos marcas de bienestar de alta gama (**Océana** y **Heiwa**) bajo una infraestructura técnica unificada. El proyecto destaca por su sistema de tematización dinámica, su arquitectura de roles y una interfaz de usuario premium optimizada para dispositivos móviles.

---

## 👥 Sistema de Roles de Usuario

La plataforma expande su funcionalidad de tienda con un sistema de reclutamiento integrado:

1.  **Candidato**: Usuarios que pueden explorar oportunidades y postularse a empleos dentro del ecosistema de las marcas.
2.  **Empresa**: Entidades que pueden ofrecer puestos de trabajo y gestionar vacantes.
3.  **Staff**: Administradores que gestionan la plataforma, supervisan trabajos y postulaciones, garantizando la integridad del sistema.

---

## ✨ Funcionalidades UI/UX Premium (Recientes)

Se ha priorizado una estética de alto impacto y una legibilidad superior:

-   **Carrusel de Manifiesto Inmersivo**: Un sistema de fondo dinámico que ocupa el ancho completo (`100vw`) con una relación de aspecto `16:9` (ajustable a vertical en móviles) para mostrar la esencia de cada marca sin comprometer la lectura.
-   **Header Rediseñado**: Rediseño integral de la cabecera con efecto *glassmorphism*, logotipos de mayor escala y una jerarquía visual clara que separa las acciones de usuario (Hola, Carrito) de la gestión administrativa.
-   **Optimización Móvil Extrema**: Auditoría y corrección de comportamientos responsivos, incluyendo el apilamiento inteligente del header y la prevención de solapamientos de texto en el carrusel mediante alturas mínimas dinámicas.
-   **Sistema de Notificaciones Moderno**: Plantillas de correo electrónico rediseñadas para alertas de stock bajo y estados de pedido, manteniendo la coherencia visual con la marca.

---

## 🏗️ Desafíos Arquitectónicos y Soluciones

### 1. Sistema de Tematización Dinámica (Middleware-Based)
A diferencia de las soluciones convencionales, utilizamos un **Middleware de Marca** personalizado:
-   Intercepta cada request para inyectar el contexto de la marca activa.
-   Conmuta dinámicamente variables CSS y el `data-theme` en el DOM.
-   Permite transiciones instantáneas entre **Océana** y **Heiwa**.

### 2. Multi-Tenant Lógico
Filtrado avanzado a nivel de **ORM (Django Querysets)** que garantiza que el stock, las categorías y los manifiestos correspondan estrictamente a la marca que el usuario está visualizando.

---

## 🛠️ Stack Tecnológico

### Backend & Core
-   **Lenguaje**: Python 3.10+
-   **Framework**: Django 4.2+ (Arquitectura MVT)
-   **Base de Datos**: PostgreSQL / SQLite
-   **Emails**: AWS SES / Django-Anymail

### Frontend
-   **Estilos**: Vanilla CSS con Arquitectura de Variables (Custom Properties) Atómicas.
-   **UX**: Diseño Responsive estricto, Micro-animaciones y Optimizaciones de Rendimiento.

---

## 🔧 Instalación y Configuración

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/GerardodeMartini/Tienda-Oceana.git
cd tienda-oceana

# 2. Entorno virtual
python -m venv venv
source venv/Scripts/activate  # Windows

# 3. Dependencias
pip install -r requirements.txt

# 4. Migraciones y Superusuario
python manage.py migrate
python manage.py createsuperuser

# 5. Ejecutar
python manage.py runserver
```

---

**Desarrollado por [Gerardo de Martini](https://github.com/GerardodeMartini)** - *Enfocado en soluciones Fullstack escalables y experiencias de usuario de alto impacto.*
