import csv

class ApplicantSkills():
    def __init__(self, applicant_skills_filepath):
        self.applicant_skills_filepath = applicant_skills_filepath
        self.applicant_skill_counts = {}
        self.skill_counts = []
        self.loadApplicantSkillsFromCsv()
        #self.convertSkillsDictionaryIntoList()

    def loadApplicantSkillsFromCsv(self):
        '''
            This function loads the Applicant Skills and Counts 
            data from a CSV.  The data is stored in a CSV to 
            make it easy for users to manually update the data
            while recording job postings that they found.
            Usually, anything manual is bad, but we don't want
            to build a scraper and end up being banned from
            every job site as the people responsible for their
            unrelenting DDOS attacks.  So, we built this around
            the specific use case of collecting the data manually.
            Sorry!
        '''
        with open(self.applicant_skills_filepath, 'r') as data:
            csv_file_data = csv.DictReader(data)
            for row in csv_file_data:
                dict_row = dict(row)
                obj = {dict_row['Skill']: dict_row['Count']}
                self.skill_counts.append(obj)
                self.applicant_skill_counts[dict_row['Skill']] = int(dict_row['Count'])

#    def convertSkillsDictionaryIntoList(self):
#        '''
#            When we merge this Applicant dataset with the JobPostings
#            dataset, they will be easier to load into a Pandas dataframe
#            if they are both lists of records.  So, we'll just convert
#            this dictionary into a list.
#            Why didn't I just load it into a list to begin with?
#            That's just an artifact of the development process.  I started
#            out with a Dictionary and wasn't sure if I wanted a list
#            or a dictionary.  In the end, a List made more sense.
#        '''
#        for k, v in self.applicant_skill_counts.items():
#            self.skill_counts.append({k: v})


