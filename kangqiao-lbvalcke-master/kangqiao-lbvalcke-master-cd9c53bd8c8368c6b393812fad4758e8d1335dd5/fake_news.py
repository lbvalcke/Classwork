import argparse
import chainer
from chainer import cuda, utils, Variable
import chainer.functions as F
import chainer.links as L
import cPickle as pickle
import json
import numpy as np
import pandas as pd
import random
import re
import string
import sys
import unicodedata
from collections import Counter

# IDEAS:
# Softmax "temperature"
# https://karpathy.github.io/2015/05/21/rnn-effectiveness/
#
# Diff. functions
# http://docs.chainer.org/en/stable/reference/links.html
#
# Basics
# http://docs.chainer.org/en/stable/tutorial/recurrentnet.html

class FooRNN(chainer.Chain):
    '''
    Defines the two layer LSTM. Drops 50% of observations in between
    layers. When called, it creates embedding vectors,
    trains the layers, and returns output embeddings.
    '''
    def __init__(self, n_vocab, n_units, train=True):
        super(FooRNN, self).__init__(  # input must be a link
            embed=L.EmbedID(n_vocab, n_units),
            l1=L.LSTM(n_units, n_units),
            l2=L.LSTM(n_units, n_units),
            l3=L.Linear(n_units, n_vocab),
        ) 
        self.n_vocab = n_vocab
        self.n_units = n_units
        self.train = train

    def reset_state(self):
        self.l1.reset_state()
        self.l2.reset_state()

    def __call__(self, x):
        '''
        Creates RNN when called. 
        '''
        h0 = self.embed(x)
        # NOTE: 50% dropout is *generally* optimal and default
        # This var. can be changed, with ratio=dropout_ratio, to minimize
        # Validation loss. Documentation suggests this may be a
        # good approach
        # http://docs.chainer.org/en/stable/_modules/chainer/functions/noise/dropout.html
        h1 = self.l1(F.dropout(h0, train=self.train))
        h2 = self.l2(F.dropout(h1, train=self.train))
        y = self.l3(F.dropout(h2, train=self.train))
        return y

def read_data(category='b', unit='char', thresh=50):
    '''
    Handles document parsing. Creates vocabulary according to unit input.
    Returns a document composed of indexes, a dictionary that maps indexes 
    to vocabulary words, and a vocabulary.
    '''
    fname = '/project/cmsc25025/uci-news-aggregator/{cat}_article.json'.format(
        cat=category
    )
    raw_doc = []
    with open(fname, 'r') as f:
        for line in f.readlines():
            text = json.loads(line)['text']
            if len(text.split()) >= 100:
                raw_doc.append(
                    unicodedata.normalize('NFKD', text)
                    .encode('ascii', 'ignore').lower()
                    .translate(string.maketrans("\n", " "))
                    .strip()
                )

    raw_doc = ' '.join(raw_doc)

    if unit == 'char':
        vocab = {el: i for i, el in enumerate(set(raw_doc))}
        id_to_word = {i: el for el, i in vocab.iteritems()}
    else: # unit == 'word':
        raw_doc = re.split('(\W+)', raw_doc)
        count = Counter(raw_doc)

        vocab = {}
        ii = 0
        for el in count:
            if count[el] >= thresh:
                vocab[el] = ii
                ii += 1

        id_to_word = {i: el for el, i in vocab.iteritems()}


    doc = [vocab[el] for el in raw_doc if el in vocab]
    print '  * doc length: {}'.format(len(doc))
    print '  * vocabulary size: {}'.format(len(vocab))
    sys.stdout.flush()

    return doc, vocab, id_to_word


