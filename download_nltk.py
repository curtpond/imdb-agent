import nltk

# Download required NLTK resources
resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
for resource in resources:
    print(f"Downloading {resource}...")
    nltk.download(resource)
print("Done downloading NLTK resources!")
