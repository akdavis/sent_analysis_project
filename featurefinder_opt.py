##extracting the features##

#for each instance, extract features#
#print to file# 



import string
all_ascii = set(string.ascii_letters + string.digits + string.punctuation)

def test_str(s):
   non_ascii = False
   for c in s:
      if c not in all_ascii:
         non_ascii = True
         break
   return non_ascii




##input files##

###training#
##neg_movie_reviews = '/Users/akdavis/documents/workspace/mypythonprograms/movie-reviews/train/neg-train'
##pos_movie_reviews = '/Users/akdavis/documents/workspace/mypythonprograms/movie-reviews/train/pos-train'
##
###validation#
##neg_movie_reviews_va = '/Users/akdavis/documents/workspace/mypythonprograms/movie-reviews/valid/neg-valid'
##pos_movie_reviews_va = '/Users/akdavis/documents/workspace/mypythonprograms/movie-reviews/valid/pos-valid'

#training#
movie_reviews = '/Users/akdavis/documents/workspace/mypythonprograms/movie-reviews/trainNvalid'


#testing#
movie_reviews_test = '/Users/akdavis/documents/workspace/mypythonprograms/movie-reviews-test'


##output files##

###training#

output_files_tr = ['/Users/akdavis/documents/workspace/mypythonprograms/train_unigrams_o5_2015.txt',
                   '/Users/akdavis/documents/workspace/mypythonprograms/train_bigrams_o5_2015.txt',
                   '/Users/akdavis/documents/workspace/mypythonprograms/train_adj_o5_2015.txt',
                   '/Users/akdavis/documents/workspace/mypythonprograms/train_top_unigrams_o5_2015.txt',
                   '/Users/akdavis/documents/workspace/mypythonprograms/train_unis_pos_o5_2015.txt']
##
###validation#
output_files_va = ['/Users/akdavis/documents/workspace/mypythonprograms/test_unigrams_o5_2015.txt',
                   '/Users/akdavis/documents/workspace/mypythonprograms/test_bigrams_o5_2015.txt',
                   '/Users/akdavis/documents/workspace/mypythonprograms/test_adj_o5_2015.txt',
                   '/Users/akdavis/documents/workspace/mypythonprograms/test_top_unigrams_o5_2015.txt',
                   '/Users/akdavis/documents/workspace/mypythonprograms/test_unis_pos_o5_2015.txt']

#minimal frequency of ngrams to qualify for inclusion in the feature set
ngram_freq = 5

import os

def get_file_list_recursive(rootdir):

   filelist = []
   def aux(junk, dirpath, namelist):
       for name in namelist:
           file = os.path.join(dirpath, name)
           if os.path.isdir(file)==False:
               filelist.append(file)

   os.path.walk(rootdir, aux, None)

   filelist = [fi.replace('\\','/') for fi in filelist]

   return filelist

##neg_train = get_file_list_recursive(neg_movie_reviews)
##pos_train = get_file_list_recursive(pos_movie_reviews)
##all_train = neg_train + pos_train
##
##neg_valid = get_file_list_recursive(neg_movie_reviews_va)
##pos_valid = get_file_list_recursive(pos_movie_reviews_va)
##all_valid = neg_valid + pos_valid

all_train = get_file_list_recursive(movie_reviews)

all_test = get_file_list_recursive(movie_reviews_test)

code = {} #this is where code numbers for features is stored

