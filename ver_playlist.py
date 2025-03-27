import streamlit as st
import streamlit.components.v1 as components
import requests
import pyrebase

# Lê as credenciais do Firebase do arquivo .streamlit/secrets.toml
firebase_config = {
    "apiKey": st.secrets["firebase"]["apiKey"],
    "authDomain": st.secrets["firebase"]["authDomain"],
    "databaseURL": st.secrets["firebase"]["databaseURL"],
    "storageBucket": st.secrets["firebase"]["storageBucket"]
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Lê email/senha de forma segura
email = st.secrets["firebase"]["email"]
senha = st.secrets["firebase"]["senha"]

playlist_id = "PLCcM9n2mu2uHA6fuInzsrEOhiTq7Dsd97"

FIREBASE_URL = "https://batalha-musical-default-rtdb.firebaseio.com/batalha_estado.json"

def sinalizar_batalha():
    res = requests.patch(FIREBASE_URL, json={"nova_batalha": True})
    return res.status_code == 200


html_code = f"""
<div id="player"></div>

<script src="https://www.youtube.com/iframe_api"></script>
<script>
  let player;
  function onYouTubeIframeAPIReady() {{
    player = new YT.Player('player', {{
      height: '394',
      width: '700',
      playerVars: {{
        listType: 'playlist',
        list: '{playlist_id}'
      }},
      events: {{
        'onStateChange': onPlayerStateChange
      }}
    }});
  }}

  function onPlayerStateChange(event) {{
    if (event.data === YT.PlayerState.ENDED) {{
      console.log("🎬 Playlist terminou. Recarregando...");
      setTimeout(() => location.reload(), 2000); // Espera 2 segundos e recarrega
    }}
  }}
</script>
"""


st.title("🎵 Playlist da Batalha")

components.html(html_code, height=420)

# Botão para iniciar nova batalha
if st.button("🔥 Iniciar nova batalha"):
    try:
        user = auth.sign_in_with_email_and_password(email, senha)
        db = firebase.database()
        db.child("batalha_estado").update({"nova_batalha": True}, user['idToken'])
        st.success("✅ Batalha sinalizada com autenticação!")
    except Exception as e:
        st.error(f"❌ Erro ao sinalizar batalha: {e}")