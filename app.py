import streamlit as st  # Avisamos del uso de la librería
from groq import Groq  # Importamos la librería

# Configuración de la ventana de la web
st.set_page_config(page_title="Mi ChatBot | IA", page_icon="🤖")

# Título de la aplicación
st.title("Mi app con Streamlit")

# Input
nombre = st.text_input("¿Cuál es tu nombre?")

# Crear un botón con funcionalidad
if st.button("Enviar"):
    # Escribimos un mensaje en pantalla
    st.write(f"¡Hola, {nombre}! Gracias por usar mi app!")

MODELOS = ["Elija un modelo", 'llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']  # Lista de opciones

# Nos conectamos con la API - creamos un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]  # Obtenemos la clave de la API
    return Groq(api_key=clave_secreta)  # Conectamos a la API

# Selecciona el modelo de la IA
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,  # Selecciona el modelo de la IA
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True  # Funcionalidad para que la IA me responda en tiempo real
    )  # Devuelve la respuesta que manda la IA

# Historial de mensajes
def inicializar_estado():
    # Si no existe "mensajes" entonces creamos un historial
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []  # Simula el historial vacío

def configurar_pagina():
    st.title("Chat de IA")  # Titulo
    st.sidebar.title("Configuración")  # Titulo => Barra lateral
    opcion = st.sidebar.selectbox(
        "Elegí un modelo",  # Titulo
        options=MODELOS,  # Opciones => deben estar en una lista
        index=0  # Valor por defecto [0, 1, 2]
    )
    return opcion  # Agregamos esto para obtener el nombre del modelo

def actualizar_historial(rol, contenido, avatar):
    # El metodo append(dato) Agrega datos a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial():  # Guarda la estructura visual del mensaje
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""  # Variable vacía
    for frase in chat_completo:
        if frase.choices[0].delta.content:  # Evitamos el dato NONE
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    # Invocación de funciones
    modelo = configurar_pagina()  # modelo debe ir en minúscula, ya que ya tenemos una en mayúscula | agarramos el modelo seleccionado
    clienteUsuario = crear_usuario_groq()  # Conecta con la API GROQ
    inicializar_estado()  # Se crea en memoria el historial vacío
    area_chat()  # Se crea el contenedor de los mensajes

    mensaje = st.chat_input("Escribí un mensaje ;)") 
    chat_completo = None  # Definir la variable antes de usarla

    # Verificar que la variable mensaje tenga contenido
    if mensaje:
        actualizar_historial("user", mensaje, "👩‍💻")  # Mostramos el mensaje en el chat
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)  # Obtenemos la respuesta de la IA
    
    # Verificamos que chat_completo no sea None antes de intentar procesarlo
    if chat_completo:
        with st.chat_message("assistant"):
            respuesta_completa = st.empty()  # Usamos un contenedor vacío para mostrar respuestas en tiempo real
            for resp in generar_respuesta(chat_completo):
                respuesta_completa.markdown(resp)  # Mostrar cada fragmento de la respuesta
            actualizar_historial("assistant", respuesta_completa, "🤖")  # Mostramos el mensaje
            st.rerun()  # Actualizar sin tocar F5

# Corregir la línea para ejecutar la aplicación correctamente
if __name__ == "__main__":
    main()
