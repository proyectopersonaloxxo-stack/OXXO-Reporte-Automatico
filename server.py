import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header # <--- ¡ESTA ES LA LÍNEA QUE FALTABA!
from flask import Flask, request, jsonify
from flask_cors import CORS

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DEL CORREO (¡REVISA ESTO!)
#    Asegúrate de que la contraseña sea la de 16 caracteres de Gmail.
# -----------------------------------------------------------------------------
SENDER_EMAIL = 'proyectopersonaloxxo@gmail.com' 
SENDER_PASSWORD = 'ekqrzjokpydqejrm' 
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
# -----------------------------------------------------------------------------

# Inicialización del servidor Flask
app = Flask(__name__)
CORS(app) # Permite que el HTML hable con el servidor

@app.route('/')
def index():
    return "El servidor de reportes OXXO está vivo y listo para recibir conexiones."

# Ruta principal para recibir los datos del reporte
@app.route('/enviar-reporte', methods=['POST'])
def enviar_reporte():
    try:
        # 1. Recibir datos del HTML (Frontend)
        datos = request.json
        tienda = datos.get('tienda')
        proveedor_email = datos.get('proveedor')
        reportador = datos.get('reportador') # Campo nuevo
        categoria = datos.get('categoria')   # Campo nuevo
        prioridad = datos.get('prioridad')   # Campo nuevo
        mensaje_plantilla = datos.get('mensaje')

        # Validación de todos los campos
        if not all([tienda, proveedor_email, reportador, categoria, prioridad, mensaje_plantilla]):
            return jsonify({"error": "Faltan campos. Se recibieron datos incompletos."}), 400

        print(f"📡 Recibiendo solicitud para tienda: {tienda} (Reporta: {reportador})")

        # 2. Construir el correo
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = proveedor_email
        
        # Asunto dinámico basado en los datos
        emoji_prioridad = "🚨" if prioridad == "Urgente" else "⚠️" if prioridad == "Normal" else "ℹ️"
        
        # Usamos Header para codificar el asunto correctamente
        asunto_texto = f"{emoji_prioridad} {prioridad.upper()} | {categoria} | Tienda: {tienda}"
        msg['Subject'] = Header(asunto_texto, 'utf-8')


        # Cuerpo del correo (HTML Profesional)
        cuerpo_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ width: 90%; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                .header {{ font-size: 24px; color: #E61C2D; font-weight: bold; }}
                .tag {{ display: inline-block; background-color: #f0f0f0; padding: 5px 10px; border-radius: 15px; font-size: 14px; font-weight: bold; }}
                .priority-Urgente {{ background-color: #E61C2D; color: white; }}
                .priority-Normal {{ background-color: #FFCA05; color: #333; }}
                .priority-Baja {{ background-color: #f0f0f0; color: #333; }}
                pre {{ background-color: #f9f9f9; padding: 15px; border: 1px solid #eee; border-radius: 5px; font-family: 'Courier New', Courier, monospace; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <div class="container">
                <span class="header">Reporte de Incidencia OXXO</span>
                <hr>
                <p>Se ha generado un nuevo reporte de incidencia con los siguientes detalles:</p>
                
                <p>
                    <strong>Tienda:</strong> {tienda}<br>
                    <strong>Reportado por:</strong> {reportador}<br>
                    <strong>Categoría:</strong> {categoria}<br>
                    <strong>Prioridad:</strong> <span class="tag priority-{prioridad}">{prioridad}</span>
                </p>

                <h3>Detalle de la Incidencia:</h3>
                <pre>{mensaje_plantilla}</pre>
                
                <p style="font-size: 12px; color: #888;">Este es un correo generado automáticamente por el Sistema de Gestión de Reportes OXXO.</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(cuerpo_html, 'html'))

        # 3. Enviar el correo
        print("-> Conectando con servidor SMTP...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Iniciar conexión segura
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, [proveedor_email], msg.as_string())
        
        print("✅ Correo enviado exitosamente.")
        return jsonify({"message": "Reporte enviado exitosamente"}), 200

    except smtplib.SMTPAuthenticationError:
        print(f"❌ ERROR DE AUTENTICACIÓN SMTP: {SENDER_EMAIL}")
        return jsonify({"error": "(535) Error de Autenticación. Revisa SENDER_EMAIL y SENDER_PASSWORD en server.py."}), 500
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------------------------
# 4. INICIO DEL SERVIDOR (LISTO PARA RENDER)
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("\n==================================================")
    print("🚀 SERVIDOR PYTHON (FLASK) INICIADO")
    print(f"📡 Escuchando en: http://0.0.0.0:{port}") 
    print("==================================================")
    
    app.run(host='0.0.0.0', port=port, debug=False)

