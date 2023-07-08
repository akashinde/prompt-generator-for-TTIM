from revChatGPT.V1 import Chatbot
from revChatGPT.V1 import *

chatbot = Chatbot(
    config={"email": "akash.shinde@allianzgi.com", "password": "Happygamer@2001"}
)

image_generation_prompt = """# URL syntax

![Image](https://image.pollinations.ai/prompt/{description}?{params})

## Prompt format

{description} is: {sceneDetailed}%20{adjective}%20{charactersDetailed}%20{visualStyle}%20{genre}%20{artistReference}

Make sure the prompts in the URL are encoded. Don't quote the generated markdown or put any code box around it.

## Params

{params} is: width={width}&height={height}&seed={seed}

Don't ask the user for params if he does not provide them. Instead come up with a reasonable suggestion depending on the content of the image.
The seed is used to create variations of the same image.

# Instructions

You will now act as a prompt generator. 
I will describe an image to you, and you will create a prompt that could be used for image-generation. 

Once I described the image, give a 5-word summary and then include the following markdown without a code box or quotes.

# Example interaction:

Assistant: 
Please describe the image to me, and I'll create a prompt that can be used for image generation.
User: 
A moroccan desert landscape
Assistant: 
high exposure sand dunes at night. 4 k resolution. Highly detailed illustration. By moebius, otomo 
![Image](https://image.pollinations.ai/prompt/high%20exposure%20sand%20dunes%20at%20night.%204%20k%20resolution.%20Highly%20detailed%20illustration.%20By%20moebius%2C%20otomo?width=768&height=384)

Assistant: 
Please describe the image to me, and I'll create a prompt that can be used for image generation.
User: 
Schematic of a skyscraper
Assistant: 
Patent filing schematic of a skyscraper.  Detailed intricate illustration. By thomas edison
![Image](https://image.pollinations.ai/prompt/high%20exposure%20sand%20dunes%20at%20night.%204%20k%20resolution.%20Highly%20detailed%20illustration.%20By%20moebius%2C%20otomo?width=256&height=768)"""


def handle_commands(command: str) -> bool:
    if command == "!help":
        print(
            """
        !help - Show this message
        !reset - Forget the current conversation
        !config - Show the current configuration
        !plugins - Show the current plugins
        !switch x - Switch to plugin x. Need to reset the conversation to ativate the plugin.
        !rollback x - Rollback the conversation (x being the number of messages to rollback)
        !setconversation - Changes the conversation
        !share - Creates a share link to the current conversation
        !exit - Exit this program
        """,
        )
    elif command == "!reset":
        chatbot.reset_chat()
        print("Chat session successfully reset.")
    elif command == "!config":
        print(json.dumps(chatbot.config, indent=4))
    elif command.startswith("!rollback"):
        try:
            rollback = int(command.split(" ")[1])
        except IndexError:
            logging.exception(
                "No number specified, rolling back 1 message",
                stack_info=True,
            )
            rollback = 1
        chatbot.rollback_conversation(rollback)
        print(f"Rolled back {rollback} messages.")
    elif command.startswith("!setconversation"):
        try:
            chatbot.conversation_id = chatbot.config["conversation_id"] = command.split(
                " "
            )[1]
            print("Conversation has been changed")
        except IndexError:
            log.exception(
                "Please include conversation UUID in command",
                stack_info=True,
            )
            print("Please include conversation UUID in command")
    elif command.startswith("!continue"):
        print()
        print(f"{bcolors.OKGREEN + bcolors.BOLD}Chatbot: {bcolors.ENDC}")
        prev_text = ""
        for data in chatbot.continue_write():
            message = data["message"][len(prev_text) :]
            print(message, end="", flush=True)
            prev_text = data["message"]
        print(bcolors.ENDC)
        print()
    elif command.startswith("!share"):
        print(f"Conversation shared at {chatbot.share_conversation()}")
    elif command == "!exit":
        if isinstance(chatbot.session, httpx.AsyncClient):
            chatbot.session.aclose()
        exit()
    else:
        return False
    return True


session = create_session()
completer = create_completer(
    [
        "!help",
        "!reset",
        "!config",
        "!rollback",
        "!exit",
        "!setconversation",
        "!continue",
        "!plugins",
        "!switch",
        "!share",
    ],
)
print()

print("Chatbot: ")
prev_text = ""
for data in chatbot.ask(image_generation_prompt, auto_continue=True):
    message = data["message"][len(prev_text) :]
    print(message, end="", flush=True)
    prev_text = data["message"]
print()

while True:
    print(f"{bcolors.OKBLUE + bcolors.BOLD}You: {bcolors.ENDC}")
    prompt = get_input(session=session, completer=completer)
    if prompt.startswith("!") and handle_commands(prompt):
        continue

    print()
    print(f"{bcolors.OKGREEN + bcolors.BOLD}Chatbot: {bcolors.ENDC}")
    if chatbot.config.get("model") == "gpt-4-browsing":
        print("Browsing takes a while, please wait...")
    with Live(Markdown(""), auto_refresh=False) as live:
        for data in chatbot.ask(prompt=prompt, auto_continue=True):
            if data["recipient"] != "all":
                continue
            result = data
            message = data["message"]
            live.update(Markdown(message), refresh=True)
    print()

    if result.get("citations", False):
        print(
            f"{bcolors.WARNING + bcolors.BOLD}Citations: {bcolors.ENDC}",
        )
        for citation in result["citations"]:
            print(
                f'{citation["metadata"]["title"]}: {citation["metadata"]["url"]}',
            )
        print()
