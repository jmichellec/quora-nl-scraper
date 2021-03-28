# Quora NL Scraper
Scrape questions and answers from Quora NL, which is formatted differently than English Quora. This code is an adaptation of the English version from: https://github.com/sdhanendra/quora-scraper.


`topic_list.txt`: text file with topics on each newline, of which each word of the topic needs to be lowercased and joined by '%20' as substitute for space. For example: 'mark%20rutte'<br />
`quora-question-scraper.py`: scrapes questions of which the topic is mentioned in the question URL and puts them in topic_questions_urls_date.csv. <br />
`quora-answer-scraper.py`: scrapes answers from topic_questions_urls_date.csv obtained by question scraper. <br />
NOTE: it scrapes all answers to the question seen when not signed in, which means 'gerelateerde antwoorden'/related answers too. Can't distinguish it from the main answers unless signed in, which does not show 'gerelateerde antwoorden'. <br />

