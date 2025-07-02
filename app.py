import streamlit as st
import json
import os
from main import summarize_article_json
from article_extract import extract_article_as_json
import global_var


st.set_page_config(page_title="Greek Article Summarizer", page_icon="🧠")
st.title("📰 Greek Article Summarizer")





# --- Main Article Input ---
url = st.text_input("📎 Επικόλλησε URL άρθρου")
uploaded_file = st.file_uploader("📤 ή Ανέβασε αρχείο JSON", type="json")

# --- Sidebar: Settings Panel ---
with st.sidebar:
    st.header("⚙️ Ρυθμίσεις")

    iterations = st.slider("🔁 Μέγιστες επαναλήψεις", 1, 10, 5)
    global_var.ITERATIONS = iterations

    bold_words = st.radio("Συμπερίληψη bold από άρθρο:", ["Yes", "No"])
    bold = bold_words.startswith("Yes")

    single_model = st.radio("Επιλογή μοντέλου περίληψης:", ["One-node (basic)", "Seven-node (advanced)"])
    single = single_model.startswith("One")

    show_explanations = st.checkbox("🔍 Προβολή επεξηγήσεων όρων", value=True)

    apply_settings = st.button("✔ Επιβεβαίωση ρυθμίσεων")

# --- State ---
article = None
article_preview_ready = False

# --- Output Paths ---
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)
summary_path = os.path.join(output_dir, "summary.txt")
terms_path = os.path.join(output_dir, "terms.txt")
graph_image_path = f"graph_plots/graph1.png" if single else f"graph_plots/graph7.png"

# --- When Settings Confirmed ---
if apply_settings:
    if url:
        try:
            with st.spinner("🔍 Γίνεται λήψη και ανάλυση άρθρου..."):
                article = extract_article_as_json(url, bold=bold)
                st.session_state["article"] = article
                st.success("✅ Άρθρο εξήχθη επιτυχώς")
        except Exception as e:
            st.error(f"⚠️ Σφάλμα κατά την επεξεργασία URL: {e}")

    elif uploaded_file:
        try:
            article = json.load(uploaded_file)
            st.session_state["article"] = article
            st.success("✅ Αρχείο φορτώθηκε επιτυχώς")
        except json.JSONDecodeError:
            st.error("❌ Το αρχείο δεν είναι έγκυρο JSON.")

# --- Optional Preview ---
if "article" in st.session_state:
    if st.button("📄 Προβολή Άρθρου"):
        st.subheader("👁️ Προεπισκόπηση Άρθρου")
        st.json(st.session_state["article"])

# --- Run Summary ---
if "article" in st.session_state and st.button("🧠 Δημιουργία Περίληψης"):
    with st.spinner("✏️ Δημιουργείται η περίληψη..."):
        summarize_article_json(
            article=st.session_state["article"],
            output_path=output_dir,
            single=single
        )

    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = f.read()
        st.success("📄 Η Περίληψη ολοκληρώθηκε!")
        st.subheader("📋 Τελική Περίληψη")
        st.text_area("Περίληψη", summary, height=300)
        st.download_button("📥 Κατέβασε Την Περίληψη", summary, file_name="summary.txt")

    if show_explanations and os.path.exists(terms_path):
        with open(terms_path, "r", encoding="utf-8") as f:
            terms = f.read()
        st.subheader("📘 Όροι & Επεξηγήσεις")
        #print(terms)
        #for line in terms.splitlines():
        st.markdown(terms)
        st.download_button("📥 Κατέβασε Όρους", terms, file_name="terms.txt")

    #if os.path.exists(graph_image_path):
    #    st.subheader("📊 Διάγραμμα Μοντέλου Περίληψης")
    #    st.image(graph_image_path, caption="Διάγραμμα LangGraph", use_column_width=True)
