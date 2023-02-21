import pyperclip
import openai
import sys
import os

key = ""
try :
    key = os.environ["openai_key"]
except KeyError:
    key = input("Please enter your OpenAI key: ")

openai.api_key = key

def main():
    items = []
    try:
        iter_count = 1 if len(sys.argv) == 1 else int(sys.argv[1])
    except ValueError:
        print("Please enter a valid integer (default is 1 if no argument is passed)")
        return

    for i in range(iter_count):
        try:
            completions = openai.Completion.create(
                engine="davinci",
                prompt="Please generate a meaningful question for testing a chat model."
            )
        except openai.error.RateLimitError:
            print("Rate limit exceeded. Tough luck. 😔")
            break
        items.append(completions)

    if len(items) == 0:
        print("No items to copy to clipboard.")
        return
    str_items = '\n'.join(items)
    print(str_items)

    # copy to clipboard
    pyperclip.copy(str_items)

if __name__ == "__main__":
    main()
