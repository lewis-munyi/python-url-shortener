from random import randint
from app.shorten import Shortener

if __name__ == "__main__":
    print("Hi There! Ready to shorten your link?")

    while(True):
        inputUrl = input("Just type it and I'll take it up from there\n\t")
        print("")
        if(inputUrl == ""):
            print("I can't shorten an empty URL :/\n")
            break

        shortener = Shortener()

        # If URL is valid
        if(not shortener.checkIfURLIsValid(inputUrl)):
            print("Enter a valid URL\n")
            continue

        exists = shortener.checkIfExists(inputUrl)
        if(exists):
            # Todo: Pass it to display URL
            print(f"The short URL for {inputUrl} is \n\n\t {exists[1]}")
            continue


        # code = shortener.generateShortCode()

        short_url = shortener.shorten(inputUrl)



        # print("Hello")
