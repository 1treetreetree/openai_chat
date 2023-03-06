import openai
import datetime

openai.api_key_path = "openai_api_key.txt"

# params
model = "gpt-3.5-turbo"
echo = False
role_of_assistant = "You are a helpful assistant."
max_tokens=3000
temperature=0.7
# -----

try:
    with open("history.txt", "r") as history:
        pass
except:
    with open("history.txt", "a") as history:
        history.write("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nThis text file shows the full history of all conversations had with the model.\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

running = True
while running:
    ongoing_convo = True
    context = [{"role": "system", "content": role_of_assistant}]
    print("\n{horizontal_line}\n\nWelcome to {model} | At any time, instead of a prompt you can type \"restart\" to reset the program, or \"stop\" to stop it.\n\n{horizontal_line}\n\n".format(horizontal_line=("-=" * 80),model=model))

    while ongoing_convo == True:
        prompt = input("Your prompt:\n>>>")
        if prompt == "stop" or prompt == "end" or prompt == "quit" or prompt == "exit":
            running = False
            break
        elif prompt == "restart" or prompt == "reset":
            ongoing_convo = False
            with open("history.txt", "a") as history:
                history.write("\n\n({datetime})\nrestarted convo".format(datetime=str(datetime.datetime.now())[:-7]))

        elif prompt == "rr":
            role_of_assistant = input("role_of_assistant (default: \"You are a helpful assistant.\"):\n>>>")
            ongoing_convo = False
            with open("history.txt", "a") as history:
                history.write("\n\n({datetime})\nrestarted convo, changed role of assistant".format(datetime=str(datetime.datetime.now())[:-7]))

        else:
            context.append({"role": "user", "content": prompt})
            output = openai.ChatCompletion.create(model=model, messages=context, temperature=temperature, max_tokens=max_tokens)
            response = output["choices"][0]["message"]["content"]
            if echo:
                print("\nPrompt: " + prompt)
                print(model + " response: " + response)
                print("\n\n", output, "\n\n")
            else:
                print(response)
            context.append({"role": "assistant", "content": response})

            with open("history.txt", "a") as history:
                history.write("\n\n({datetime})\nrole of assistant: \"{role_of_assistant}\"\nprompt: {prompt}\n{model} response: {response}".format(datetime=str(datetime.datetime.now())[:-7],prompt=prompt,role_of_assistant=role_of_assistant,model=model,response=response))
