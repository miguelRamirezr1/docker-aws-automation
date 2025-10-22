import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Red Social - Home",
    page_icon="<à",
    layout="wide"
)

# Título principal
st.title("<à Bienvenido a nuestra Red Social")

# Descripción
st.markdown("""
## Una plataforma para conectar personas

Esta es una aplicación de red social construida con **Streamlit** y conectada a un backend FIWARE.

### Características principales:
- =Ý **Registro de usuarios**: Crea tu cuenta de forma rápida y segura
- = **Login seguro**: Accede con tus credenciales
- =ñ **Muro social**: Comparte tus ideas y conecta con otros usuarios
- =Ê **Visualización de datos**: Integración con Grafana para análisis

### Tecnologías utilizadas:
""")

# Columnas para mostrar tecnologías
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **Frontend**
    - Streamlit
    - Python 3
    - Docker
    """)

with col2:
    st.success("""
    **Backend**
    - FIWARE Orion-LD
    - QuantumLeap
    - MongoDB
    """)

with col3:
    st.warning("""
    **Análisis**
    - CrateDB
    - Grafana
    - Time Series Data
    """)

# Sección de navegación
st.markdown("---")
st.markdown("### =€ Comienza ahora")

col_left, col_center, col_right = st.columns(3)

with col_left:
    st.markdown("#### ¿Nuevo usuario?")
    st.markdown("Crea tu cuenta en segundos")
    if st.button("Ir a Registro", key="btn_registro"):
        st.info("=H Usa el menú lateral para ir a 'Registro'")

with col_center:
    st.markdown("#### ¿Ya tienes cuenta?")
    st.markdown("Inicia sesión para continuar")
    if st.button("Ir a Login", key="btn_login"):
        st.info("=H Usa el menú lateral para ir a 'Login'")

with col_right:
    st.markdown("#### ¿Explorar?")
    st.markdown("Conoce nuestra comunidad")
    if st.button("Ver Muro", key="btn_muro"):
        st.info("=H Usa el menú lateral para ir a 'Muro'")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Red Social Demo | Construido con Streamlit y FIWARE</p>
    <p>© 2024 - Todos los derechos reservados</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con información adicional
with st.sidebar:
    st.markdown("## 9 Información")
    st.markdown("""
    Esta es una aplicación demo que muestra:
    - Autenticación de usuarios
    - Gestión de contenido
    - Integración con IoT platforms
    """)

    st.markdown("### =Ê Estado del sistema")

    # Simulación de estado del sistema
    st.metric("Usuarios registrados", "1,234", "+12")
    st.metric("Posts en el muro", "5,678", "+89")
    st.metric("Conexiones activas", "456", "+23")

    st.markdown("---")
    st.markdown("### = Enlaces útiles")
    st.markdown("- [Documentación](https://streamlit.io)")
    st.markdown("- [FIWARE](https://www.fiware.org)")
    st.markdown("- [Soporte](mailto:support@example.com)")
