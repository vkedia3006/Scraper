import requests
from bs4 import BeautifulSoup
import json
from io import StringIO
import csv

module_urls = ["https://www.apnatoronto.com/rights-and-responsibilities-of-citizenship/", "https://www.apnatoronto.com/chapter-who-we-are/", "https://www.apnatoronto.com/canadas-history/", "https://www.apnatoronto.com/canadas-history-02/", "https://www.apnatoronto.com/modern-canada/", "https://www.apnatoronto.com/how-canadians-govern-themselves/", "https://www.apnatoronto.com/federal-elections/", "https://www.apnatoronto.com/the-justice-system/", "https://www.apnatoronto.com/canadian-symbols/", "https://www.apnatoronto.com/canadas-economy/", "https://www.apnatoronto.com/canadas-regions/"]
practice_test = "https://www.apnatoronto.com/canadian-citizenship-test"
test_urls = [f"{practice_test}{i}/" for i in range(1, 11)]

for url in test_urls:
    name = url.split("/")[-2]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find(id="wpvqgr_quiz_trivia-script-global-js-extra").text
    jsonFile = StringIO(script.split("var wpvqgr = ")[1].strip().rstrip(";"))
    data = json.load(jsonFile)
    qs = data["vars"]["quiz"]["questions"]
    questions = []
    answers = []

    for q in qs:
        questions.append(q["wpvqgr_quiz_questions_content"])
        answers.append([(op["wpvqgr_quiz_questions_answers_answer"], op["wpvqgr_quiz_questions_answers_right"]) for op in q["wpvqgr_quiz_questions_answers"]])

    data = []
    index = ["a", "b", "c", "d"]

    for question, options in zip(questions, answers):
        d = [f"{question}\n"]
        correct = ""
        for (op, isCorrect), i in zip(options, index):
            if isCorrect:
                correct = op
            d[0] = d[0] + f"{i}. {op.strip()}\n"
        d.append(correct.strip())
        data.append(d)

    with open(f"{name}.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
