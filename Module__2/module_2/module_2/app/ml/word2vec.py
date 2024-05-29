import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')


def preprocess_text(record: str) -> list[str]:
    # 1. tokenize all
    tokens = word_tokenize(record.lower())
    # 2. remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]

    # 3. stemming /lemmatizing
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

    return stemmed_tokens


# def update_model(model: Word2Vec, pre_processed_text: list[str]) -> None:
    # re-train word2vec model
    # model = Word2Vec(
    #     [pre_processed_text], min_count=1, vector_size=5
    #)
    # model.save("app/ml/word2vec.model")


def generate_embeddings(record: str) -> None:
    pre_processed_text = preprocess_text(record)
    # load model from file
    # word2vec_words = model.wv.index_to_key
    # model.vw
    # embedding_vector = np.array(
    #    [model.vw[word] for word in word2vec_words]
    # )

# record: list[str] -> str
def find_similar_records(x: list, y: list) -> any:
    print('X: ', x)
    print('Y: ', y)

    # X - embedding of record, Y - other embeddings
    # aggregared_emb_for_record = sum(all embedding vectors of the record)
    similarity = cosine_similarity(x, y)
    return similarity
    # return most similar record based on cosine similarity