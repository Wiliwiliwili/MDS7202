import gradio as gr

from services import enviar_prediccion

CANALES = ["Correo", "Página Web", "Whatsapp"]
CATEGORIAS = ["Cobros", "Cuenta", "Fraude", "Otro", "Pregunta general", "Técnica"]
TIPOS_CUENTA = ["Business", "Free", "Premium"]

COLOR_PRIORIDAD = {
    "Baja": "#2E7D32",
    "Media": "#F9A825",
    "Alta": "#EF6C00",
    "Critica": "#C62828",
}

CUSTOM_CSS = """
#header {
    background: linear-gradient(90deg, #0B3D91 0%, #00B4D8 100%);
    padding: 24px 28px;
    border-radius: 12px;
    color: white;
    margin-bottom: 8px;
}
#header h1 { margin: 0 0 4px 0; }
#header p { margin: 0; opacity: 0.9; }
#resultado {
    font-size: 1.3rem;
    font-weight: 700;
    text-align: center;
    padding: 18px;
    border-radius: 10px;
    border: 2px solid #ccc;
}
"""

theme = gr.themes.Soft(primary_hue="cyan", secondary_hue="blue", neutral_hue="slate")


def predecir(asunto, contenido, canal, categoria, tipo_cuenta, antiguedad):
    if not asunto or not asunto.strip() or not contenido or not contenido.strip():
        return "<div id='resultado' style='background:#F5F5F5; color:#616161; border-color:#BDBDBD;'>⚠️ Debes completar el asunto y el contenido del ticket.</div>"

    try:
        prioridad = enviar_prediccion(asunto, contenido)
    except Exception as e:
        return f"<div id='resultado' style='background:#FDECEA; color:#C62828; border-color:#C62828;'>❌ Error al obtener la predicción: {e}</div>"

    color = COLOR_PRIORIDAD.get(prioridad, "#333333")
    return (
        f"<div id='resultado' style='background:{color}22; color:{color}; border-color:{color};'>"
        f"Prioridad predicha: {prioridad}</div>"
    )


with gr.Blocks(title="ChaucherApp - Priorización de Tickets") as demo:
    gr.HTML(
        "<div id='header'>"
        "<h1>💬 ChaucherApp — Priorización de Tickets de Soporte</h1>"
        "<p>Clasifica automáticamente la urgencia de un ticket usando IA</p>"
        "</div>"
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🎫 Atributos del Ticket")
            asunto = gr.Textbox(label="Asunto del ticket", placeholder="Ej: No puedo acceder a mi cuenta")
            contenido = gr.Textbox(label="Contenido del ticket", lines=6, placeholder="Describe el problema...")
            canal = gr.Dropdown(CANALES, label="Canal", value=CANALES[0])
            categoria = gr.Dropdown(CATEGORIAS, label="Categoría del problema", value=CATEGORIAS[0])

        with gr.Column():
            gr.Markdown("### 👤 Atributos del Usuario")
            tipo_cuenta = gr.Dropdown(TIPOS_CUENTA, label="Tipo de cuenta", value=TIPOS_CUENTA[0])
            antiguedad = gr.Number(label="Antigüedad de la cuenta (días)", value=365, precision=0, minimum=0)

    boton = gr.Button("Predecir Prioridad", variant="primary")
    resultado = gr.HTML()

    boton.click(
        predecir,
        inputs=[asunto, contenido, canal, categoria, tipo_cuenta, antiguedad],
        outputs=resultado,
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=theme, css=CUSTOM_CSS)
