from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from autogen import UserProxyAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent, AssistantAgent
from autogen import config_list_from_json
import json
import autogen
from django.conf import settings
from bs4 import BeautifulSoup
import requests
import re

config_list = [
    {
        'model': 'gpt-3.5-turbo-0125',
        'api_key': settings.OPENAI_API_KEY,
    },
]
config_list_gemini_pro = [
    {
        'model': 'gemini-pro',
        'api_key': settings.GOOGLE_AI_API_KEY,
        'api_type': 'google'
    },
]

scraper_instruction ="""

You always run first. When the Researcher tell you "SCRAPER, REPEAT", you will repeat by scrape another url that you found

You are a Website Content Crawler. You obtained an input with raw content. The data is about an algorithm problem.

Your duty is clean it  and return it with JSON format. Just return the cleaned data WITHOUT ANY TEXT.

-First, you will search google. And then, you choose the two most relevant url. And scrape it AS MUCH AS DATA POSSIBLE IN THIS URL.
 Note that you DON'T scrape https://leetcode.com url directly because this website can't scrape.
 DON'T REPEAT THIS ACTION UNLESS Researcher tell you do. I said one more time, DON'T REPEAT.

-After that, you will clean the raw data returned. Return the REALLY cleaned data with JSON Format WITHOUT ANY TEXT
"""

researcher_instruction = """
- You run after received the data of Scraper. If the data from Scraper didn't detail enough. Include:
	 +overview: Explain the problem
	 +input: The example input WITHOUT ANY TEXT
	 +output: Output due to the input fields. 
	 +explain_output: tell why we have the output after the input. If the output is very easy to understand, return ""
	 +approachs: The list of approachs of this problem
	 +title: The name of solution
	 +step: The step of this approachs
	 +complexity: Return the complexity of this approachs WITHOUT ANY TEXT
	 +code: code using C++ 
You will say "SCRAPER, REPEAT" WITHOUT ANY TEXT. BUT YOU JUST CAN REPEAT LESS THAN 3 TIMES
If you satisfied, you will do these instruction: 

- Problem Understanding: You should be able to understand the problem statement.
 This could be achieved by using natural language processing techniques to extract key information from the problem statement.

- Search and Scrape: You should get the data returned by Scraper and read it carefully before continue your tasks.
If scraping didn't work, just use your own data. You JUST REFER the data and generate by yourself.-When you scraped,
you should think "Can i research deeper" and continue call Scraperone more time. But DON'T do it more than 3 times

- Analyze and Summarize: You should be able to analyze the scraped data returned by Scraper. This could involve identifying the key steps in the solution,
understanding the logic behind the solution, and presenting it in a clear and concise manner.

- Performance and Accuracy: To improve performance and accuracy, you could limit the number of search and scrape operations.
Also, you could use machine learning techniques to learn from past interactions and improve your ability to solve algorithm problems over time.
You should run the code and fix it for increase performance

Generate JSON: You MUST generate a JSON object with fields like
 {“overview”:data,
  “input”:data,
  “output”:data,
  "explain_output"=data,
  "approachs":[
	{
		"title":data,
		"step":[data]
		"complexity":data
		"code": data
	}

],"code":[]} .
 Note that:
	 +overview: Explain the problem
	 +input: The example input WITHOUT ANY TEXT
	 +output: Output due to the input fields. 
	 +explain_output: tell why we have the output after the input. If the output is very easy to understand, return ""
	 +approachs: The list of approachs of this problem
	 +title: The name of solution
	 +step: The step of this approachs
	 +complexity: Return the complexity of this approachs WITHOUT ANY TEXT
	 +code: code using C++

When you done, You MUST return the JSON. After generate JSON, tell "TERMINATE" outside JSON format in the end WITHOUT ANY TEXT 
"""
def web_scraping(url):
    with requests.Session() as session:
        try:
            response = session.get(url)
            response.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError) as e:
            print(f"Failed to get content from {url}, error: {e}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in re.split(r"\s{2,}", line))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    


def google_search(search_keyword):    
    print(search_keyword)
    url = "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": search_keyword
    })

    headers = {
        'X-API-KEY': settings.SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
# Agents
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "use_docker": False,
    }
)

difficulty = GPTAssistantAgent(
    name="difficulty reviewer",
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_a1UfEsDoYNTRz19DPTibUtVI"
    },
    code_execution_config={
        "use_docker": False,
    }
)
scraper = GPTAssistantAgent(
    name="scraper",
    overwrite_instructions=True,
    instructions= scraper_instruction,
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_PbdYfnKYdjkTpEoNJRPSDg4u"
    },
    code_execution_config={
        "use_docker": False,
    }
)
scraper.register_function(
    function_map={
        "web_scraping": web_scraping,
        "google_search": google_search
    }
)

researcher = AssistantAgent(
    name="researcher",
    overwrite_instructions=True,
    instructions= researcher_instruction,
    llm_config={
        "config_list": config_list,
        "assistant_id": "asst_o6f79wNVkXoPE1QWfOzBS9bj"
    },
    code_execution_config={
        "use_docker": False,
    }
)
groupchat = autogen.GroupChat(agents=[user_proxy,scraper,researcher], messages=[], max_round=12)
manager = autogen.GroupChatManager(
                groupchat=groupchat,
                llm_config={
                    "config_list": config_list
                    },
                code_execution_config={
                    "use_docker": False,
                    }
            )
# Views part
class GPT40DifficultyView(APIView):
    """
    GPT-4 Algorithm Difficulty Reviewer API
    [POST]/api/v1/difficulty
    """
    def post(self, request, format=None):
        try:
            print("Hi")
            raw_data = request.body.decode('utf-8')
            print('DATA: ',raw_data)
            data = json.loads(raw_data)
            message = data['data']
            user_proxy.initiate_chat(manager, message=message)
            result = user_proxy.last_message()
            print(result)
            res = result['content'].replace("TERMINATE", "").strip()
            res_final =json.dumps(
                {
                    "data": res
                }
            )
            print("hi", res)
            return Response(res_final)
        except Exception as e:
            errors = "There are errors: {}".format(str(e))
            return Response({"error": errors}).status_code(500)