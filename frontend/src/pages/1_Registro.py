import streamlit as st
import re
from datetime import datetime

st.set_page_config(page_title="Registro", layout="wide")

# Título
st.title("Registro de Usuario")
st.markdown("Crea tu cuenta para unirte a nuestra comunidad")

# Inicializar session state para mensajes
if 'registro_exitoso' not in st.session_state:
    st.session_state.registro_exitoso = False

# Crear dos columnas
col1, col2 = st.columns([2, 1])

with col1:
    # Formulario de registro
    with st.form("formulario_registro"):
        st.markdown("### Información Personal")

        # Nombre completo
        nombre_completo = st.text_input(
            "Nombre Completo *",
            placeholder="Juan Pérez"
        )

        # Email
        email = st.text_input(
            "Correo Electrónico *",
            placeholder="usuario@ejemplo.com"
        )

        # Usuario
        username = st.text_input(
            "Nombre de Usuario *",
            placeholder="usuario123",
            help="Solo letras, números y guiones bajos"
        )

        # Contraseña
        col_pass1, col_pass2 = st.columns(2)
        with col_pass1:
            password = st.text_input(
                "Contraseña *",
                type="password",
                placeholder="Mínimo 8 caracteres"
            )

        with col_pass2:
            password_confirm = st.text_input(
                "Confirmar Contraseña *",
                type="password",
                placeholder="Repite tu contraseña"
            )

        st.markdown("### Información Adicional")

        # Fecha de nacimiento
        fecha_nacimiento = st.date_input(
            "Fecha de Nacimiento",
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now()
        )

        # País
        pais = st.selectbox(
            "País",
            ["Seleccionar...", "España", "México", "Argentina", "Colombia", "Chile", "Perú", "Otro"]
        )

        # Género
        genero = st.radio(
            "Género",
            ["Prefiero no decirlo", "Masculino", "Femenino", "Otro"],
            horizontal=True
        )

        # Intereses
        st.markdown("### Intereses")
        col_int1, col_int2 = st.columns(2)

        with col_int1:
            tecnologia = st.checkbox("Tecnología")
            deportes = st.checkbox("Deportes")
            musica = st.checkbox("Música")

        with col_int2:
            arte = st.checkbox("Arte")
            viajes = st.checkbox("Viajes")
            gastronomia = st.checkbox("Gastronomía")

        # Biografía
        bio = st.text_area(
            "Biografía",
            placeholder="Cuéntanos algo sobre ti... (Opcional)",
            max_chars=500,
            height=100
        )

        # Términos y condiciones
        st.markdown("---")
        terminos = st.checkbox("Acepto los términos y condiciones *")
        newsletter = st.checkbox("Quiero recibir novedades por email")

        # Botón de submit
        st.markdown("")
        submitted = st.form_submit_button("Crear Cuenta", use_container_width=True)

        if submitted:
            # Validaciones
            errores = []

            if not nombre_completo:
                errores.append("El nombre completo es requerido")

            if not email:
                errores.append("El email es requerido")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errores.append("El formato del email no es válido")

            if not username:
                errores.append("El nombre de usuario es requerido")
            elif not re.match(r"^[a-zA-Z0-9_]+$", username):
                errores.append("El nombre de usuario solo puede contener letras, números y guiones bajos")

            if not password:
                errores.append("La contraseña es requerida")
            elif len(password) < 8:
                errores.append("La contraseña debe tener al menos 8 caracteres")

            if password != password_confirm:
                errores.append("Las contraseñas no coinciden")

            if not terminos:
                errores.append("Debes aceptar los términos y condiciones")

            # Mostrar errores o éxito
            if errores:
                for error in errores:
                    st.error(f"{error}")
            else:
                st.success("¡Registro exitoso! Bienvenido a la comunidad")
                st.balloons()
                st.session_state.registro_exitoso = True

                # Aquí iría la lógica para guardar en la base de datos
                st.info("En producción, aquí se enviarían los datos a FIWARE Orion-LD")

                # Mostrar resumen de datos (simulación)
                with st.expander("Ver resumen de datos"):
                    st.json({
                        "nombre": nombre_completo,
                        "email": email,
                        "username": username,
                        "pais": pais,
                        "fecha_nacimiento": str(fecha_nacimiento),
                        "genero": genero,
                        "intereses": {
                            "tecnologia": tecnologia,
                            "deportes": deportes,
                            "musica": musica,
                            "arte": arte,
                            "viajes": viajes,
                            "gastronomia": gastronomia
                        },
                        "newsletter": newsletter,
                        "fecha_registro": datetime.now().isoformat()
                    })

with col2:
    st.markdown("### Consejos")
    st.info("""
    **Contraseña segura:**
    - Mínimo 8 caracteres
    - Incluye mayúsculas y minúsculas
    - Usa números y símbolos
    - Evita palabras comunes
    """)

    st.success("""
    **Privacidad:**
    - Tus datos están seguros
    - No compartimos información
    - Puedes eliminar tu cuenta cuando quieras
    """)

    st.warning("""
    **Beneficios:**
    - Perfil personalizado
    - Conexión con amigos
    - Contenido relevante
    - Notificaciones en tiempo real
    """)

# Sección de ayuda
st.markdown("---")
st.markdown("### ¿Ya tienes cuenta?")
col_help1, col_help2 = st.columns([3, 1])
with col_help1:
    st.markdown("Si ya tienes una cuenta, puedes iniciar sesión")
with col_help2:
    if st.button("Ir a Login", use_container_width=True):
        st.info("Usa el menú lateral para ir a 'Login'")

# Footer
st.markdown("---")
st.caption("* Campos obligatorios")

