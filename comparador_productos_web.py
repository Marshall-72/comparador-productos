import pandas as pd
import streamlit as st
import os  # Para trabajar con nombres de archivo

st.title("🔬 Comparador de Propiedades Físico-Químicas entre Productos")

st.markdown("""
Sube las tablas de los **4 productos** en formato Excel.  
Cada archivo debe tener dos columnas: **Propiedad** y **Valor**.  
El nombre del archivo (por ejemplo `diesel.xlsx`) se usará como nombre del producto.
""")

# Subida de archivos
uploaded_files = st.file_uploader("Sube los archivos Excel:", type=["xlsx"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 4:
    productos = {}
    for file in uploaded_files:
        # Usar nombre de archivo como nombre de producto
        nombre_producto = os.path.splitext(file.name)[0].capitalize()
        df = pd.read_excel(file)
        productos[nombre_producto] = df

    # Mostrar nombres cargados
    st.success(f"✅ Archivos cargados: {', '.join(productos.keys())}")

    # Crear lista única de propiedades disponibles
    todas_propiedades = pd.concat([df["Propiedad"] for df in productos.values()]).unique()

    # Buscador de propiedad
    texto_busqueda = st.text_input("🔍 Escribe parte del nombre de la propiedad:")
    propiedades_filtradas = [p for p in todas_propiedades if texto_busqueda.lower() in p.lower()]

    if propiedades_filtradas:
        propiedad_seleccionada = st.selectbox("Selecciona la propiedad exacta:", sorted(propiedades_filtradas))

        if st.button("Comparar"):
            resultados = []

            for nombre, df in productos.items():
                fila = df[df["Propiedad"] == propiedad_seleccionada]
                if not fila.empty:
                    valor = fila["Valor"].values[0]
                else:
                    valor = "No disponible"
                resultados.append({"Producto": nombre, "Valor": valor})

            comparativa = pd.DataFrame(resultados)

            st.subheader(f"📊 Comparativa de '{propiedad_seleccionada}' entre productos:")
            st.dataframe(comparativa)
    else:
        if texto_busqueda:
            st.warning("No se encontraron propiedades que coincidan.")
else:
    st.warning("Por favor sube exactamente 4 archivos Excel con formato: Propiedad | Valor.")