#put all unigrams into the dictionary unigrams
#all bigrams in the dictionary bigrams
#all unigrams + pos into the dictionary unigrams-pos
#all adjectives in the dictionary adjectives
#all the in the dictionary top-unigrams
#run this ONLY for training files, NOT validation files
def feature_finder(all_train):

   unigrams_pos = {}
   unigrams = {}
   bigrams = {}
   adjectives = {}
   for eachfile in all_train:
        
        if '.DS_Store' in eachfile:#discard it
           print 'discarded%s'%eachfile
           all_train.remove(eachfile)
         
        else:
           #read the file as a string
           review = open(eachfile, 'r').read()
        
           #split into words
           unis = review.split()


                 
           for i in range(len(unis)): # for each word
              uni = unis[i]
           
              #add to unigrams_pos dictionary
              unigrams_pos[uni] = unigrams_pos.get(uni, 0) + 1

              #add to bigrams dictionary
              if i < len(unis) - 1:
                             bi1 = unis[i].rsplit('/', 1)[0] #remove tag
                             bi2 = unis[i+1].rsplit('/', 1)[0] #remove tag
                             bi = bi1 + ' ' + bi2
                             bigrams[bi] = bigrams.get(bi, 0) + 1
                             


           
              #get adjectives, and put into adjectives dictionary
              if 'JJ' in uni:#it's an adjective
                             adj = uni.rsplit('/', 1)[0] #remove tag
                             adjectives[adj] = adjectives.get(adj, 0) + 1
                             
              #add to unigrams dictionary
              word = uni.split('/', 1)[0] #split uni into pos tag and words(s)
              unigrams[word] = unigrams.get(word, 0) +1 #put word part into unigrams       



   print 'pairing down features'
                #get rid of all unigrams with frequency less than ngram_freq
   freq_unis = []
   for uni in unigrams.keys():
              if unigrams[uni] >= ngram_freq:
                    #put into the list
                    freq_unis.append(uni)

   freq_unigrams = set(freq_unis)

   N = len(freq_unigrams)

#get rid of unigrams-pos not in freq-unigrams

   freq_unis_pos = []
   
   for uni in unigrams_pos.keys():
              word = uni.rsplit('/', 1)[0] #take off pos tag
              if word in unigrams.keys():
                 freq_unis_pos.append(uni)

   freq_unigrams_pos = set(freq_unis_pos)
   

#get rid of all adjectives with frequency less than ngram_freq

   freq_adjs = []

   for adj in adjectives.keys():
              if adjectives[adj] >= ngram_freq:
                 #put into the list
                 freq_adjs.append(adj)

   freq_adjectives = set(freq_adjs)

   M = len(freq_adjectives)
           
         


#get N most frequent bigrams


   bis = [(v, k) for k, v in bigrams.items()]
   bis.sort() #less frequent items are first
   bis.reverse() #more frequent items are first
   bis2 = bis[:N] #get the N most frequent bigrams

   freq_bis = []
   for bi in bis2:
              freq_bis.append(bi[1])

   freq_bigrams = set(freq_bis)

#get M most frequent unigrams

   uni_pairs = [(v, k) for k, v in unigrams.items()]
   uni_pairs.sort() #less frequent items are first
   uni_pairs.reverse() #more frequent items are first
   uni_pairs2 = uni_pairs[:M] #get the N most frequent bigrams
           

   freq_unis = []
   for uni in uni_pairs2:
              freq_unis.append(uni[1])

   top_unigrams = set(freq_unis)


#make a dictionary of items with a unique number for each
   all_items = list(freq_unigrams) + list(freq_bigrams) + list(freq_adjectives) + list(freq_unigrams_pos) + list(top_unigrams)

   i = 1
   for item in all_items:
              code[item] = i
              i +=1

   return (freq_unigrams, freq_unigrams_pos, freq_adjectives, freq_bigrams, top_unigrams)


features = feature_finder(all_train)

print 'Number of unigrams features:%d'%len(features[0])
print 'Number of unigram pos features: %d'%len(features[1])
print 'Number of adjective features: %d'%len(features[2])
print 'Number of bigram features: %d'%len(features[3])
print 'Number of top unigram features: %d'%len(features[4])
                                          

#make lists of strings
#each string begins with +1 (positive) or -1 (negative)
#then has a series of features, of the format <value>:<feature>, where value=1
#ends with \n
#each list will have a different set of features, or combination of features
#each list represents one instance

