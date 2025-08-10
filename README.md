# Bias_Detector_in_NewsStory
🕵️ Societal Bias Detector
The Societal Bias Detector is a Streamlit-based interactive web app that analyzes political, gender, and cultural biases in news articles or documents. It uses NLP (spaCy) to detect bias-indicative words, provides color-coded highlights, visual summaries, and generates a word cloud of biased terms.

🚀 Features
📥 Multiple Input Methods

Paste text directly into the app.

Upload PDF files (auto text extraction).

🔍 Bias Detection

Detects political (left/right) bias words.

Detects gender (male/female) bias stereotypes.

Detects cultural (Western/Non-Western) bias terms.

🎨 Interactive Visuals

Highlighted text with category-based colors and tooltips.

Bar chart showing counts of bias words per category.

Summary table with explanations of each bias type.

Word cloud of most frequent biased terms.

📄 PDF Support

Automatically extracts text from uploaded PDF news stories.

🛠️ Tech Stack
Frontend & App Framework: Streamlit

NLP Processing: spaCy

Data Visualization: Matplotlib, Seaborn

Word Cloud Generation: WordCloud library

PDF Parsing: PyMuPDF (fitz)

📊 Bias Categories
Category	Example Keywords	Description
Political Left	progressive, liberal, woke	Progressive or liberal ideologies
Political Right	conservative, patriot, freedom	Conservative or traditionalist viewpoints
Gender Female	emotional, beautiful, weak	Common gender stereotypes for women
Gender Male	strong, logical, aggressive	Common gender stereotypes for men
Cultural Western	modern, advanced, scientific	Positive framing of Western culture
Cultural Non-Western	primitive, exotic, inferior	Negative framing of non-Western culture

📌 Example Output
Colored Text Highlights — See exactly where bias appears in your text.

Bar Chart — Compare categories of detected biases visually.

Word Cloud — View frequently occurring biased terms at a glance.

Author:
Atharva Hanchate
