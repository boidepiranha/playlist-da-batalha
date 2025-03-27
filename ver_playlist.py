import streamlit as st
import streamlit.components.v1 as components
import requests

FIREBASE_URL = "https://batalha-musical-default-rtdb.firebaseio.com"
EMAIL = st.secrets["firebase"]["email"]
SENHA = st.secrets["firebase"]["senha"]
API_KEY = st.secrets["firebase"]["apiKey"]

playlist_id = "PLCcM9n2mu2uHA6fuInzsrEOhiTq7Dsd97"

@st.cache_data
def autenticar():
    auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    res = requests.post(auth_url, json={"email": EMAIL, "password": SENHA, "returnSecureToken": True})
    res.raise_for_status()
    return res.json()["idToken"]

def sinalizar_batalha(token):
    url = f"{FIREBASE_URL}/batalha_estado.json?auth={token}"
    res = requests.patch(url, json={"nova_batalha": True})
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
        token = autenticar()
        if sinalizar_batalha(token):
            st.success("✅ Batalha sinalizada com sucesso!")
        else:
            st.error("❌ Falha ao atualizar no Firebase.")
    except Exception as e:
        st.error(f"Erro: {e}")


