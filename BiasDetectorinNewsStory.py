import streamlit as st
import spacy
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import fitz  # PyMuPDF
import threading
from matplotlib.backends.backend_agg import RendererAgg
import io

_lock = threading.Lock()
nlp = spacy.load("en_core_web_sm")

# Bias lexicons
political_bias_words = {
    'left': ['progressive', 'liberal', 'woke', 'inclusive','socialist','social justice','anti-racist',
             'equity','intersectional','climate action','defund','safe space','diversity','inclusivity'],
    'right': ['conservative', 'patriot', 'traditional', 'freedom','nationalist','law and order','pro-life','traditional values',
              'tax relief','border security','anti-globalist','gun rights','family values','Christian nation']
}

gender_bias_words = {
    'female': ['emotional', 'hysterical', 'bossy', 'beautiful','nurturing','passive',
               'delicate','dramatic','vain','weak','flirtatious','intuitive','gentle','dependent'],
    'male': ['strong', 'rational', 'aggressive', 'leader','dominant','unemotional','stoic','assertive','breadwinner','decisive',
             'fearless','powerful','logical','rugged',]
}

cultural_bias_words = {
    'western': ['civilized', 'developed', 'modern','enlightened','first-world','advanced','efficient',
                'global standard','superior','leading','objective','scientific','structured'],
    'non-western': ['primitive', 'tribal', 'backward','exotic','undeveloped','chaotic','mystical',
                    'superstitious','barbaric','inferior','submissive','corrupt','authoritarian']
}

combined_lexicon = {
    'political_left': political_bias_words['left'],
    'political_right': political_bias_words['right'],
    'gender_female': gender_bias_words['female'],
    'gender_male': gender_bias_words['male'],
    'cultural_western': cultural_bias_words['western'],
    'cultural_non-western': cultural_bias_words['non-western']
}

bias_explanations = {
    'political_left': 'Words often associated with progressive or liberal ideologies.',
    'political_right': 'Words often linked to conservative or traditionalist viewpoints.',
    'gender_female': 'Stereotypical terms commonly used to describe women, often unfairly.',
    'gender_male': 'Stereotypical traits associated with masculinity or male dominance.',
    'cultural_western': 'Words praising Western customs or culture.',
    'cultural_non-western': 'Words portraying non-Western traditions negatively.'
}

# ---- Core Functions ---- #
def analyze_bias(text):
    doc = nlp(text.lower())
    bias_counts = defaultdict(int)
    word_annotations = []
    biased_words = []

    for token in doc:
        word = token.text
        bias_tag = None
        for bias_type, keywords in combined_lexicon.items():
            if word in keywords:
                bias_counts[bias_type] += 1
                bias_tag = bias_type
                biased_words.append(word)
                break
        word_annotations.append((word, bias_tag))
    return bias_counts, word_annotations, biased_words

def highlight_biased_text(word_annotations):
    bias_labels = {
        'political_left': ('#88e1f2', '🟦 Left Bias'),
        'political_right': ('#ff9999', '🟥 Right Bias'),
        'gender_female': ('#dda0dd', '💜 Female Bias'),
        'gender_male': ('#add8e6', '💙 Male Bias'),
        'cultural_western': ('#c6efce', '🌍 Western Bias'),
        'cultural_non-western': ('#ffc7ce', '🌏 Non-Western Bias')
    }
    highlighted = []
    for word, tag in word_annotations:
        if tag:
            color, label = bias_labels.get(tag, ('#ffffcc', 'Bias'))
            highlighted.append(f"<span style='background-color:{color}; padding:2px; border-radius:3px;' title='{label}'>{word}</span>")
        else:
            highlighted.append(word)
    return " ".join(highlighted)

def plot_bias(bias_counts):
    if not bias_counts:
        st.info("No bias-indicative words detected.")
        return
    df = pd.DataFrame(list(bias_counts.items()), columns=['Bias_Type', 'Count'])
    with _lock:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df, x="Bias_Type", y="Count", palette="coolwarm", ax=ax)
        ax.set_title("Detected Bias by Category")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

def display_bias_summary(bias_counts):
    if not bias_counts:
        return
    st.markdown("### 🧾 Bias Summary Table")
    summary = [{"Bias Category": f"{icon} {k.replace('_', ' ').title()}",
                "Explanation": bias_explanations[k],
                "Detected Words": v}
               for k, v in bias_counts.items()
               for icon in ["✅"]]
    df = pd.DataFrame(summary)
    st.dataframe(df)

def generate_wordcloud(words):
    if not words:
        return
    text = " ".join(words)
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    with _lock:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ---- Streamlit UI ---- #
st.set_page_config(page_title="Societal Bias Detector", layout="wide")

st.title("🕵️ Societal Bias Detector in News Stories")
st.markdown("Analyze **political**, **gender**, and **cultural** bias in news articles or uploaded PDFs. Get insightful feedback with interactive visuals.")

# Input
input_method = st.radio("📥 Choose Input Method", ["📝 Paste Text", "📄 Upload PDF"], horizontal=True)

user_input = ""
if input_method == "📝 Paste Text":
    user_input = st.text_area("✏️ Enter News Text Below:", height=200, placeholder="Type or paste a news article here...")
elif input_method == "📄 Upload PDF":
    uploaded_file = st.file_uploader("📄 Upload a PDF file", type=["pdf"])
    if uploaded_file:
        user_input = extract_text_from_pdf(uploaded_file)

# Analyze button
if st.button("🔍 Analyze Bias"):
    if not user_input.strip():
        st.warning("🚨 Please enter or upload some text to analyze.")
    else:
        with st.spinner("⏳ Analyzing for societal bias..."):
            bias_counts, annotations, biased_words = analyze_bias(user_input)
            st.success("✅ Analysis Complete!")

            st.markdown("---")
            st.markdown("## 🖍️ Highlighted Biased Text")
            st.markdown("Words detected as biased are color-coded and explained with hover tooltips.")
            st.markdown(highlight_biased_text(annotations), unsafe_allow_html=True)

            st.markdown("---")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("## 📊 Bias Category Breakdown")
                st.markdown("This bar chart shows the number of detected words in each bias category.")
                plot_bias(bias_counts)

            with col2:
                st.markdown("## 🧾 Bias Summary Table")
                display_bias_summary(bias_counts)

            st.markdown("---")
            st.markdown("## ☁️ Word Cloud of Biased Words")
            st.markdown("See which words contribute most frequently to detected biases.")
            generate_wordcloud(biased_words)
