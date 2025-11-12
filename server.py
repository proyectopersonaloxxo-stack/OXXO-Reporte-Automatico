import smtplib
from email.mime.text import MIMEText
from email.header import Header
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# --- CONFIGURACIÓN DE TU SERVIDOR Y CORREO ---
# ¡IMPORTANTE! Reemplaza estos datos con tu correo y tu contraseña de aplicación.
SMTP_SERVER = 'smtp.gmail.com' # Si usas Gmail
SMTP_PORT = 587  # Cambio para forzar despliegue
SENDER_EMAIL = 'proyectopersonaloxxo@gmail.com' # TU CORREO
SENDER_PASSWORD = 'ekqrzjokpydqejrm' # TU CONTRASEÑA DE APLICACIÓN

app = Flask(__name__)
# Esto permite que el HTML (que se abre localmente) se conecte con el servidor Python.
CORS(app) 

@app.route('/enviar-reporte', methods=['POST'])
def enviar_reporte():
    try:
        # Intenta cargar el JSON del cuerpo de la solicitud
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'Datos JSON faltantes'}), 400

        tienda = data.get('tienda')
        proveedor = data.get('proveedor')
        mensaje_cuerpo = data.get('mensaje')

        if not tienda or not proveedor or not mensaje_cuerpo:
            return jsonify({'success': False, 'error': 'Faltan campos (tienda, proveedor o mensaje)'}), 400

        # 1. Construir el mensaje de correo
        msg = MIMEText(mensaje_cuerpo, 'plain', 'utf-8')
        
        # Usamos Header para codificar el asunto correctamente (especialmente con acentos)
        asunto = Header(f"🚨 REPORTE OXXO - Tienda {tienda}", 'utf-8')
        
        msg['Subject'] = asunto
        msg['From'] = SENDER_EMAIL
        msg['To'] = proveedor

        print(f"📡 Recibiendo solicitud para tienda: {tienda}")

        # 2. Conectar y Enviar Correo usando SMTPLIB
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Inicia la conexión segura
            server.login(SENDER_EMAIL, SENDER_PASSWORD) # Inicia sesión
            server.sendmail(SENDER_EMAIL, [proveedor], msg.as_string()) # Envía el correo

        print("✅ Correo enviado exitosamente.")
        return jsonify({'success': True, 'message': 'Correo enviado exitosamente'})

    except Exception as e:
        print(f"❌ Error al procesar o enviar el correo: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# -----------------------------------------------------------------------------
# 4. INICIO DEL SERVIDOR (LISTO PARA RENDER)
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # Render (nube) asignará un puerto en la variable 'PORT'.
    # Si 'PORT' no existe (porque estamos en la PC local), usará 5000.
    port = int(os.environ.get('PORT', 5000))
    
    print("\n==================================================")
    print("🚀 SERVIDOR PYTHON (FLASK) INICIADO")
    print(f"📡 Escuchando en: http://0.0.0.0:{port}") # Notar 0.0.0.0 aquí
    print("==================================================")
    
    # host='0.0.0.0' permite que Render se conecte
    app.run(host='0.0.0.0', port=port, debug=False)

