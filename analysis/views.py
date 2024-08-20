from django.shortcuts import render
from .forms import TextInputForm
import spacy
#from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import seaborn as sns
from io import BytesIO
import base64

nltk.download('punkt')
nltk.download('stopwords')

class TextAnalysisApp:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))

    def extract_keywords(self, text):
        word_tokens = word_tokenize(text)
        filtered_text = [w for w in word_tokens if w not in self.stop_words]
        return filtered_text[:5]

    def get_sentiment_score(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def generate_word_cloud(self, text):
        wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(str(text))
        plt.figure(figsize=(10, 7))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis('off')
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')

    def display_entity_distribution(self, ents):
        labels = [ent.label_ for ent in ents]
        counts = {label: labels.count(label) for label in labels}
        fig, ax = plt.subplots()
        ax.pie(counts.values(), labels=list(counts.keys()), autopct='%1.1f%%')
        ax.axis('equal')
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')

    def display_dependency_graph(self, doc):
        edges = []
        for token in doc:
            for child in token.children:
                edges.append(('{0}-{1}'.format(token.lower_, token.i), '{0}-{1}'.format(child.lower_, child.i)))

        graph = nx.Graph(edges)
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", alpha=0.6, edge_color="gray", font_size=10, font_color="black", font_weight="bold")
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')

def analyze_text(request):
    form = TextInputForm()
    analysis_results = None
    if request.method == 'POST':
        form = TextInputForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            uploaded_file = form.cleaned_data.get('file')

            if uploaded_file:
                text = uploaded_file.read().decode('utf-8')

            if text:
                app = TextAnalysisApp()
                doc = app.nlp(text)
                word_cloud = app.generate_word_cloud(text)
                dep_graph = app.display_dependency_graph(doc)
                entity_dist = app.display_entity_distribution(doc.ents)
                analysis_results = {
                    'word_cloud': word_cloud,
                    'dep_graph': dep_graph,
                    'entity_dist': entity_dist,
                    'pos_data': [(token.text, token.pos_, token.dep_, token.head.text) for token in doc],
                    'keywords': app.extract_keywords(text),
                    'sentiment': app.get_sentiment_score(text),
                }
    return render(request, 'analysis/analyze_text.html', {'form': form, 'analysis_results': analysis_results})
