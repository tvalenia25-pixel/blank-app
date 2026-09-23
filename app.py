import streamlit as st

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Reliper - Sistema Productivo",
    page_icon="🏭",
    layout="wide"
)

# ============================================================
# TÍTULO
# ============================================================

st.title("🏭 Sistema Productivo Reliper")
st.subheader("Cotización y estimación de Lead Time")

st.divider()

# ============================================================
# DATOS DEL PEDIDO
# ============================================================

st.header("1. Datos del pedido")

col1, col2, col3 = st.columns(3)

with col1:
    categoria = st.selectbox(
        "Categoría",
        [
            "Perno",
            "Perno M",
            "Espárrago",
            "Tuerca",
            "Otro"
        ]
    )

with col2:
    geometria = st.selectbox(
        "Geometría final",
        [
            "HEXAGONAL",
            "REDONDO",
            "CUADRADO",
            "CAB. CUADRADA",
            "OTRA"
        ]
    )

with col3:
    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        value=100,
        step=1
    )

col4, col5, col6 = st.columns(3)

with col4:
    diametro = st.number_input(
        "Diámetro (pulg)",
        min_value=0.0,
        value=0.75,
        step=0.01
    )

with col5:
    tratamiento = st.selectbox(
        "Tratamiento térmico",
        ["NO", "SI"]
    )

with col6:
    recubrimiento = st.selectbox(
        "Recubrimiento",
        ["NO", "SI"]
    )

st.divider()

# ============================================================
# RUTA PRODUCTIVA
# ============================================================

st.header("2. Ruta productiva")

# Por ahora son reglas iniciales.
# Después conectaremos aquí el Motor de rutas.

procesos = []

# -------------------------
# CORTE
# -------------------------

if categoria == "Espárrago":

    if diametro <= 1.5:
        corte = "Corte automático"
    else:
        corte = "Corte Sierra"

elif categoria == "Perno M":

    corte = "Corte Cizalla"

else:

    corte = "Corte Cizalla"


procesos.append(corte)

# -------------------------
# BISELADO
# -------------------------

biselado = "No definido"

if categoria in ["Perno", "Perno M", "Espárrago"]:
    biselado = "Biselado-Centro"

procesos.append(biselado)

# -------------------------
# HILADO
# -------------------------

hilado = "No definido"

if categoria in ["Perno", "Perno M", "Espárrago"]:
    hilado = "Terraja"

procesos.append(hilado)

# -------------------------
# FORJADO
# -------------------------

forjado = "No definido"

if categoria in ["Perno", "Perno M"]:
    forjado = "Forjado"

procesos.append(forjado)

# -------------------------
# MECANIZADO
# -------------------------

mecanizado = "No"

# Regla actual:
# todos los productos métricos llevan mecanizado

if categoria == "Perno M":
    mecanizado = "Mecanizado"

procesos.append(mecanizado)

# -------------------------
# TRATAMIENTO
# -------------------------

if tratamiento == "SI":
    procesos.append("Tratamiento térmico")

# -------------------------
# RECUBRIMIENTO
# -------------------------

if recubrimiento == "SI":
    procesos.append("Recubrimiento")

# ============================================================
# MOSTRAR RUTA
# ============================================================

st.subheader("Ruta estimada")

for i, proceso in enumerate(procesos, start=1):

    if proceso not in ["No definido", "No"]:
        st.write(f"**{i}. {proceso}**")

st.divider()

# ============================================================
# ESTIMACIÓN DE LEAD TIME
# ============================================================

st.header("3. Estimación de Lead Time")

# Por ahora dejamos un cálculo provisional.
# Más adelante aquí conectaremos el modelo Random Forest.

lead_time_base = 10

if cantidad > 500:
    lead_time_base += 3

if cantidad > 1000:
    lead_time_base += 3

if tratamiento == "SI":
    lead_time_base += 3

if recubrimiento == "SI":
    lead_time_base += 2

if mecanizado == "Mecanizado":
    lead_time_base += 3

lead_time = lead_time_base

col7, col8, col9 = st.columns(3)

with col7:
    st.metric(
        "Cantidad",
        f"{cantidad:,}".replace(",", ".")
    )

with col8:
    st.metric(
        "Procesos",
        len([p for p in procesos if p not in ["No definido", "No"]])
    )

with col9:
    st.metric(
        "Lead Time estimado",
        f"{lead_time} días"
    )

st.divider()

# ============================================================
# RESULTADO
# ============================================================

st.header("4. Resultado")

st.success(
    f"Lead Time estimado: {lead_time} días hábiles"
)

st.info(
    "Esta es la primera versión del sistema. "
    "El cálculo será reemplazado posteriormente por el modelo predictivo."
)

# ============================================================
# PIE
# ============================================================

st.caption(
    "Reliper | Sistema Productivo para la Adjudicación de Pedidos de Producción"
)
