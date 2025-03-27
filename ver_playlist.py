import streamlit as st

playlist_id = "PLCcM9n2mu2uHA6fuInzsrEOhiTq7Dsd97"
iframe_html = f'''
<iframe width="700" height="394"
        src="https://www.youtube.com/embed/videoseries?list={playlist_id}"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen>
</iframe>
'''

st.title("🎵 Playlist da Batalha")
st.components.v1.html(iframe_html, height=400)
