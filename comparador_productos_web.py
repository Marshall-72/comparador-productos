import pandas as pd
import streamlit as st

st.title("🔬 Comparador de Propiedades Físico-Químicas entre Productos")

st.markdown("""
Sube las tablas de los **4 productos** en formato Excel.  
Cada archivo debe tener dos columnas: **Propiedad** y **Valor**.
""")

# Subida de archivos
uploaded_files = st.file_uploader("Sube los archivos Excel:", type=["xlsx"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 4:
    productos = {}
    for i, file in enumerate(uploaded_files):
        nombre_producto = f"Producto {chr(65 + i)}"  # Producto A, B, C, D
        df = pd.read_excel(file)
        productos[nombre_producto] = df

    # Obtener lista única de propiedades disponibles
    todas_propiedades = pd.concat([df["Propiedad"] for df in productos.values()]).unique()
    propiedad_seleccionada = st.selectbox("Selecciona la propiedad a comparar:", sorted(todas_propiedades))

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
    st.warning("Por favor sube exactamente 4 archivos Excel con formato: Propiedad | Valor.")

