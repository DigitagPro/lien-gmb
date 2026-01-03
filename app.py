import streamlit as st
from serpapi import GoogleSearch

# --- CONFIGURATION ---
st.set_page_config(page_title="Lien Avis Google", page_icon="⭐")

# --- TA CLÉ API (Celle que tu as envoyée) ---
# Je l'ai mise ici pour que tu n'aies rien à faire
MA_CLE_SECRETE = "07d69c13788621a9c084603f0f6f019c48a0061dcc7c050138d208a6bdf227c1"

# --- TITRE ---
st.title("⭐ Générateur de lien Avis Client")
st.write("Entre le nom du client, reçois le lien 5 étoiles.")

# --- FORMULAIRE ---
col1, col2 = st.columns(2)
with col1:
    nom = st.text_input("Nom de l'entreprise", placeholder="Ex: Garage Dupont")
with col2:
    ville = st.text_input("Ville", placeholder="Ex: Lyon")

bouton = st.button("Obtenir le lien")

# --- LOGIQUE ---
if bouton and nom:
    try:
        with st.spinner('Recherche du lien magique...'):
            params = {
                "engine": "google_maps",
                "q": f"{nom} {ville}",
                "api_key": MA_CLE_SECRETE,
                "type": "search"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            place_id = None
            nom_trouve = ""

            # On cherche l'ID unique
            if "place_results" in results:
                place_id = results["place_results"]["place_id"]
                nom_trouve = results["place_results"]["title"]
            elif "local_results" in results and len(results["local_results"]) > 0:
                place_id = results["local_results"][0]["place_id"]
                nom_trouve = results["local_results"][0]["title"]
            
            # RÉSULTAT
            if place_id:
                # Voici le lien GMB direct
                lien_final = f"https://search.google.com/local/writereview?placeid={place_id}"
                
                st.success(f"✅ Entreprise trouvée : **{nom_trouve}**")
                st.info("Copie ce lien et envoie-le au client :")
                st.code(lien_final, language="text")
                st.write(f"[👉 Tester le lien ici]({lien_final})")
            else:
                st.error("❌ Entreprise introuvable. Essaie d'ajouter la ville ou de corriger le nom.")

    except Exception as e:
        st.error(f"Petite erreur : {e}")
