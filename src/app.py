from flask import Flask, request, render_template
from wordvector import PreprocessUtil
from wordvector import FileOperations

import gensim
import numpy
import pickle


app = Flask(__name__)


class VectorError(Exception):
    """
    Exception raised for errors during vector processing.
    """

    def __init__(self, message):
        self.message = message


def get_google_model(model_path):
    '''
    Load wordembeddings model in Binary in gensim format
    :param model_path: path to the model loaded
    :return: model object
    '''
    try:
        google_model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
        print('Success: Model loaded - Size: %d dimensions' % google_model.vector_size)
    except IOError:
        print('Failure: Model not loaded. Check path and file')
        exit(-1)  # exit with code -1 (error)
    return google_model


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
        raise VectorError('Document cannot be processed. No word embeddings found.')
    else:
        return numpy.mean(tokens_vector_list, axis=0)

def get_classifier(classifier_path):
    '''
    Load the desired machine learning classifier
    :param classifier_path: classifier object path
    :return: classifier object
    '''
    try:
        ml_model= pickle.load(open(classifier_path, 'rb'))
        print(' Machine learning classifier loaded: %s' % classifier_path)
    except IOError:
        print('Error: Machine learning classifier not loaded.')
        exit(-1)  # exit with code -1 (error)
    return ml_model

@app.route('/')
def main_page():
    return render_template("main_page.html")

@app.route('/classify',methods = ['POST', 'GET'])
def classify():
    text = request.form['text']
    short = (len(text)<250)
    # Transforming document into doc_vector
    tokens = preprocess.clean(text)  # clean text - no stopwords, punctuations
    tokens_vector = get_gensim_vectors(tokens, we_model)  # returns list of vectors - per token
    try:
      doc_vector = document_avg_vector(tokens_vector)  # avg of all word-vectors in the document
      new_label = ml_model.predict([doc_vector])  # predict the label-class for unseen text data

      if new_label == 'mg':
        text = 'Spun: This text was likely paraphrased by a machine!'
      elif new_label == 'og':
        text = 'Original: This text was likely written by a human!'
      else:
        text = 'Something went wrong, I do not know the origin of this text. Sorry.'
    except VectorError:
      text = 'Sorry, we were unable to classify the text you entered.'

    message='Please note that our classifier, just like any other automated approach, can be wrong. Please read the text carefully, watch out for oddities, and make your own decision about the text. '
    warning = ''
    if short:
        warning = '''Please note that the accuracy of our classifier depends on the length of the text. The longer the text, the more accurate the classification will be.
            
            Your text seems to be very short!'''
    return render_template('result_page.html', title=text, message=message, warning=warning)

if __name__ == '__main__':
    # object to clean text
    preprocess = PreprocessUtil.Preprocess()  # text pre-processing
    file_io = FileOperations.FileUtil()  # classifier object

    we_model_folder = '/data/googlenews300d.bin'  # model location
    ml_folder = '/data/svm-model'  # machine learning classifier model

    # # word embeddings models
    we_model = get_google_model(we_model_folder)  # word embeddings model
    model_size = we_model.vector_size  # size of the word embeddings model used
    #
    # # machine learning classifier
    ml_model = get_classifier(ml_folder)

    #  WebApp  run
    app.run(debug=True, host='0.0.0.0')
