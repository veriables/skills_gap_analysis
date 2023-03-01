import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import MWETokenizer
import os
import re
import ObjListOfTokens as atl
import ObjTokensToSkills as sl

class JobPostings:
    def __init__(self, job_posting_dir, additional_stopwords_file):
        self.job_posting_dir = job_posting_dir
        self.additional_stopwords_file = additional_stopwords_file
        self.raw_additional_stop_words = []
        self.final_stop_words = []
        self.job_posting_file_names = []
        self.text = ""
        self.clean_text = ""
        self.tokens = []
        self.token_counts = {}
        self.skill_counts = {}

    def getJobPostingFileNames(self):
        '''
            Opens the /data/job_postings_data directory
            and lists all the files inside it storing
            their filenames in self.job_posting_file_names.
        '''
        for name in os.listdir(self.job_posting_dir):
            if name != '.DS_Store':
                f = os.path.join(self.job_posting_dir, name)
                if os.path.isfile(f):
                    self.job_posting_file_names.append(f)

    def extractTextFromFiles(self):
        '''
            Build a large text string containing all the text
            from the files in the /data/job_postings_data 
            directory.  That text string is stored in self.text.
        '''
        for filepath in self.job_posting_file_names:
            with open(filepath) as f:
                text = f.read()
                text = text.replace('\n',' ')
                self.text += text

    def cleanText(self):
        '''
            Remove punctuation, strip extra whitespace, and
            put all text in lowercase.
        '''
        WHITESPACE = re.compile(r"(?a:\s+)")
        self.clean_text = self.text.replace("("," ")
        self.clean_text = self.clean_text.replace(")"," ")
        self.clean_text = self.clean_text.replace("!", "")
        self.clean_text = self.clean_text.replace("?"," ")
        self.clean_text = self.clean_text.replace("."," ")
        self.clean_text = self.clean_text.replace(":"," ")
        self.clean_text = self.clean_text.replace(";"," ")
        self.clean_text = self.clean_text.replace("/"," ")
        self.clean_text = self.clean_text.replace(","," ")
        self.clean_text = WHITESPACE.sub(" ", self.clean_text)
        self.clean_text = self.clean_text.lower()

    def readStopWordsFile(self):
        '''
            Reads a text file containing any words that we
            want to exclude from the analysis (one word per 
            line). These will be combined with the NLTK list 
            of stop words (which often does not exclude enough 
            words) to form the final list of stop words which 
            will be excluded from analysis.  Returns a list of 
            strings (i.e., words).
        '''
        with open(self.additional_stopwords_file) as file:
            data = file.read()
        words = data.split('\n')
        lowercase_words = []
        for word in words:
            lowercase_words.append(word.lower())
        self.raw_additional_stop_words = lowercase_words

    def buildStopWords(self):
        '''
            Combines the NLTK stopwords with a list of 
            additional stop words defined by the user
            in the /data/stopwords/stop.txt file (one
            word per line).  The final combined list
            of stopwords is stored in 
            self.final_stop_words.
        '''
        nltk_stopwords = stopwords.words('english')
        additional_words = self.raw_additional_stop_words
        self.final_stop_words = nltk_stopwords + additional_words

    def removeStopWords(self):
        '''
            Uses the self.final_stop_words list to remove
            all the stop words from self.text to generate
            a new string which is stored in self.clean_text.
        '''
        clean_words = []
        for word in self.clean_text.split():
            if not word in self.final_stop_words:
                clean_words.append(word)
        self.clean_text = ' '.join(clean_words)

    def tokenizeText(self):
        '''
            Takes the text from self.clean_text and searches
            it for any of the tokens listed in LIST_OF_TOKENS
            list from ObjListOfTokens.  The results are stored
            in self.tokens.
        '''
        tok = MWETokenizer(atl.LIST_OF_TOKENS)
        tokens = tok.tokenize(self.clean_text.split())
        self.tokens = tokens

    def countTokens(self):
        '''
            Iterates over self.tokens and counts how many
            times each token occurred.  The generates a
            dictionary with each token as the key and the 
            number of times it occurred as the value.  This
            dictionary is stored in self.token_counts.
        '''
        for token in self.tokens:
            if self.token_counts.get(token):
                self.token_counts[token] += 1
            else:
                self.token_counts[token] = 1

    def convertTokensToSkills(self):
        '''
            This is, effectively, a translation step.  We
            have token counts, but we need skill counts.
            So we have to translate each token into the 
            associated Skill.  For example, the tokens 
            "sql_server", "mssql", and "t-sql" are all 
            associated with the Skill "Microsoft SQL Server".
            So, this function iterates over the self.token_counts 
            dictionary.  For each token, it looks up the 
            associated Skill in the TOKENS_TO_SKILLS map (loaded 
            from ObjTokensToSkills.py).  Then, it counts the 
            number of times each Skill was mentioned and 
            stores the results in a new dictionary named 
            self.skill_counts.
        '''
        for k, v in self.token_counts.items():
            if sl.TOKENS_TO_SKILLS.get(k):
                skill = sl.TOKENS_TO_SKILLS[k]
                if self.skill_counts.get(skill):
                    self.skill_counts[skill] += v
                else:
                    self.skill_counts[skill] = v

    def run(self):
        '''
            This method simply runs every function in this class
            in the correct order.  It could be called from the
            __init__ method, but, for testing purposes, it is 
            easier to leave it separate.
        '''
        self.getJobPostingFileNames()
        self.extractTextFromFiles()
        self.cleanText()
        self.readStopWordsFile()
        self.buildStopWords()
        self.removeStopWords()
        self.tokenizeText()
        self.countTokens()
        self.convertTokensToSkills()



    
        

