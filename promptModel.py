from revChatGPT.V1 import Chatbot
import re

chatbot = Chatbot(
    config={"email": "akash.shinde@allianzgi.com", "password": "Happygamer@2001"}
)


def askGPT(prompt):
    for data in chatbot.ask(prompt):
        res = data["message"]
    return res


def generateExamples(prompt):
    extract_key_prompt = (
        "consider following prompt ("
        + prompt
        + "). Research and tell me which photography category is best for this?"
    )
    key_elements = askGPT(extract_key_prompt)

    example_prompt = (
        "You will now act as a prompt generator. Generate generative prompts related to these key elements. Also, Using following key elements make a table with 5 rows of example data where the first column start with prompt's main element then Lighting, Composition, Reflections, Colors, Silhouettes. ("
        + key_elements
        + ")"
    )
    example_tables = askGPT(example_prompt)
    convert_to_array_prompt = (
        "Convert following table rows to comma seperated and insert them into python list with variable name data. ("
        + example_tables
        + ")"
    )
    final_examples = askGPT(convert_to_array_prompt)
    return final_examples


def generateExamples2(prompt):
    algorithm = '''
    You will now act as a prompt generator which could be use to generate ai images. 
    Consider following structure of the prompt used in AI image generator to generate excellent prompts ([image content/subject, description of action, state, and mood], [art form, style, and artist references], [additional settings, such as lighting, colors, and framing])
    Consider following parameters in above structure to create perfect prompt:
    1. Include the art form, style, and artist references like Photography, painting, illustration, digital arts, film stills
    2. Add more details to your prompt like Framing, Lighting, Color scheme, Level of detail and realism
    Considering all above points and generate lists of prompts for the following image description.
    Generate prompts for following image description ('''+prompt+''') in a detailed storytelling format.
    '''
    examples = askGPT(algorithm)
    print(examples)
    return examples

def generateExamples3(prompt):
    algorithm = '''
    You will now act as a prompt enhancer which will be used in AI image generation. 
    The prompt is: ('''+prompt+''').
    Following is prompt structure which generates the images in AI image generation. 
    The structure is: (medium, subject, noun, details, background (use the word "in"), specify details about background, stylizers, artist names). 
    First create 10 different possible values for each of the objects from above structure (POSSIBILITIES SHOULD BE IN THE CONTEXT OF ORIGINAL PROMPT ONLY. DO NOT CHANGE THE CONTEXT OF ORIGINAL PROMPT)
    Next, generate 10 different prompts with more meaning than the original prompt. (DO NOT CHANGE THE CONTEXT OF ORIGINAL PROMPT.)

    OUTPUT OF ABOVE RESULT SHOULD BE IN THE FORM OF JSON RESPONSE. For first result use "data" as the variable name and for the second result use "prompts" as the variable name.
    '''
    response = askGPT(algorithm)
    data = eval(response)
    return data

def extractArray(example_list):
    data = []
    pattern = r"```python\n([\s\S]*?)```"
    match = re.search(pattern, example_list)
    if match:
        extracted_string = match.group(1)
        print(extracted_string)
        data_pattern = r"data = ([\s\S]*?\n\])"
        data_match = re.search(data_pattern, extracted_string)
        if data_match:
            data_array_string = data_match.group(1)
            data = eval(data_array_string)
    return data


def runModel(prompt):
    # example_list = generateExamples(prompt)
    # examples = extractArray(example_list)
    # examples = generateExamples2(prompt)
    examples = generateExamples3(prompt)
    return examples


# Prompt format
# [medium], [subject], [noun], [details], [background (use the word "in")], [specify details about background], [stylizers], [artist names]