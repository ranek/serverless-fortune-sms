import boto3
import os
import random
import re

SNS_TOPIC = os.environ['SNS_TOPIC']
PERMITTED_CHARACTERS = re.compile(
    r'^[a-zA-Z0-9 _@?!1$"%&\\()*:+;,<\-=.>/\']+$')
FORTUNE_PREFIX = ""

sns_topic = boto3.resource('sns').Topic(SNS_TOPIC)


def permitted_fortune(fortune):
    """Throw away a couple hundred fortunes that are contain unusual
    characters or would be uncomfortanbly long for the SMS medium.
    While SNS does support sending SMS with GSM, ASCII, and UCS-2 character
    sets, and will automatically break up long messages, this subset of
    fortunes all fit comfortably in one SMS, avoiding unexpected bills
    and display weirness on older phones. """
    return PERMITTED_CHARACTERS.match(
        fortune) and len(fortune) + len(FORTUNE_PREFIX) < 140


fortunes = [":( Error loading fortune file."]
with open('vendor/fortunes.txt', 'r') as fortune_file:
    fortunes = fortune_file.readlines()

fortunes = list(filter(permitted_fortune, fortunes))

# Force connection to us-west-2, since not all regions support SMS
sns_client = boto3.client('sns', region_name='us-west-2')


def lambda_handler(event, context):
    fortune = FORTUNE_PREFIX + random.choice(fortunes)
    sns_topic.publish(Message=fortune)
