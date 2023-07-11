from promptModel import runModel
from dotenv import load_dotenv
import replicate

def print_array(arr):
    for item in arr:
        print(item)
        print()

def generatePrompts(prompt):
    response = runModel(prompt)
    print("\n\nOriginal PROMPT: \n" + prompt + "\n")
    print("New PROMPTS: ")
    print(response)
    print()

load_dotenv()
prompt = "Imagine a bustling city street during a rainy evening."
generatePrompts(prompt)

# output = replicate.run(
#     "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
#     input={"prompt": prompt}
# )
# print(output)


# Examples
# "Describe a peaceful beach scene at sunset."
# "Provide a detailed description of a cozy cabin in the snowy mountains."
# "Imagine a bustling city street during a rainy evening."
# "Describe a picturesque waterfall surrounded by lush greenery."
# "Paint a vivid picture of a serene countryside meadow in springtime."
# "Envision a vibrant market filled with colorful fruits, vegetables, and flowers."
# "Describe a majestic castle nestled on top of a hill, overlooking a tranquil lake."
# "Imagine a charming café with cozy seating, soft lighting, and delicious pastries."
# "Provide a detailed description of a futuristic cityscape with towering skyscrapers and flying vehicles."
# "Describe a magical forest illuminated by the soft glow of fireflies."