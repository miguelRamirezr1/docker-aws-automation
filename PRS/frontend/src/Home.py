import streamlit as st

# Configuraci�n de la p�gina
st.set_page_config(
    page_title="Red Social - Home",
    page_icon="<�",
    layout="wide"
)

# T�tulo principal
st.title("<� Bienvenido a nuestra Red Social")

# Descripci�n
st.markdown("""
## Una plataforma para conectar personas

Esta es una aplicaci�n de red social construida con **Streamlit** y conectada a un backend FIWARE.

### Caracter�sticas principales:
- =� **Registro de usuarios**: Crea tu cuenta de forma r�pida y segura
- = **Login seguro**: Accede con tus credenciales
- =� **Muro social**: Comparte tus ideas y conecta con otros usuarios
- =� **Visualizaci�n de datos**: Integraci�n con Grafana para an�lisis

### Tecnolog�as utilizadas:
""")

# Columnas para mostrar tecnolog�as
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
    **An�lisis**
    - CrateDB
    - Grafana
    - Time Series Data
    """)

# Secci�n de navegaci�n
st.markdown("---")
st.markdown("### =� Comienza ahora")

col_left, col_center, col_right = st.columns(3)

with col_left:
    st.markdown("#### �Nuevo usuario?")
    st.markdown("Crea tu cuenta en segundos")
    if st.button("Ir a Registro", key="btn_registro"):
        st.info("=H Usa el men� lateral para ir a 'Registro'")

with col_center:
    st.markdown("#### �Ya tienes cuenta?")
    st.markdown("Inicia sesi�n para continuar")
    if st.button("Ir a Login", key="btn_login"):
        st.info("=H Usa el men� lateral para ir a 'Login'")

with col_right:
    st.markdown("#### �Explorar?")
    st.markdown("Conoce nuestra comunidad")
    if st.button("Ver Muro", key="btn_muro"):
        st.info("=H Usa el men� lateral para ir a 'Muro'")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Red Social Demo | Construido con Streamlit y FIWARE</p>
    <p>� 2024 - Todos los derechos reservados</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con informaci�n adicional
with st.sidebar:
    st.markdown("## 9 Informaci�n")
    st.markdown("""
    Esta es una aplicaci�n demo que muestra:
    - Autenticaci�n de usuarios
    - Gesti�n de contenido
    - Integraci�n con IoT platforms
    """)

    st.markdown("### =� Estado del sistema")

    # Simulaci�n de estado del sistema
    st.metric("Usuarios registrados", "1,234", "+12")
    st.metric("Posts en el muro", "5,678", "+89")
    st.metric("Conexiones activas", "456", "+23")

    st.markdown("---")
    st.markdown("### = Enlaces �tiles")
    st.markdown("- [Documentaci�n](https://streamlit.io)")
    st.markdown("- [FIWARE](https://www.fiware.org)")
    st.markdown("- [Soporte](mailto:support@example.com)")
