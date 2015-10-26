"""Utility file to seed law school database from ABA data in seed_data/"""


"""
From aba-2013-1l-entering-class-data.txt:

[0] SCHOOL
[1] Total Unduplicated Applications
[2] Total Unduplicated Offers
[3] Admit Rate
[4] 1L Matriculants Yield
[5] 75th Percentile UGPA
[6] 50th Percentile UGPA
[7] 25th Percentile UGPA
[8] 75th Percentile LSAT
[9] 50th Percentile LSAT
[10] 25th Percentile LSAT

Items separated by spaces

We want to use:
[0] SCHOOL
[1] Total Unduplicated Applications
[3] Admit Rate
[5] 75th Percentile UGPA
[6] 50th Percentile  UGPA
[7] 25th Percentile UGPA
[8] 75th Percentile LSAT
[9] 50th Percentile LSAT
[10] 25th Percentile LSAT


From aba-2013-tuition-expenses-data.txt:

[0] SchoolName
[1] Full-Time Resident Student Tuition
[2] Full-Time Non-Resident Student Tuition
[3] Single student living off-campus Living Expenses

Items separated by spaces
Using all info


Additional desired info, no current source:
- school addresses
- school websites


"""
