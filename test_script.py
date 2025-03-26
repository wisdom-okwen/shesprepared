from gpt import get_gpt_response
from llama import get_llama_response

def run_test():
    """Function to interact with chatbot from the terminal."""

    print("\n----------------------Welcome To Your Friendly HIV Prevention Chatbot----------------------------\n")
    print("I am ShesPrEPared, a friendly assistant focused on HIV prevention and PrEP counseling for women.")
    print("How can I assist you today?\n")

    user_input = input("Enter your query here:  ")
    print()
    while user_input:
        try:
            response = get_gpt_response(user_input)
            print("RESPONSE:")
            print("---------")
            print(f"{response}")
            print()
            print("Hit the 'Enter' key to end this session.\n")
            print("-----------------------------------------------------------------------------------------------\n")
            user_input = input("YOUR INPUT:  ")
            print()
        except Exception as e:
            print("An error occured:  ", e)
            exit()


if __name__ == "__main__":
    run_test()