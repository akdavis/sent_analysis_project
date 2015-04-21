##Andrea Davis##

##Baseline Positive/Negative Classifier##

#the directory file that is to be run through the classifier#

directory_file = '/Users/akdavis/documents/workspace/mypythonprograms/movie-reviews-test'


pos_words = set(['good/JJ', 'great/JJ', 'fabulous/JJ', 'fantastic/JJ', 'brilliantly/RB', 'rocked/VBD',
                 'beauty/NN', 'sensational/JJ', 'faultless/JJ', 'masterpiece/NN', 'grace/NN',
                 'best/JJS', 'loved/VBD', 'excellent/JJ', 'greatest/JJS', 'exciting/VBG', 'original/JJ', 'perfect/JJ',
                 'perfection/NN', 'fun/JJ'])
neg_words = set(['bad/JJ', 'awful/JJ', 'horrible/JJ', 'sucks/VBZ', 'stupid/JJ','ridiculous/JJ', 'dumb/JJ', 'empty/JJ',
                 'worst/JJS', 'hated/VBD', 'waste/NN', 'boring/JJ', 'predictable/JJ', 'moronic/JJ', 'idiotic/JJ', 'disgusted/VBN',
                 'detested/VBD', 'repelled/VBD', 'crappiest/JJS', 'lousy/JJ'])

#input to the function is one movie review
#a movie review is a string 
#given the review, assign the label positive or negative
def base_classifier(review):
        pos_count = 0
        neg_count = 0
        #split the review string into words
        review_words = review.split()
        for word in review_words:
                if word in pos_words:
                        pos_count +=1
                elif word in neg_words:
                        neg_count +=1
        if pos_count > neg_count:
                return 1
        elif neg_count > pos_count:
                return -1
        else: #it's a tie
                return 0

#get file list        
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


testing = get_file_list_recursive(directory_file)

num_corr = 0
total = 0
ties = 0



for eachfile in testing:
        if 'pos' in eachfile: #then it's a positive review
                review = open(eachfile, 'r').read()
                clas = base_classifier(review)
                total +=1
                if clas == 1: #it got it right
                        num_corr +=1
                elif clas == 0: #tie
                        ties +=1
        elif 'neg' in eachfile: #then it's a negative review
                review = open(eachfile, 'r').read()
                clas = base_classifier(review)
                total +=1
                if clas == -1: #it got it right
                        num_corr += 1
                elif clas == 0: #tie
                        ties += 1



print 'Number correct is %d'%num_corr
print 'Number of ties is %d'%ties

perc_corr = num_corr*100.0/total

print 'Percent correct is %f'%perc_corr
                        
        
        
