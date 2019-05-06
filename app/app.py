from flask import Flask, request, render_template
from classify_text import classify_text
from wordvector import PreprocessUtil



import gensim
import numpy


app = Flask(__name__)


def get_google_model(model_path):
    '''
    Load wordembeddings model in Binary in gensim format
    :param model_path: path to the model loaded
    :return: model object
    '''
    return gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)


def get_gensim_vectors(tokens, model):
    '''
    Transforms list of tokens in a list of vectors (for each token)
    :param tokens: as a list
    :return: list of vectors for a given word embeddings model
    '''
    list_vec = []
    for token in tokens:
        try:
            list_vec.append(model.word_vec(token))
            # print("vector found <" + token+ ">")
        except KeyError:
            # print("vector not found: <" + token + ">")
            continue  # do nothing
    return list_vec

def document_avg_vector(tokens_vector_list):
    '''
    Averages all word-vectors in a single document-vector representation
    :param tokens_vector_list: list of vectors for each word
    :return: average of all vectors in the given document
    '''
    if len(tokens_vector_list) == 0:
        print('Document cannot be processed. No word embeddings found.')
        exit(-1)  # exit with code -1 (error)
    else:
        return numpy.mean(tokens_vector_list, axis=0)


@app.route('/')
def main_page():
    return render_template("main_page.html")

@app.route('/classify',methods = ['POST', 'GET'])
def classify():
    text = request.form['text']
    # Transforming document into doc_vector
    tokens = preprocess.clean(text)  # clean text - no stopwords, punctuations
    tokens_vector = get_gensim_vectors(tokens, model)  # returns list of vectors - per token
    doc_vector = document_avg_vector(tokens_vector)  # avg of all word-vectors in the document
    doc_vector_labeled = numpy.append(doc_vector, 'UNK')  # dumb label for unseen document - label should not be used
    # we want use 'doc_vector_labeled' for our actual classification
    # try: return classify_text(doc_vector_labeled) (uncomment classify_text in classify_text.py)
    return classify_text(text)


if __name__ == '__main__':
    # object to clean text
    preprocess = PreprocessUtil.Preprocess()  # text pre-processing
    model_folder = '/data/googlenews300d.bin'  # model location

    try:
        model = get_google_model(model_folder)   # word embeddings model
        model_size = model.vector_size  # size of the word embeddings model used
        print('Success: Model loaded - Size: %d dimensions' % model_size)
    except IOError:
        print('Failure: Model not loaded. Check path and file')

    #  WebApp  run
    app.run(debug=True, host='0.0.0.0')