__doc__ = """
Make script to print out n questions which has been voted the most by **LABEL** on stackoverflow.com.
the result after run the script is: Question's Title, the most voted answer link.

Link API: https://api.stackexchange.com/docs

Command prompt:

  python3 so.py n LABEL
"""

import requests
import sys
import json
import html


def top_n_questions_by_label(n, label):
    titles = []
    answer_urls = []
    get_questions_url = "https://api.stackexchange.com/2.2/questions?pagesize={}&order=desc&sort=votes&tagged={}&site=stackoverflow".format(
        n, label
    )
    session_1 = requests.Session()
    session_2 = requests.Session()
    request_1 = session_1.get(get_questions_url).text
    json_response = json.loads(request_1)
    for item in json_response["items"]:
        # get all the question titles and convert them to Unicode characters
        titles.append(html.unescape(item["title"]))
        question_ids = item["question_id"]
        get_answer_url = "https://api.stackexchange.com/2.2/questions/{}/answers?pagesize=1&order=desc&sort=votes&site=stackoverflow".format(
            question_ids
        )
        request_2 = session_2.get(get_answer_url).text
        answer_ids = json.loads(request_2)["items"][0]["answer_id"]
        # get all the answer links
        answer_urls.append("https://stackoverflow.com/a/" + str(answer_ids))

    # mix these two lists altogether as a list of tuples
    result = list(zip(titles, answer_urls))
    return result


def main():
    try:
        if len(sys.argv) != 3:
            print(
                "Please input as following instruction: number of questions and question label"
            )
            sys.exit()
        n, label = int(sys.argv[1]), sys.argv[2]
        if n <= 0:
            print("Please input number > 0")
        for (idx, (title, answer_url)) in enumerate(top_n_questions_by_label(n, label), start=1):
            print("{}. {} - Answer link: {}".format(idx, title, answer_url))
    except ValueError:
        print(
            "Please input as following instruction: number of questions and question label")


if __name__ == "__main__":
    main()
