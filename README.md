# Quora NL Scraper
Scrape questions and answers from Quora NL, which is formatted differently than regular Quora. Code adaptation from https://github.com/sdhanendra/quora-scraper.


`topic_list.txt`: text file with topics on each newline, of which each word of the topic needs to be lowercased and joined by '%20' as substitute for space. For example: 'corona%20vaccinatie'<br />
`quora-question-scraper.py`: scrapes questions of which the topic is mentioned in the question URL and puts them in topic_questions_urls.txt. <br />
`quora-answer-scraper.py`: scrapes answers from topic_questions_urls.txt obtained by question scraper. [work in progress]. <br />
