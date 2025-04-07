import pandas as pd
import streamlit as st

st.title("Comparador de Propiedades Físico-Químicas entre Productos")

st.markdown("""
Sube las tablas de los **4 productos** en formato Excel.  
Cada archivo debe tener una tabla con propiedades como columnas (por ejemplo: Densidad, pH, Color, etc.).
""")

# Subida de archivos
uploaded_files = st.file_uploader("Sube los archivos Excel:", type=["xlsx"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 4:
    productos = {}
    for i, file in enumerate(uploaded_files):
        nombre_producto = f"Producto {chr(65+i)}"  # Producto A, B, C, D
        df = pd.read_excel(file)
        productos[nombre_producto] = df

    # Unir los dataframes
    def unir_productos(diccionario_productos):
        df_unido = pd.DataFrame()
        for nombre, df in diccionario_productos.items():
            df_temp = df.copy()
            df_temp["Producto"] = nombre
            df_unido = pd.concat([df_unido, df_temp], ignore_index=True)
        return df_unido

    df_productos = unir_productos(productos)

    # Selección de propiedad
    propiedades_disponibles = [col for col in df_productos.columns if col != "Producto"]
    propiedad_seleccionada = st.selectbox("Selecciona la propiedad a comparar:", propiedades_disponibles)

    if st.button("Comparar"):
        comparativa = df_productos[["Producto", propiedad_seleccionada]].drop_duplicates()
        comparativa = comparativa.sort_values("Producto")

        st.subheader(f"Comparativa de '{propiedad_seleccionada}' entre productos:")
        st.dataframe(comparativa.reset_index(drop=True))

else:
    st.warning("Por favor sube exactamente 4 archivos Excel.")
