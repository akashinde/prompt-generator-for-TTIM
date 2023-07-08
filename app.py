from promptModel import runModel

def print_array(arr):
    for item in arr:
        print(item)
        print()

def generatePrompts():
    prompt = "A cat on the sofa"
    new_prompts = runModel(prompt)
    print("\n\nOriginal PROMPT: \n" + prompt + "\n")
    print("New PROMPTS: ")
    print(new_prompts)
    print()


generatePrompts()



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