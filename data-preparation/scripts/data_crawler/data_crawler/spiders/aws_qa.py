import scrapy
import json
import pandas as pd

class AwsQaSpider(scrapy.Spider):
    name = "aws_qa"
    allowed_domains = ["www.amazonaws.cn"]
    start_urls = [
        "https://www.amazonaws.cn/en/ec2/faqs/",
        "https://www.amazonaws.cn/en/rds/faqs/",
        "https://www.amazonaws.cn/en/lambda/faqs/"
    ]

    def parse(self, response):
        question_data = []
        # Extracting the desired element using xpath selector
        for grid in response.xpath('//div[@class="lb-grid"]'):
            for question in grid.xpath('./div[@class="lb-row lb-row-max-large lb-snap"]/div[@class="lb-col lb-tiny-24 lb-mid-24"]/div[@class="lb-txt-16 lb-rtxt"]/p'):
                # Extracting the text from the desired element using xpath selector
                if question.xpath('./b'):
                    current_question = dict(input="",output="")
                    question_text = question.xpath('./b/text()').get()
                    print(f"question->\n{question_text}")
                    current_question["instruction"]=question_text
                else:
                    answer_text = question.xpath('./text()').get()
                    if current_question["output"]!="":
                        current_question["output"]="\n".join([current_question["output"],answer_text])
                    else:
                        current_question["output"]=answer_text
                    print(f"answer->\n{answer_text}")
                if "instruction" in current_question and current_question["output"]!="" :
                    question_data.append(current_question)
        print(len(question_data))
        with open('question_data.json', 'w') as f:
            json.dump(question_data, f)

