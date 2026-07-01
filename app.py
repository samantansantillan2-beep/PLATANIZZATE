import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="Platanízzate",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# ESTILOS
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #fffaf0 0%, #f7f2e8 100%);
    }
    .hero {
        padding: 2.2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #204f32, #4d7c46);
        color: white;
        box-shadow: 0 12px 30px rgba(32,79,50,.18);
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        font-size: 3rem;
        margin: 0;
    }
    .hero p {
        font-size: 1.1rem;
        margin-top: .7rem;
        margin-bottom: 0;
    }
    .card {
        background: white;
        border-radius: 20px;
        padding: 1.3rem;
        border: 1px solid #eadfca;
        box-shadow: 0 8px 22px rgba(82,64,38,.07);
        margin-bottom: 1rem;
    }
    .price {
        font-size: 1.7rem;
        font-weight: 800;
        color: #204f32;
    }
    .small-note {
        font-size: .9rem;
        color: #5d5d5d;
    }
    .order-box {
        background: #ffffff;
        border-left: 6px solid #e58c2b;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 8px 22px rgba(82,64,38,.08);
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        min-height: 3rem;
    }
</style>
""", unsafe_allow_html=True)

PIZZAS = {
    "Pizza Tradicional": {
        "precio": 7.99,
        "descripcion": "Base de plátano verde, salsa de tomate, queso, jamón y pimiento.",
    },
    "Pizza de Camarón": {
        "precio": 9.99,
        "descripcion": "Base de plátano verde, salsa de tomate, queso y camarón.",
    },
    "Pizza de Carne Molida": {
        "precio": 7.99,
        "descripcion": "Base de plátano verde, salsa de tomate, queso y carne molida.",
    },
}

EXTRAS = {
    "Queso extra": 0.75,
    "Jamón": 0.75,
    "Pepperoni": 0.75,
    "Pimiento": 0.50,
    "Camarón": 1.50,
    "Carne molida": 1.00,
}

INGREDIENTES_RETIRABLES = [
    "Queso",
    "Jamón",
    "Pepperoni",
    "Pimiento",
    "Camarón",
    "Carne molida",
    "Cebolla",
    "Ajo",
]

# -----------------------------
# ENCABEZADO
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>🍕 Platanízzate</h1>
    <p>Pizza artesanal con base de plátano verde, libre de gluten y personalizada a tu gusto.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🌿 Nuestra propuesta")
    st.write(
        "Ofrecemos pizzas con base de plátano verde para personas celíacas, "
        "con sensibilidad al gluten o que buscan una alternativa diferente."
    )
    st.info(
        "La información sobre alergias sirve para personalizar el pedido. "
        "Las alergias graves deben confirmarse directamente con el negocio."
    )
    st.markdown("---")
    st.caption("Proyecto académico de emprendimiento")

tab_inicio, tab_pedido, tab_resumen = st.tabs(
    ["🏠 Inicio", "🛒 Crear pedido", "📋 Resumen"]
)

with tab_inicio:
    st.subheader("Conoce nuestro menú")
    cols = st.columns(3)
    for col, (nombre, datos) in zip(cols, PIZZAS.items()):
        with col:
            st.markdown(
                f"""
                <div class="card">
                    <h3>{nombre}</h3>
                    <p>{datos["descripcion"]}</p>
                    <div class="price">${datos["precio"]:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### ¿Por qué Platanízzate?")
    c1, c2, c3 = st.columns(3)
    c1.success("🌱 Base elaborada con plátano verde")
    c2.success("🧩 Pedido personalizable")
    c3.success("⚠️ Registro de alergias y restricciones")

with tab_pedido:
    st.subheader("Arma tu pizza")

    with st.form("formulario_pedido", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            nombre_cliente = st.text_input(
                "Nombre del cliente *",
                placeholder="Ejemplo: Andrea Pérez",
            )
            telefono = st.text_input(
                "Número de contacto *",
                placeholder="Ejemplo: 0999999999",
            )
            pizza = st.selectbox("Selecciona tu pizza *", list(PIZZAS.keys()))
            cantidad = st.number_input(
                "Cantidad",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
            )
            extras = st.multiselect(
                "Ingredientes adicionales",
                list(EXTRAS.keys()),
                help="Los ingredientes extra tienen un costo adicional.",
            )

        with col2:
            retirar = st.multiselect(
                "Ingredientes que deseas retirar",
                INGREDIENTES_RETIRABLES,
            )
            tiene_alergias = st.radio(
                "¿Tienes alergias o restricciones alimentarias?",
                ["No", "Sí"],
                horizontal=True,
            )
            alergias = st.text_area(
                "Especifica tus alergias o restricciones",
                placeholder="Ejemplo: alergia a los lácteos o intolerancia a la cebolla",
                disabled=tiene_alergias == "No",
            )
            entrega = st.selectbox(
                "Forma de entrega",
                ["Retiro en el local", "Entrega a domicilio"],
            )
            direccion = st.text_input(
                "Dirección de entrega",
                placeholder="Sector, calle principal y referencia",
                disabled=entrega == "Retiro en el local",
            )
            pago = st.selectbox(
                "Forma de pago",
                ["Efectivo", "Transferencia bancaria", "Tarjeta (demostración)"],
            )

        observaciones = st.text_area(
            "Observaciones adicionales",
            placeholder="Ejemplo: cortar en ocho porciones",
        )

        precio_base = PIZZAS[pizza]["precio"]
        precio_extras = sum(EXTRAS[item] for item in extras)
        total = (precio_base + precio_extras) * cantidad

        st.markdown(f"### Total estimado: **${total:.2f}**")

        enviar = st.form_submit_button("Generar pedido 🍕", use_container_width=True)

    if enviar:
        errores = []
        if not nombre_cliente.strip():
            errores.append("Debes escribir el nombre del cliente.")
        if not telefono.strip():
            errores.append("Debes escribir un número de contacto.")
        if tiene_alergias == "Sí" and not alergias.strip():
            errores.append("Debes especificar la alergia o restricción.")
        if entrega == "Entrega a domicilio" and not direccion.strip():
            errores.append("Debes escribir la dirección de entrega.")

        if errores:
            for error in errores:
                st.error(error)
        else:
            pedido = {
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Cliente": nombre_cliente.strip(),
                "Teléfono": telefono.strip(),
                "Pizza": pizza,
                "Cantidad": int(cantidad),
                "Extras": ", ".join(extras) if extras else "Ninguno",
                "Retirar": ", ".join(retirar) if retirar else "Nada",
                "Alergias": alergias.strip() if tiene_alergias == "Sí" else "Ninguna indicada",
                "Entrega": entrega,
                "Dirección": direccion.strip() if entrega == "Entrega a domicilio" else "No aplica",
                "Pago": pago,
                "Observaciones": observaciones.strip() if observaciones.strip() else "Ninguna",
                "Total": f"${total:.2f}",
            }
            st.session_state["pedido"] = pedido
            st.success("Pedido generado correctamente. Revísalo en la pestaña «Resumen».")

with tab_resumen:
    st.subheader("Resumen del pedido")

    if "pedido" not in st.session_state:
        st.info("Todavía no has generado un pedido.")
    else:
        p = st.session_state["pedido"]

        resumen = f"""PEDIDO PLATANÍZZATE
Fecha: {p["Fecha"]}
Cliente: {p["Cliente"]}
Teléfono: {p["Teléfono"]}
Pizza: {p["Pizza"]}
Cantidad: {p["Cantidad"]}
Ingredientes extra: {p["Extras"]}
Retirar: {p["Retirar"]}
Alergias o restricciones: {p["Alergias"]}
Entrega: {p["Entrega"]}
Dirección: {p["Dirección"]}
Forma de pago: {p["Pago"]}
Observaciones: {p["Observaciones"]}
TOTAL ESTIMADO: {p["Total"]}

Pedido sujeto a confirmación del negocio.
"""

        st.markdown(
            f"""
            <div class="order-box">
                <h3>🍕 {p["Pizza"]}</h3>
                <p><b>Cliente:</b> {p["Cliente"]}</p>
                <p><b>Cantidad:</b> {p["Cantidad"]}</p>
                <p><b>Extras:</b> {p["Extras"]}</p>
                <p><b>Retirar:</b> {p["Retirar"]}</p>
                <p><b>Alergias:</b> {p["Alergias"]}</p>
                <p><b>Entrega:</b> {p["Entrega"]}</p>
                <p><b>Pago:</b> {p["Pago"]}</p>
                <h3>Total: {p["Total"]}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area("Texto completo del pedido", resumen, height=330)

        col_a, col_b = st.columns(2)

        with col_a:
            st.download_button(
                "Descargar pedido en TXT",
                data=resumen.encode("utf-8"),
                file_name="pedido_platanizzate.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with col_b:
            df = pd.DataFrame([p])
            st.download_button(
                "Descargar pedido en CSV",
                data=df.to_csv(index=False).encode("utf-8-sig"),
                file_name="pedido_platanizzate.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.caption(
            "Esta versión no usa una base de datos. El pedido se muestra en pantalla "
            "y puede descargarse como archivo."
        )
