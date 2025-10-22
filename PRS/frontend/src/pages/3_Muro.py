import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Muro Social", page_icon="📱", layout="wide")

# Inicializar session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'posts' not in st.session_state:
    # Posts dummy iniciales
    st.session_state.posts = [
        {
            "id": 1,
            "autor": "María García",
            "username": "@maria_g",
            "avatar": "👩‍💼",
            "contenido": "¡Increíble conferencia sobre IoT y FIWARE! Aprendí mucho sobre Context Brokers y cómo gestionar datos en tiempo real. #FIWARE #IoT",
            "imagen": None,
            "timestamp": datetime.now() - timedelta(hours=2),
            "likes": 24,
            "comentarios": 5,
            "compartidos": 3
        },
        {
            "id": 2,
            "autor": "Carlos Ruiz",
            "username": "@carlos_dev",
            "avatar": "👨‍💻",
            "contenido": "Acabo de terminar mi proyecto con Streamlit y Docker. La integración fue sorprendentemente fácil. ¿Alguien más trabajando con esta stack?",
            "imagen": None,
            "timestamp": datetime.now() - timedelta(hours=5),
            "likes": 18,
            "comentarios": 8,
            "compartidos": 2
        },
        {
            "id": 3,
            "autor": "Ana Martínez",
            "username": "@ana_data",
            "avatar": "👩‍🔬",
            "contenido": "Visualizando datos de sensores IoT en Grafana. Los dashboards en tiempo real son simplemente impresionantes. 📊📈",
            "imagen": None,
            "timestamp": datetime.now() - timedelta(hours=8),
            "likes": 31,
            "comentarios": 12,
            "compartidos": 7
        },
        {
            "id": 4,
            "autor": "Luis Torres",
            "username": "@luis_cloud",
            "avatar": "👨‍🎓",
            "contenido": "Tutorial nuevo en mi blog: 'Cómo desplegar aplicaciones Python en AWS con Docker'. Link en bio. #AWS #Docker #Python",
            "imagen": None,
            "timestamp": datetime.now() - timedelta(hours=12),
            "likes": 45,
            "comentarios": 15,
            "compartidos": 18
        },
        {
            "id": 5,
            "autor": "Sofia Jiménez",
            "username": "@sofia_tech",
            "avatar": "👩‍🚀",
            "contenido": "Comparando MongoDB vs CrateDB para proyectos IoT. Ambas son excelentes, pero CrateDB brilla en time-series data. ¿Opiniones?",
            "imagen": None,
            "timestamp": datetime.now() - timedelta(hours=18),
            "likes": 27,
            "comentarios": 22,
            "compartidos": 5
        }
    ]

if 'nuevo_post' not in st.session_state:
    st.session_state.nuevo_post = ""

# Título
st.title("📱 Muro Social")

# Verificar si está logueado
if not st.session_state.logged_in:
    st.warning("⚠️ Debes iniciar sesión para ver y publicar en el muro")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Ir a Login", use_container_width=True):
            st.info("👈 Usa el menú lateral para ir a 'Login'")
    with col2:
        if st.button("📝 Registrarse", use_container_width=True):
            st.info("👈 Usa el menú lateral para ir a 'Registro'")

