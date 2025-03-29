import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Sample intent data
intent_data = [
    ("show me cheap smartphones", "FindProduct"),
    ("compare iPhone 15 and Samsung S24", "CompareProducts"),
    ("what are the latest laptops", "FindProduct"),
]

# Train simple intent classifier
X_train = [x[0] for x in intent_data]
y_train = [x[1] for x in intent_data]

vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)

classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)

# Save model
with open("models/intent_classifier.pkl", "wb") as f:
    pickle.dump((vectorizer, classifier), f)

# Load NLP model for entity recognition
nlp = spacy.load("en_core_web_sm")

def parse_intent(query):
    vectorizer, classifier = pickle.load(open("models/intent_classifier.pkl", "rb"))
    intent = classifier.predict(vectorizer.transform([query]))[0]
    return intent

def extract_entities(query):
    doc = nlp(query)
    entities = {ent.label_: ent.text for ent in doc.ents}
    return entities

# Example
query = "find a cheap smartphone with a good camera"
print("Intent:", parse_intent(query))
print("Entities:", extract_entities(query))
