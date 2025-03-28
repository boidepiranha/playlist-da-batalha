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

<script>
  var tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  var player;
  function onYouTubeIframeAPIReady() {{
    player = new YT.Player('player', {{
      height: '394',
      width: '700',
      playerVars: {{
        listType: 'playlist',
        list: '{playlist_id}',
        autoplay: 1,
        controls: 1
      }},
      events: {{
        'onReady': onPlayerReady,
        'onStateChange': onPlayerStateChange
      }}
    }});
  }}

  function onPlayerReady(event) {{
    console.log("🎬 Player pronto");
  }}

  function onPlayerStateChange(event) {{
    // Detecta quando um novo vídeo começa a tocar
    if (event.data === YT.PlayerState.PLAYING) {{
      var index = player.getPlaylistIndex();
      console.log("🎵 Tocando vídeo índice:", index);
      
      // Se for o vídeo de índice 2 (terceiro vídeo), notifica o Firebase
      if (index === 2) {{
        console.log("🚨 Começou o vídeo da contagem regressiva!");

        // Notifica o Firebase
        fetch("{FIREBASE_URL}/batalha_estado.json", {{
          method: "PATCH",
          headers: {{
            "Content-Type": "application/json"
          }},
          body: JSON.stringify({{ nova_batalha: true }})
        }}).then(r => console.log("✅ Firebase atualizado"))
          .catch(e => console.error("❌ Erro no envio para Firebase", e));
      }}
    }}
    
    // Mantém a função original para recarregar quando a playlist terminar
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


