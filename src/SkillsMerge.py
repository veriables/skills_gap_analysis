import pandas as pd

class SkillsMerge():
    def __init__(self, job_posting_skills, applicant_skills):
        self.job_posting_skills = job_posting_skills # dict
        self.applicant_skills = applicant_skills # dict
        self.skills = []
        self.skills_counts = {}
        self.skills_records = []
        self.skills_df = None

    def createSkillsKeys(self):
        '''
            Iterate over the job_posting_skills and add all
            the keys to the self.skills dictionary.  Then,
            iterate over the applicant_skills and add any
            keys that don't already exist in self.skills.
        '''
        # Add all the keys from job_posting_skills
        for k, v in self.job_posting_skills.items():
            self.skills.append(k)
        # Add all the keys from applicant_skills
        for k, v in self.applicant_skills.items():
            if k not in self.skills:
                self.skills.append(k)

    def setSkillsCounts(self):
        '''
            Iterate over all the skills listed in the self.skills
            dictionary.  For each one, lookup the number of times
            it was mentioned in the Job Postings and the Applicant
            Profiles.  Create a new object with all three pieces
            of inforamtion and append it to the self.skills_records
            list.
        '''
        for key in self.skills:
            skill = key
            # Lookup the number of times this skill was encountered
            # in the job postings
            job_posting_count = 0
            if self.job_posting_skills.get(skill):
                job_posting_count = self.job_posting_skills[skill]
            # Lookup the number of times this skill was encountered
            # in the applicant profiles
            applicant_count = 0
            if self.applicant_skills.get(skill):
                applicant_count = self.applicant_skills[skill]
            # Build a new object with the skill and two counts
            new_skill_record = {
                'Skill': skill,
                'Job_Posting_Count': job_posting_count,
                'Applicant_Count': applicant_count
            }
            # Append this new object to the self.skills_records 
            # list
            self.skills_records.append(new_skill_record)

    def setSkillsCountsDataframe(self):
        '''
            Create a Pandas DataFrame using the list from
            self.skills_records and save it in self.skills_df
        '''
        self.skills_df = pd.DataFrame.from_records(self.skills_records)

    def run(self):
        '''
            Run each of the functions in this class in the correct 
            order.  This could go in (or be called from) the __init__ 
            method, but leaving it separate makes for easier testing
            of each individual method.
        '''
        self.createSkillsKeys()
        self.setSkillsCounts()
        self.setSkillsCountsDataframe()
