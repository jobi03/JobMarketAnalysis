# Job Market Analysis

This project consists of testing the three major skills: collecting data by scraping a website, using natural language processing, and building a binary classifier.

I collected salary information on data science jobs in the Indeed Australia only. Then using the location, title, and summary of the job I attempted to predict the salary of the job. For job posting sites, this would be extraordinarily useful. While most listings do not come with salary information, being to able extrapolate or predict the expected salaries from other listings can be useful.

I also determined if each job’s salary is high and low based on average salary from payscale.com. Normally, regression could be used for a task like this; however, since there is a fair amount of natural variance in job salaries, I approached this as a classification problem and used a random forest classifier. 

The first part of the project was focused on scraping Indeed.com.au. The latter part of the project was focused on using natural language processing and building models using job postings with salary information to predict salaries.