#all_train is a list of files, output_files is a list of files, features is a tuple of feature sets
#finds features in individual instances that were selected in feature_finder (eg, top bigrams are based on the entire corpus of instances)
#translates them to SVM-light readable format: <feature>:<value>
#<value> in this case is binary, either 1 or left out (SVM-light doesn't need features with a value of 0 represented)
def feature_extract(all_train, output_files, features): #rename - make_svmlight_compatible_files_with_desired_features

   #
   freq_unigrams = features[0]
   freq_unigrams_pos = features[1]
   freq_adjectives = features[2]
   freq_bigrams = features[3]
   top_unigrams = features[4]

   train_unigrams = output_files[0]
   train_bigrams = output_files[1]
   train_adj = output_files[2]
   train_top_unigrams = output_files[3]
   train_unis_pos = output_files[4]

   

   #
   uni_pos_features = []
   uni_features = []
   pos_features = []
   adjective_features = []
   bi_features = []
   top_unis_features = []
   for eachfile in all_train:
        #read the file as a string
        review = open(eachfile, 'r').read()
        #split into words, get only unique items
        unis = review.split()
        #start lists for each feature type, or set of features
        uni_pos_L = []
        uni_L = []
        pos_L = []
        adj_L = []
        bi_L = []
        top_L = []
        

        for i in range(len(unis)): #for each word/pos in the review
           uni = unis[i]
           
           #extract the POS unigrams#
           if uni in freq_unigrams_pos:
              uni_pos_L.append(code[uni])
              
            #extract the bigrams
           if i < len(unis) - 1: 
                             bi1 = unis[i].rsplit('/', 1)[0] #remove tag
                             bi2 = unis[i+1].rsplit('/', 1)[0] #remove tag
                             bi = bi1 + ' ' + bi2
                             if bi in freq_bigrams:
                                bi_L.append(code[bi])
                             


           
           #extract adjectives
           if 'JJ' in uni:#it's an adjective
              adj = uni.rsplit('/', 1)[0] #remove tag
              if adj in freq_adjectives:
                 adj_L.append(code[adj])
                 
           #extract unigrams
           word = uni.split('/', 1)[0] #split uni into pos tag and words(s)
           if word in freq_unigrams:
              uni_L.append(code[word])

           #extract the top unigrams
           if word in top_unigrams:
              top_L.append(code[word])
            


        uni_pos_L = list(set(uni_pos_L))
        uni_pos_L.sort()
        uni_pos_s = ''
        for each in uni_pos_L:
           uni_pos_s += ' %d:1'%each
           
        uni_L = list(set(uni_L))
        uni_L.sort()
        uni_s = ''
        for each in uni_L:
           uni_s += ' %d:1'%each
           
        pos_L = list(set(pos_L))
        pos_L.sort()
        pos_s = ''
        for each in pos_L:
           pos_s += ' %d:1'%each
           
        adj_L = list(set(adj_L))
        adj_L.sort()
        adj_s = ''
        for each in adj_L:
           adj_s += ' %d:1'%each
           
        bi_L = list(set(bi_L))
        bi_L.sort()
        bi_s = ''
        for each in bi_L:
           bi_s += ' %d:1'%each
           
        top_L = list(set(top_L))
        top_L.sort()
        top_s = ''
        for each in top_L:
           top_s += ' %d:1'%each

        uni_pos_s += '\n'
        uni_s += '\n'
        pos_s += '\n'
        adj_s += '\n'
        bi_s += '\n'
        top_s += '\n'

        if 'pos' in eachfile: #it's a positive review
           uni_pos_s = '+1' + uni_pos_s
           uni_s = '+1' + uni_s
           pos_s = '+1'+ pos_s
           adj_s = '+1' + adj_s
           bi_s = '+1' + bi_s
           top_s = '+1' + top_s

        else: #it's a negative review
           uni_pos_s = '-1' + uni_pos_s
           uni_s = '-1' + uni_s
           pos_s = '-1'+ pos_s
           adj_s = '-1' + adj_s
           bi_s = '-1' + bi_s
           top_s = '-1' +top_s
         #add strings to lists
        uni_pos_features.append(uni_pos_s)
        uni_features.append(uni_s)
        pos_features.append(pos_s)
        adjective_features.append(adj_s)
        bi_features.append(bi_s)
        top_unis_features.append(top_s)

   print 'writing to output files'


   tr_unis = open(train_unigrams, 'w')

   for instance in uni_features:
      tr_unis.write(instance)

   tr_unis.close()


   tr_bis = open(train_bigrams, 'w')

   for instance in bi_features:
      tr_bis.write(instance)

   tr_bis.close()


   tr_adj = open(train_adj, 'w')

   for instance in adjective_features:
      tr_adj.write(instance)

   tr_adj.close()



   tr_top_unis = open(train_top_unigrams, 'w')

   for instance in top_unis_features:
      tr_top_unis.write(instance)

   tr_top_unis.close()



   tr_unis_pos = open(train_unis_pos, 'w')

   for instance in uni_pos_features:
      tr_unis_pos.write(instance)

   tr_unis_pos.close()



feature_extract(all_train, output_files_tr, features)

#feature_extract(all_train, output_files_va, features)









