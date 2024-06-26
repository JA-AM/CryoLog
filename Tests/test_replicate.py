from dotenv import load_dotenv
import replicate

load_dotenv()

input = {
    "prompt": "Write fizz buzz in SQL",
    "temperature": 0.2
}

for event in replicate.stream(
    "snowflake/snowflake-arctic-instruct",
    input=input
):
    print(event, end="")
#=> "Fizz Buzz is a common programming problem that involves ...