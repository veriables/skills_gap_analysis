from LoadJobPostingSkills import JobPostings
from LoadApplicantSkills import ApplicantSkills
from SkillsMerge import SkillsMerge
from SkillsAnalysis import SkillsAnalysis
from config import CONFIG

######################################################################
## Build the analysis
######################################################################
jpf = JobPostings(CONFIG['job_postings_dir'], CONFIG['stop_words_file'])
jpf.run()
aps = ApplicantSkills(CONFIG['applicant_skills_file'])
skm = SkillsMerge(jpf.skill_counts, aps.applicant_skill_counts)
skm.run()
sa = SkillsAnalysis(skm.skills_df)
sa.run()

######################################################################
## Build Charts and Export Datasets
######################################################################
sa.plotAll()
sa.plotLowerRightQuandrant()
sa.plotAboveAverageJobPostingSkills()
sa.plotSkillsGapSkillsImportance()

