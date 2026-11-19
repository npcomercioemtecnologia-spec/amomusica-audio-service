# Microserviço de Áudio do YouTube - AmoMúsica PRO

Este microserviço extrai o fluxo de áudio puro (`.m4a` / `.opus`) de vídeos do YouTube usando FastAPI e `yt-dlp`.
Ele foi projetado para rodar em plataformas de nuvem gratuitas (como **Render.com**, **Railway** ou **Koyeb**) para permitir que sua aplicação na **Hostinger** toque áudio nativo com tela apagada, contornando o bloqueio de `shell_exec` da hospedagem compartilhada.

---

## Como publicar gratuitamente no Render.com (3 minutos):

1. **Crie um repositório no GitHub**:
   - Acesse [github.com/new](https://github.com/new).
   - Nomeie como `amomusica-stream-service` (pode ser Público ou Privado).
   - Faça upload dos 3 arquivos desta pasta (`main.py`, `requirements.txt`, `Procfile`).

2. **Crie o serviço no Render**:
   - Acesse [dashboard.render.com](https://dashboard.render.com) e entre com sua conta do GitHub.
   - Clique no botão **New +** > **Web Service**.
   - Conecte o repositório `amomusica-stream-service` que acabou de criar.
   - Configurações:
     - **Name**: `amomusica-audio-service` (ou outro nome de sua preferência)
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: `Free` (Gratuito)
   - Clique em **Create Web Service**.

3. **Copie a URL gerada e configure no seu AmoMúsica**:
   - Assim que o Render terminar o deploy (1 a 2 minutos), ele exibirá a sua URL pública:
     `https://amomusica-audio-service.onrender.com`
   - Abra o arquivo `.env` do AmoMúsica (tanto local quanto na Hostinger) e adicione:
     ```env
     YT_STREAM_SERVICE_URL=https://amomusica-audio-service.onrender.com
     ```

Pronto! Seu AmoMúsica agora transmitirá áudio puro nativo em qualquer hospedagem e com a tela do celular bloqueada.