def convert(data, batch_size, ii, gpu_id=-1):
    '''
    Converts data into array for use with chainer module functions.
    Creates arrays based on batch size and .
    Type of array depends on whether CPUS or GPUS are being used. 
    '''
    xp = np if gpu_id < 0 else cuda.cupy
    offsets = [t * len(data) // batch_size for t in xrange(batch_size)]
    x = [data[(offset + ii) % len(data)] for offset in offsets]
    x_in = chainer.Variable(xp.array(x, dtype=xp.int32))
    y = [data[(offset + ii + 1) % len(data)] for offset in offsets]
    y_in = chainer.Variable(xp.array(y, dtype=xp.int32))
    return x_in, y_in


def gen_text(model, curr, id_to_word, text_len, gpu_id=-1):
    '''
    Uses trained model to generate fake text. 
    '''
    xp = np if gpu_id < 0 else cuda.cupy

    n_vocab = len(id_to_word)
    gen = [id_to_word[curr]] * text_len
    model.predictor.reset_state()
    for ii in xrange(text_len):
        output = model.predictor(
            chainer.Variable(xp.array([curr], dtype=xp.int32))
        )
        # NOTE: softmax occurs here. I couldn't figure out why they're accessing index 0.
        # If we're going to control softmax temp, we do it here
        p = F.softmax(output).data[0]
        if gpu_id >= 0:
            p = cuda.to_cpu(p)

        # NOTE: This selects from n_vocab based on prob. vector p
        # What would happen if we simply selected the most probable
        # word, or limited the distribution
        curr = np.random.choice(n_vocab, p=p)
        gen[ii] = id_to_word[curr]

    return ''.join(gen)


def main():
    # Parses Function Inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', '-b', type=int, default=2048,
                        help='Number of examples in each mini-batch') # NOTE: play around with this to get maximum GPU utilization
    parser.add_argument('--epoch', '-e', type=int, default=100,
                        help='Number of sweeps over the dataset to train') # NOTE: Keep this var. relatively low while experimenting
    parser.add_argument('--gpu_id', '-g', type=int, default=-1,
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--train_len', '-tl', type=int, default=5000000,
                        help='training doc length') # NOTE: train and valid ~should~ be fine. Can ~maybe~ reduce train_len for speed
    parser.add_argument('--valid_len', '-vl', type=int, default=50000,
                        help='validation doc length')
    parser.add_argument('--gen_len', '-gl', type=int, default=1000,
                        help='generated doc length')
    parser.add_argument('--bp_len', '-bl', type=int, default=30,
                        help='back propagate length') # NOTE: Refers to num batches, NOT num words. See @BP1
    parser.add_argument('--unit', '-u', type=str, default='char',
                        help='type of unit in doc')
    parser.add_argument('--n_units', '-nu', type=int, default=256,
                        help='Number of LSTM units in each layer') # NOTE: Set this manually, > 256. We can probably go much higher with this, but it will be slower
    parser.add_argument('--n_text', '-nt', type=int, default=100,
                        help='Number of generated news')
    parser.add_argument('--output', '-o', type=str, default='output.txt',
                        help='file to write generated txt')
    parser.add_argument('--thresh', '-th', type=int, default=50,
                        help='threshold of words counts for vocabulary') # NOTE: Play around with this, may decrease volatility at the expense of creativity
    args = parser.parse_args()
    
    # Creates variables corresponding to inputs
    gpu_id = args.gpu_id
    n_epoch = args.epoch
    train_len = args.train_len
    valid_len = args.valid_len
    batch_size = min(args.batch_size, args.train_len)

    print "loading doc...."
    sys.stdout.flush()

    doc, vocab, id_to_word = read_data(
      category='b', unit=args.unit, thresh=args.thresh
    )
    n_vocab = len(vocab)

    if train_len + valid_len > len(doc):
        raise Exception(
            'train len {} + valid len {} > doc len {}'.format(
                train_len, valid_len, len(doc)
            )
        )

    # Creates training set and validation set
    train = doc[:train_len]
    valid = doc[(train_len+1):(train_len+1+valid_len)]

    print "initializing...."
    sys.stdout.flush()

    # Initializes model and sets optimization method, default ADAM
    model = L.Classifier(FooRNN(n_vocab, args.n_units, train=True))
    sys.stdout.flush()
    model.predictor.reset_state()
    #optimizer = chainer.optimizers.SGD(lr=1.0)
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    # Adds L2 norm threshold
    optimizer.add_hook(chainer.optimizer.GradientClipping(100))

    if gpu_id >= 0:
        cuda.get_device(gpu_id).use()
        model.to_gpu()

    # main training loop
    print "training loop...."
    sys.stdout.flush()
    xp = np if gpu_id < 0 else cuda.cupy
    for t in xrange(n_epoch):
        train_loss = train_acc = n_batches = loss = 0
        model.predictor.reset_state()
        for i in range(0, len(train) // batch_size + 1): 
            x, y = convert(train, batch_size, i, gpu_id)
            batch_loss = model(x, y)
            loss += batch_loss
            # NOTE: backProp implemented here, bp_len refers to BATCHES, so backprop occurs every bp_len batches @BP1
            if (i+1) % min(len(train) // batch_size, args.bp_len) == 0:
                model.cleargrads()
                loss.backward()
                loss.unchain_backward() # NOTE: truncate backprop
                optimizer.update()
            train_loss += batch_loss.data
            n_batches += 1
        train_loss = train_loss / n_batches
        train_acc = train_acc / n_batches

        # Tests validation set
        valid_loss = valid_acc = n_batches = 0
        for i in range(0, len(valid) // batch_size + 1):
            x, y = convert(valid, batch_size, i, gpu_id)
            batch_loss = model(x, y)
            valid_loss += batch_loss.data
            n_batches += 1
        perplexity = 2 ** (valid_loss)
        valid_loss = valid_loss / n_batches
        valid_acc = valid_acc / n_batches

        print '  * Epoch {} train loss={} valid loss={} perplexity={}'.format(
            t,
            train_loss,
            valid_loss,
            perplexity
        )
        sys.stdout.flush()

        if t >= 1 and xp.abs(train_loss - old_tr_loss) / train_loss < 1e-5:
            print "Converged."
            sys.stdout.flush()
            break

        old_tr_loss = train_loss

    print "generating doc...."
    sys.stdout.flush()
    model.predictor.train = False
    with open(args.output, 'w') as f:
        for ii in xrange(args.n_text):
            start = random.choice(xrange(len(vocab)))
            fake_news = gen_text(
                model,
                start,
                id_to_word,
                text_len=args.gen_len,
                gpu_id=gpu_id
            )
            f.write(fake_news)
            f.write('\n\n\n')

    if gpu_id >= 0:
        model.to_cpu()
    with open('model_%s.pickle' % args.output[:-4], 'wb') as f:
        pickle.dump(model, f, protocol=2)


if __name__ == '__main__':
    main()
