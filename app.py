import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Planificador de Ahorro", layout="centered")
st.title("🎯 Planificador de Ahorro")

# Inicializar variables en la sesión
if "datos" not in st.session_state:
    st.session_state.datos = pd.DataFrame(columns=["Mes", "Ingreso", "Gasto Libre", "Ahorro", "Interés", "Saldo Final"])
    st.session_state.saldo_actual = 150000.0  # Tu ahorro inicial

# Barra lateral para ingresar datos
st.sidebar.header("Agrega un nuevo mes")
mes = st.sidebar.text_input("Nombre del mes (Ej: Agosto)", "")
ingreso = st.sidebar.number_input("Ingresos ($)", min_value=0, value=160000, step=10000)
gasto = st.sidebar.number_input("Gastos Libres ($)", min_value=0, value=40000, step=10000)

if st.sidebar.button("Registrar Mes"):
    if mes:
        # Cálculos matemáticos
        ahorro = ingreso - gasto
        interes = (st.session_state.saldo_actual + ahorro) * 0.0041
        nuevo_saldo = st.session_state.saldo_actual + ahorro + interes
        
        # Crear nueva fila de datos
        nuevo_mes = pd.DataFrame([{
            "Mes": mes,
            "Ingreso": ingreso,
            "Gasto Libre": gasto,
            "Ahorro": ahorro,
            "Interés": round(interes),
            "Saldo Final": round(nuevo_saldo)
        }])
        
        # Actualizar la tabla y el saldo
        st.session_state.datos = pd.concat([st.session_state.datos, nuevo_mes], ignore_index=True)
        st.session_state.saldo_actual = nuevo_saldo
    else:
        st.sidebar.warning("Por favor, escribe el nombre del mes.")

# Mostrar métrica principal
st.metric(label="Saldo Acumulado Actual", value=f"${round(st.session_state.saldo_actual):,}".replace(",", "."))

# Mostrar tabla y gráfico si hay datos
if not st.session_state.datos.empty:
    st.write("### Desglose Mensual")
    st.dataframe(st.session_state.datos, use_container_width=True)
    
    st.write("### Crecimiento del Ahorro")
    st.line_chart(st.session_state.datos.set_index("Mes")["Saldo Final"])
    
    if st.button("Reiniciar Planificador"):
        st.session_state.datos = pd.DataFrame(columns=["Mes", "Ingreso", "Gasto Libre", "Ahorro", "Interés", "Saldo Final"])
        st.session_state.saldo_actual = 150000.0
        st.rerun()
