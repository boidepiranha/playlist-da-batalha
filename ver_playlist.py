import streamlit as st
import streamlit.components.v1 as components

playlist_id = "PLCcM9n2mu2uHA6fuInzsrEOhiTq7Dsd97"

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
