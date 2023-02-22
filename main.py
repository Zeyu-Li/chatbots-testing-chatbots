from simple_term_menu import TerminalMenu
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
    engine_list = ["davinci", "curie", "babbage", "ada"]
    engine = "davinci"
    prompt = "Please generate a meaningful question for testing a chat model."
    OVERRIDE_PROMPT = False

    try:
        iter_count = 1 if len(sys.argv) == 1 else int(sys.argv[1])
    except ValueError:
        print("Please enter a valid integer (default is 1 if no argument is passed)")
        return

    # override prompt if we find the selection process annoying
    if OVERRIDE_PROMPT:
        print("Using engine: davinci (default) \nUsing prompt: Please generate a meaningful question for testing a chat model. (default)\n")

        terminal_menu = TerminalMenu(["Accept default for all", "davinci (default)",  "curie", "babbage", "ada"])
        choice_index = terminal_menu.show()

        if choice_index != 0:
            engine = engine_list[choice_index - 1]

            # get prompt
            terminal_menu = TerminalMenu(["Please generate a meaningful question for testing a chat model. (default)", "Write your own"])
            choice_index = terminal_menu.show()

            if choice_index != 0:
                prompt = input("Please enter your prompt: ")

    # for all instance if return with rate limit error then break and keep the items we have
    for i in range(iter_count):
        try:
            completions = openai.Completion.create(
                engine=engine,
                prompt=prompt
            )
        except openai.error.RateLimitError:
            print("Rate limit exceeded. Tough luck. 😔")
            break
        items.append(completions)

    if len(items) == 0:
        print("No items to copy to clipboard. 📋")
        return
    str_items = '\n'.join(items)
    print(str_items)

    # copy to clipboard
    pyperclip.copy(str_items)

if __name__ == "__main__":
    main()
