import sys
from random import choice 
import os
import discord

"""Generate Markov text from text files."""



def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    text_in_file = open(file_path).read()

    return text_in_file


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """
    words = text_string.split()
    chains = {}
    for i in range(len(words)-2):
        bigram = (words[i], words[i+1])
        word_following_bigram = words[i+2]
        existing_words = chains.get(bigram, []) #creates key with blank list; existing_words is the value
        existing_words.append(word_following_bigram) #appends following word to the empty list
        chains[bigram] = existing_words    #stores new appended list back into the dictionary
       
    return chains


def make_text(chains):
    """Return text from chains."""
    
    words = []
    #random_value = choice(chains) #randomly chooses valu from the dictionary
    # random_key = random_value.values() 
    random_key = choice(list(chains))
    words.extend(random_key)
    while True:
        random_value = choice(chains[random_key])
        words.append(random_value)
        random_key = (random_key[1], random_value)
        if random_key not in chains:
            break
    
    #print(random_value)
    #loops
    # while True:
    #     if link not in chains:
    #         break
    #     else:
    #         random_val = random.choice(chains[chains[key]])
        #start with link = random key and then randomly select value from that key
        #put link into list
        #second link = second key value from the previous and the random value, and the value for that one is selected randomly
        #when key is not in dictionary break 
    #Get link out of list form and convert to a string


    return ' '.join(words)


filenames = sys.argv[1]

# Open the file and turn it into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# Produce random text
random_text = make_text(chains)

#print(random_text)



client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    
    if message.content.startswith('hello'):
        await message.channel.send(random_text)

client.run(os.environ['DISCORD_TOKEN'])
