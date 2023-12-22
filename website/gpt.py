import openai


openai.api_key = "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" #API


def generate_response(question):

    prompt = """ You are a helpful assistant AI with knowledge across various domains. You are going to assist the user. """.format(question)
    model = "text-davinci-003"
    tokens = 250
    temp = 1

    generate_response = openai.Completion.create(
        
        engine = model,
        prompt = prompt,
        max_tokens = tokens, #tokens limit
        temperature = temp #no of characters 
    )
    return generate_response.choices[0].text.strip()
