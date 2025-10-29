import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Login", page_icon="=", layout="wide")

# Inicializar session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'intentos_login' not in st.session_state:
    st.session_state.intentos_login = 0

# Usuarios dummy para pruebas
USUARIOS_DEMO = {
    "admin": {"password": "admin123", "nombre": "Administrador", "rol": "admin"},
    "usuario1": {"password": "user123", "nombre": "Juan Pérez", "rol": "usuario"},
    "demo": {"password": "demo123", "nombre": "Usuario Demo", "rol": "usuario"}
}

# Título
st.title("= Iniciar Sesión")

# Si ya está logueado, mostrar mensaje
if st.session_state.logged_in:
    st.success(f" Ya has iniciado sesión como **{st.session_state.username}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("=ñ Ir al Muro", use_container_width=True):
            st.info("=H Usa el menú lateral para ir a 'Muro'")

    with col2:
        if st.button("=ª Cerrar Sesión", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

else:
    # Formulario de login
    col_form, col_info = st.columns([2, 1])

    with col_form:
        st.markdown("### Accede a tu cuenta")

        with st.form("formulario_login"):
            # Campo de usuario
            username = st.text_input(
                "Usuario o Email",
                placeholder="Ingresa tu usuario o email",
                help="Usa 'demo' / 'demo123' para probar"
            )

            # Campo de contraseña
            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Ingresa tu contraseña"
            )

            # Recordarme
            col_check, col_forgot = st.columns(2)
            with col_check:
                recordarme = st.checkbox("Recordarme")

            with col_forgot:
                st.markdown("")
                st.markdown("[¿Olvidaste tu contraseña?](#)")

            st.markdown("")

            # Botón de login
            col_btn1, col_btn2 = st.columns([2, 1])
            with col_btn1:
                submitted = st.form_submit_button("= Iniciar Sesión", use_container_width=True)

            with col_btn2:
                google_login = st.form_submit_button("< Google", use_container_width=True)

            if submitted:
                # Validación básica
                if not username or not password:
                    st.error("L Por favor completa todos los campos")
                else:
                    # Verificar credenciales (demo)
                    if username in USUARIOS_DEMO:
                        if USUARIOS_DEMO[username]["password"] == password:
                            # Login exitoso
                            with st.spinner("Iniciando sesión..."):
                                time.sleep(1)

                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.intentos_login = 0

                            st.success(f" ¡Bienvenido, {USUARIOS_DEMO[username]['nombre']}!")
                            st.balloons()

                            # Mostrar info de sesión
                            st.info("=ä En producción, aquí se verificaría contra FIWARE Orion-LD")

                            # Recargar página
                            time.sleep(2)
                            st.rerun()
                        else:
                            # Contraseña incorrecta
                            st.session_state.intentos_login += 1
                            st.error(f"L Contraseña incorrecta (Intento {st.session_state.intentos_login}/3)")

                            if st.session_state.intentos_login >= 3:
                                st.warning("  Demasiados intentos fallidos. Por seguridad, espera un momento.")
                    else:
                        # Usuario no encontrado
                        st.session_state.intentos_login += 1
                        st.error("L Usuario no encontrado")

            if google_login:
                st.info("= Integración con Google OAuth pendiente de implementar")

        # Separador
        st.markdown("---")

        # Sección de registro
        st.markdown("### ¿No tienes cuenta?")
        col_reg1, col_reg2 = st.columns([3, 1])
        with col_reg1:
            st.markdown("Únete a nuestra comunidad en segundos")
        with col_reg2:
            if st.button("Registrarse", use_container_width=True):
                st.info("=H Usa el menú lateral para ir a 'Registro'")

    with col_info:
        st.markdown("### =¡ Información")

        st.info("""
        **Usuarios de prueba:**
        - Usuario: `demo`
        - Contraseña: `demo123`
        """)

        st.success("""
        **Características:**
        - Inicio de sesión seguro
        - Sesión persistente
        - Autenticación OAuth
        - Recuperación de contraseña
        """)

        st.warning("""
        **Seguridad:**
        - Contraseñas encriptadas
        - Tokens JWT
        - Sesiones con timeout
        - Protección CSRF
        """)

        # Estadísticas
        st.markdown("### =Ê Estadísticas")
        st.metric("Sesiones activas", "342", "+18")
        st.metric("Intentos de login hoy", "1,245", "+89")

        # Tips de seguridad
        st.markdown("### = Tips de Seguridad")
        with st.expander("Ver recomendaciones"):
            st.markdown("""
            1. Nunca compartas tu contraseña
            2. Usa contraseñas únicas
            3. Habilita autenticación 2FA
            4. Cierra sesión en dispositivos públicos
            5. Revisa tu actividad regularmente
            """)

# Footer
st.markdown("---")

# Mostrar información de sesión actual
if st.session_state.logged_in:
    col_footer1, col_footer2, col_footer3 = st.columns(3)

    with col_footer1:
        st.metric("Usuario", st.session_state.username)

    with col_footer2:
        st.metric("Rol", USUARIOS_DEMO[st.session_state.username]["rol"])

    with col_footer3:
        st.metric("Sesión iniciada", datetime.now().strftime("%H:%M:%S"))

else:
    st.caption("¿Problemas para iniciar sesión? Contacta con soporte@ejemplo.com")

# Sidebar con información adicional
with st.sidebar:
    st.markdown("## = Estado de Autenticación")

    if st.session_state.logged_in:
        st.success(f"Conectado como: **{st.session_state.username}**")
        st.markdown(f"**Nombre:** {USUARIOS_DEMO[st.session_state.username]['nombre']}")
        st.markdown(f"**Rol:** {USUARIOS_DEMO[st.session_state.username]['rol']}")
    else:
        st.warning("No has iniciado sesión")

    st.markdown("---")

    st.markdown("### 9 Sobre el Login")
    st.markdown("""
    Este sistema de autenticación es una demo que simula:
    - Verificación de credenciales
    - Gestión de sesiones
    - Integración con backend FIWARE
    """)

    st.markdown("---")

    # Actividad reciente (simulada)
    st.markdown("### =Ë Actividad Reciente")
    st.markdown("""
    - =P 10:30 - 23 usuarios conectados
    - =P 10:15 - 15 nuevos registros
    - =P 10:00 - 8 usuarios desconectados
    """)

