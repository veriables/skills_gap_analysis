import unittest
#import sys
#sys.path.insert(0, '../src')
#sys.path.insert(0, '../config')
from LoadJobPostingSkills import JobPostings
from LoadApplicantSkills import ApplicantSkills
from SkillsMerge import SkillsMerge
from SkillsAnalysis import SkillsAnalysis
from config import CONFIG

class TestSkillsGapAnalysis(unittest.TestCase):

    ################################################################################
    ## Test JobPostings
    ################################################################################
    def test_getJobPostingFileNames(self):
        jpf = JobPostings(CONFIG['test_read_text_dir'], CONFIG['stop_words_file'])
        jpf.getJobPostingFileNames()
        actual = len(jpf.job_posting_file_names)
        expected = 1
        self.assertEqual(actual, expected, "The number of job posting files does not match the number of files in the job_postings directory")

    def test_extractTextFromFile(self):
        jpf = JobPostings(CONFIG['test_read_text_dir'], CONFIG['stop_words_file'])
        jpf.getJobPostingFileNames()
        jpf.extractTextFromFiles()
        actual = jpf.text
        expected = 'Just a Test!  This is another line of the test.'
        self.assertEqual(actual, expected, "The text read from the file does not match the test data")

    def test_cleanText(self):
        jpf = JobPostings(CONFIG['test_clean_text_dir'], CONFIG['stop_words_file'])
        jpf.text = "Just a Test! Well... (I think) This is just a test; could that be a-lie?"
        jpf.cleanText()
        actual = jpf.clean_text
        expected = "just a test well i think this is just a test could that be a-lie "
        self.assertEqual(actual, expected, "The cleaned text does not match the desired outcome")

    def test_readStopWordsFile(self):
        jpf = JobPostings(CONFIG['test_clean_text_dir'], CONFIG['stop_words_file'])
        jpf.readStopWordsFile()
        actual = len(jpf.raw_additional_stop_words)
        expected = 478
        self.assertEqual(actual, expected, "The number of stopwords read does not equal the number of stopwords in the file")

    def test_buildFullStopWordsList(self):
        jpf = JobPostings(CONFIG['test_clean_text_dir'], CONFIG['stop_words_file'])
        jpf.readStopWordsFile()
        jpf.buildStopWords()
        extra_words = len(jpf.raw_additional_stop_words)
        actual = len(jpf.final_stop_words)
        self.assertGreaterEqual(actual, extra_words, "The number of stopwords is not greater than the number of words we added")

    def test_removeStopWords(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.getJobPostingFileNames()
        jpf.extractTextFromFiles()
        jpf.cleanText()
        jpf.readStopWordsFile()
        jpf.buildStopWords()
        jpf.removeStopWords()
        actual = jpf.clean_text
        expected = "microsoft sql server tool business mssql mssql t-sql sql developers sql server"
        self.assertEqual(actual, expected, "The remaining words were not what was expected.")

    def test_tokenizeText(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.getJobPostingFileNames()
        jpf.extractTextFromFiles()
        jpf.cleanText()
        jpf.readStopWordsFile()
        jpf.buildStopWords()
        jpf.removeStopWords()
        jpf.tokenizeText()
        actual = False
        if 'mssql' in jpf.tokens:
            actual = True
        expected = True
        self.assertEqual(actual, expected, "The tokens did not include mssql")

    def test_countTokens(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.getJobPostingFileNames()
        jpf.extractTextFromFiles()
        jpf.cleanText()
        jpf.readStopWordsFile()
        jpf.buildStopWords()
        jpf.removeStopWords()
        jpf.tokenizeText()
        jpf.countTokens()
        actual = jpf.token_counts
        expected = {'microsoft_sql_server': 1, 'tool': 1, 'business': 1, 'mssql': 2, 't-sql': 1, 'sql': 1, 'developers': 1, 'sql_server': 1}
        self.assertEqual(actual, expected, "The counted tokens did not match the expected token counts")

    def test_convertToApplicantSkillCounts(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        actual = jpf.skill_counts
        expected = {'Microsoft SQL Server': 5, 'SQL': 1}
        self.assertEqual(actual, expected, "The skill counts did not match the expected skill counts")

    ################################################################################
    ## Test ApplicantSkills
    ################################################################################
    def test_loadApplicantSkillCounts(self):
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        actual = aps.applicant_skill_counts['Machine Learning']
        expected = 14
        self.assertEqual(actual, expected, "The number of machine learning skills recorded was not 14")

    ################################################################################
    ## Test SkillsMerge
    ################################################################################

    def test_createSkillsKeys(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.createSkillsKeys()
        actual = len(skm.skills)
        expected = 77
        self.assertEqual(actual, expected, "The number of Microsoft SQL Server skills recorded was not 0")

    def test_setSkillsCounts(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.createSkillsKeys()
        skm.setSkillsCounts()
        actual = len(skm.skills_records)
        expected = 77
        self.assertEqual(actual, expected, "The number of skills records does not match the number of keys")

    def test_setSkillsCountsDataframe(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.createSkillsKeys()
        skm.setSkillsCounts()
        skm.setSkillsCountsDataframe()
        num_rows = skm.skills_df.shape[0]
        num_cols = skm.skills_df.shape[1]
        actual = True
        if num_rows != 77:
            actual = False
        if num_cols != 3:
            actual = False
        expected = True
        self.assertEqual(actual, expected, "The shape of the skills DataFrame was not (77,3)")

    ################################################################################
    ## Test SkillsAnalysis
    ################################################################################
    def test_setDescriptiveStatistics(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.run()
        sa = SkillsAnalysis(skm.skills_df)
        sa.setDescriptiveStatistics()
        descriptive_stats = {
            'jpost_mean': -1,
            'jpost_std': -1,
            'jpost_min': -1,
            'jpost_max': -1,
            'app_mean': -1,
            'app_std': -1,
            'app_min': -1,
            'app_max': -1
        }
        descriptive_stats['jpost_mean'] = sa.job_postings_mean
        descriptive_stats['jpost_std'] = sa.job_postings_std
        descriptive_stats['jpost_min'] = sa.job_postings_min
        descriptive_stats['jpost_max'] = sa.job_postings_max
        descriptive_stats['app_mean'] = sa.applicants_mean
        descriptive_stats['app_std'] = sa.applicants_std
        descriptive_stats['app_min'] = sa.applicants_min
        descriptive_stats['app_max'] = sa.applicants_max
        actual = True
        for k, v in descriptive_stats.items():
            if v == -1:
                actual = False
        expected = True
        self.assertEqual(actual, expected, "At least one descriptive statistic was not set")

    def test_dropZeroedData(self):
        jpf = JobPostings(CONFIG['job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.run()
        sa = SkillsAnalysis(skm.skills_df)
        sa.setDescriptiveStatistics()
        sa.dropZeroedData()
        df = sa.data[sa.data['Sum'] == 0]
        actual = df.shape
        expected = (0,4)
        self.assertEqual(actual, expected, "The shape of the rows where JobPosting and Applicant counts were both zero is not (0,0))")

    def test_normaliseScores(self):
        jpf = JobPostings(CONFIG['test_job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.run()
        sa = SkillsAnalysis(skm.skills_df)
        sa.run()
        actual = sa.data.shape
        expected = (77,6)
        self.assertEqual(actual, expected, "The dataframe does not contain 77 rows and six columns")

    def test_plotAll(self):
        jpf = JobPostings(CONFIG['job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.run()
        sa = SkillsAnalysis(skm.skills_df)
        sa.run()
        sa.plotAll()

    def test_plotLowerRightQuandrant(self):
        jpf = JobPostings(CONFIG['job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.run()
        sa = SkillsAnalysis(skm.skills_df)
        sa.run()
        sa.plotLowerRightQuandrant()

    def test_plotAboveAverageJobPostingSkills(self):
        jpf = JobPostings(CONFIG['job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.run()
        sa = SkillsAnalysis(skm.skills_df)
        sa.run()
        sa.plotAboveAverageJobPostingSkills()

    def test_plotSkillsGapSkillsImportance(self):
        jpf = JobPostings(CONFIG['job_postings_dir'], CONFIG['stop_words_file'])
        jpf.run()
        aps = ApplicantSkills(CONFIG['applicant_skills_file'])
        skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
        skm.run()
        sa = SkillsAnalysis(skm.skills_df)
        sa.run()
        sa.plotSkillsGapSkillsImportance()
        
unittest.main()
