import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.bedrock_services import generar_descripcion_producto, generar_imagen_promocional, generar_resumen_comentarios

# --- Interfaz de Streamlit ---
st.title("Snack Marketing AI 🤖")
st.markdown("Genera descripciones e imágenes de productos con Bedrock.")

tab1, tab2, tab3 = st.tabs(["Generador de Descripción", "Generador de Imágenes", "Análisis de Comentarios de Clientes"])

with tab1:
    st.header("✍️ Generar Descripción de Producto")
    with st.form("form_descripcion"):
        nombre = st.text_input("Nombre del Producto", "Power Crunch")
        ingredientes = st.text_input("Ingredientes Clave", "Avena, almendras, chocolate negro")
        beneficios = st.text_area("Beneficios del Producto", "Alto en fibra, energía sostenida, sin azúcares añadidos")
        submitted_desc = st.form_submit_button("Generar Descripción")
        if submitted_desc:
            with st.spinner('Generando descripción...'):
                descripcion = generar_descripcion_producto(nombre, ingredientes, beneficios)
                st.subheader("Descripción Generada:")
                st.success(descripcion)

with tab2:
    st.header("🖼️ Generar Imagen Promocional")
    with st.form("form_imagen"):
        prompt_imagen = st.text_area("Prompt para la Imagen",
                                     "Foto de un bowl de snack de avena y almendras, con chocolate derretido, en un entorno rústico de madera, con luz natural. Estilo fotográfico: minimalista y saludable.")
        submitted_img = st.form_submit_button("Generar Imagen")
        if submitted_img:
            with st.spinner('Generando imagen...'):
                imagen_base64 = generar_imagen_promocional(prompt_imagen)
                st.subheader("Imagen Generada:")
                if imagen_base64.startswith("Error"):
                    st.error(imagen_base64)
                else:
                    st.image(imagen_base64, caption="Imagen promocional generada", use_column_width=True)

with tab3:
    st.header("🗣️ Análisis de Comentarios de Clientes")
    with st.form("form_comentarios"):
        comentarios = st.text_area(
            "Pega aquí los comentarios de usuarios",
            "¡Me encanta el sabor a coco, es delicioso y crujiente!\\n"
            "El empaque es muy bonito y práctico, pero el precio es un poco alto.\\n"
            "Ideal para una merienda rápida y saludable.\\n"
            "No me gustó que es muy dulce, esperaba algo más natural."
        )
        submitted = st.form_submit_button("Generar Resumen")

    if submitted:
        if not comentarios:
            st.warning("Por favor, ingresa al menos un comentario.")
        else:
            with st.spinner('Analizando y generando resumen...'):
                resumen = generar_resumen_comentarios(comentarios)
                st.subheader("Resumen Generado:")
                st.success(resumen)