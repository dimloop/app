
import os
import json
import streamlit as st

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

    # ————— Pipeline parameters —————
    iterations = st.slider("🔁 Μέγιστες επαναλήψεις", 1, 10, global_var.ITERATIONS)
    global_var.ITERATIONS = iterations

    bold_words = st.radio("Συμπερίληψη bold από άρθρο:", ["Yes", "No"])
    bold = bold_words.startswith("Yes")


    model = st.radio("Επιλογή μοντέλου περίληψης:", ["1-node", "7-node", "8-node"])
    #single = single_model.startswith("One")

    show_explanations = st.checkbox("🔍 Προβολή επεξηγήσεων όρων", value=True)

    st.markdown("---")

    # ————— LLM provider + model —————
    provider = st.radio("LLM provider:",
                        ["OpenAI", "Claude", "Gemini"],
                        horizontal=True)
    custom_model = st.text_input("🔤 (Προαιρετικά) όνομα μοντέλου",
                                 placeholder="Leave blank for default")
    temperature = st.slider("🌡️ Temperature", 0.0, 1.0, 0.2)

    apply_settings = st.button("✔ Επιβεβαίωση ρυθμίσεων")

# ---------------------------------------------------------------------
# Paths & in-memory state
# ---------------------------------------------------------------------
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)
summary_path = os.path.join(output_dir, "summary.txt")

terms_path = os.path.join(output_dir, "terms.txt")
#graph_image_path = f"graph_plots/graph1.png" if single else f"graph_plots/graph7.png"

# ---------------------------------------------------------------------
# Handle the “Apply settings” click
# ---------------------------------------------------------------------
if apply_settings:
    # 1️⃣ Swap the active LLM for the whole app  -----------------------
    try:
        import config               # local import to avoid circular refs
        config.llm = config.get_llm(
            provider=provider.lower(),
            model=custom_model or None,
            temperature=temperature,
        )
        st.toast(f"✅ Χρησιμοποιείται τώρα {provider}"
                 + (f' / “{custom_model}”' if custom_model else " (προεπιλογή)"))
    except Exception as e:
        st.error(f"❌ Αποτυχία ρύθμισης LLM: {e}")

    # 2️⃣ Ingest the article ------------------------------------------
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

# ---------------------------------------------------------------------
# Optional article preview
# ---------------------------------------------------------------------
if "article" in st.session_state and st.button("📄 Προβολή Άρθρου"):
    st.subheader("👁️ Προεπισκόπηση Άρθρου")
    st.json(st.session_state["article"])

# ---------------------------------------------------------------------
# Run the summarization pipeline
# ---------------------------------------------------------------------
if "article" in st.session_state and st.button("🧠 Δημιουργία Περίληψης"):
    with st.spinner("✏️ Δημιουργείται η περίληψη..."):
        summarize_article_json(
            article=st.session_state["article"],
            output_path=output_dir,
            model=model
        )

    # ---------- Display results ----------
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = f.read()

        st.success("📄 Η Περίληψη ολοκληρώθηκε!")
        st.subheader("📋 Τελική Περίληψη")
        st.text_area("Περίληψη", summary, height=300)
        st.download_button("📥 Κατέβασε Την Περίληψη",
                           summary,
                           file_name="summary.txt")

    if show_explanations and os.path.exists(terms_path):
        with open(terms_path, "r", encoding="utf-8") as f:
            terms = f.read()

        st.subheader("📘 Όροι & Επεξηγήσεις")
        st.markdown(terms)
        st.download_button("📥 Κατέβασε Όρους",
                           terms,
                           file_name="terms.txt")

    #if os.path.exists(graph_image_path):
    #    st.subheader("📊 Διάγραμμα Μοντέλου Περίληψης")
    #    st.image(graph_image_path, caption="Διάγραμμα LangGraph", use_column_width=True)