else:
    # Layout principal
    col_main, col_sidebar = st.columns([2, 1])

    with col_main:
        # Crear nuevo post
        st.markdown("### ✍️ ¿Qué estás pensando?")

        with st.form("nuevo_post_form", clear_on_submit=True):
            contenido_post = st.text_area(
                "",
                placeholder="Comparte tus ideas, proyectos o descubrimientos...",
                height=100,
                max_chars=500
            )

            col_form1, col_form2, col_form3 = st.columns([2, 1, 1])

            with col_form1:
                emoji_seleccionado = st.selectbox(
                    "Añadir emoji",
                    ["Sin emoji", "😊", "🎉", "💡", "🚀", "❤️", "👍", "🔥", "💻", "📊"]
                )

            with col_form2:
                st.markdown("")
                st.markdown("")
                incluir_imagen = st.checkbox("Imagen")

            with col_form3:
                st.markdown("")
                st.markdown("")
                publicar = st.form_submit_button("📤 Publicar", use_container_width=True)

            if publicar and contenido_post:
                # Crear nuevo post
                if emoji_seleccionado != "Sin emoji":
                    contenido_post = f"{contenido_post} {emoji_seleccionado}"

                nuevo_post = {
                    "id": len(st.session_state.posts) + 1,
                    "autor": st.session_state.get('username', 'Usuario'),
                    "username": f"@{st.session_state.get('username', 'user')}",
                    "avatar": "🙂",
                    "contenido": contenido_post,
                    "imagen": "🖼️ Imagen de ejemplo" if incluir_imagen else None,
                    "timestamp": datetime.now(),
                    "likes": 0,
                    "comentarios": 0,
                    "compartidos": 0
                }

                st.session_state.posts.insert(0, nuevo_post)
                st.success("✅ ¡Post publicado exitosamente!")
                st.balloons()

                # En producción se enviaría a FIWARE
                st.info("📤 En producción, este post se almacenaría en FIWARE Orion-LD")

        st.markdown("---")

        # Feed de posts
        st.markdown("### 📰 Feed de Publicaciones")

        # Filtros y ordenamiento
        col_filter1, col_filter2, col_filter3 = st.columns(3)

        with col_filter1:
            filtro_orden = st.selectbox("Ordenar por", ["Más recientes", "Más populares", "Más comentados"])

        with col_filter2:
            filtro_tipo = st.selectbox("Tipo", ["Todos", "Solo seguidos", "Tendencias"])

        with col_filter3:
            st.markdown("")
            if st.button("🔄 Actualizar", use_container_width=True):
                st.rerun()

        st.markdown("---")

        # Mostrar posts
        for post in st.session_state.posts:
            # Contenedor de post
            with st.container():
                # Header del post
                col_avatar, col_info = st.columns([1, 11])

                with col_avatar:
                    st.markdown(f"## {post['avatar']}")

                with col_info:
                    st.markdown(f"**{post['autor']}** {post['username']}")
                    tiempo_transcurrido = datetime.now() - post['timestamp']
                    horas = int(tiempo_transcurrido.total_seconds() / 3600)
                    if horas < 1:
                        minutos = int(tiempo_transcurrido.total_seconds() / 60)
                        tiempo_str = f"{minutos}m"
                    elif horas < 24:
                        tiempo_str = f"{horas}h"
                    else:
                        dias = int(horas / 24)
                        tiempo_str = f"{dias}d"

                    st.caption(f"🕐 {tiempo_str}")

                # Contenido del post
                st.markdown(post['contenido'])

                # Imagen si existe
                if post['imagen']:
                    st.info(f"📷 {post['imagen']}")

                # Acciones del post
                col_like, col_comment, col_share, col_save = st.columns(4)

                with col_like:
                    if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                        post['likes'] += 1
                        st.rerun()

                with col_comment:
                    if st.button(f"💬 {post['comentarios']}", key=f"comment_{post['id']}"):
                        st.info("💬 Sección de comentarios en desarrollo")

                with col_share:
                    if st.button(f"🔄 {post['compartidos']}", key=f"share_{post['id']}"):
                        post['compartidos'] += 1
                        st.success("¡Post compartido!")

                with col_save:
                    if st.button("🔖 Guardar", key=f"save_{post['id']}"):
                        st.success("Post guardado en favoritos")

                st.markdown("---")

    with col_sidebar:
        # Tendencias
        st.markdown("### 🔥 Tendencias")

        st.markdown("""
        1. **#FIWARE** - 1.2k posts
        2. **#IoT** - 856 posts
        3. **#Docker** - 734 posts
        4. **#Python** - 621 posts
        5. **#AWS** - 489 posts
        6. **#Streamlit** - 367 posts
        7. **#DataScience** - 298 posts
        """)

        st.markdown("---")

        # Sugerencias de seguimiento
        st.markdown("### 👥 Sugerencias para seguir")

        usuarios_sugeridos = [
            ("Pedro López", "@pedro_tech", "👨‍💼", "Developer | IoT Enthusiast"),
            ("Laura Kim", "@laura_ai", "👩‍🔬", "AI Researcher | ML Engineer"),
            ("Diego Silva", "@diego_cloud", "👨‍🚀", "Cloud Architect | AWS Expert")
        ]

        for nombre, username, avatar, bio in usuarios_sugeridos:
            col_avatar_sug, col_info_sug = st.columns([1, 3])

            with col_avatar_sug:
                st.markdown(f"### {avatar}")

            with col_info_sug:
                st.markdown(f"**{nombre}**")
                st.caption(username)

            st.caption(bio)
            if st.button(f"➕ Seguir", key=f"follow_{username}", use_container_width=True):
                st.success(f"Ahora sigues a {nombre}")

            st.markdown("")

        st.markdown("---")

        # Estadísticas del usuario
        st.markdown("### 📊 Tus Estadísticas")

        st.metric("Posts publicados", random.randint(10, 50))
        st.metric("Seguidores", random.randint(100, 500))
        st.metric("Siguiendo", random.randint(50, 200))
        st.metric("Likes recibidos", random.randint(200, 1000))

        st.markdown("---")

        # Enlaces rápidos
        st.markdown("### 🔗 Enlaces Rápidos")

        if st.button("📝 Mi Perfil", use_container_width=True):
            st.info("Página de perfil en desarrollo")

        if st.button("⚙️ Configuración", use_container_width=True):
            st.info("Página de configuración en desarrollo")

        if st.button("📧 Mensajes", use_container_width=True):
            st.info("Sistema de mensajería en desarrollo")

        if st.button("🔔 Notificaciones", use_container_width=True):
            st.info("Tienes 5 notificaciones nuevas")

# Sidebar adicional
with st.sidebar:
    st.markdown("## 📱 Información del Muro")

    if st.session_state.logged_in:
        st.success(f"Conectado como: **{st.session_state.get('username', 'Usuario')}**")
    else:
        st.warning("Inicia sesión para interactuar")

    st.markdown("---")

    st.markdown("### 📈 Actividad en Vivo")
    st.markdown(f"""
    - 👥 {random.randint(200, 500)} usuarios activos
    - 📝 {random.randint(50, 150)} posts hoy
    - 💬 {random.randint(500, 1500)} comentarios hoy
    - ❤️ {random.randint(1000, 5000)} likes hoy
    """)

    st.markdown("---")

    st.markdown("### ℹ️ Sobre el Muro")
    st.markdown("""
    Este muro social es una demo que simula:
    - Publicación de contenido
    - Interacción social (likes, comentarios)
    - Feed en tiempo real
    - Integración con FIWARE para almacenamiento
    """)
