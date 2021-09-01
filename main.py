
# All the imports
import os
import json
import requests
import discord

# Huggingface URL
API_URL = 'https://api-inference.huggingface.co/models/microsoft/'

#Main Class Creates Client for discord
class MyClient(discord.Client):
    def __init__(self, model_name):
        super().__init__()
        self.api_endpoint = API_URL + model_name
        # retrieve the secret API token from the system environment
        huggingface_token = "YOUR_HUGGING_FACE_API_TOKEN"
        # format the header in our request to Hugging Face
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }
        
        # Queries the huggingface api and stores the result in json format

    def query(self, payload):
        """
        make request to the Hugging Face model API
        """
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret

    async def on_ready(self):
        # print out information when the bot is online
        print('Logged in!')
        print('Yayyy! Axobot is on!')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # send a request to the model without caring about the response
        # just so that the model wakes up and starts loading
        self.query({'inputs': {'text': 'Hello!'}})

    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return

        # form query payload with the content of the message
        payload = {'inputs': {'text': message.content}}

        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        async with message.channel.typing():
            response = self.query(payload)
        bot_response = response.get('generated_text', None)

        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'Oopsie! Something is not right!'

        # send the model's response to the Discord channel
        await message.channel.send(bot_response)


def main():
    # DialoGPT-medium-joshua is my model name
    client = MyClient('DialoGPT-large')
    discord_token = "YOUR_DISCORD_TOKEN"
    client.run(discord_token)



if __name__ == '__main__':
    main()

