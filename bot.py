import random
import twitter
import logging
import os
from datetime import date

from secrets import *

# https://www.vegsoc.org/sslpage.aspx?pid=525
foods = {
    1: ["Apples", "Beetroot", "Brussels Sprouts", "Cabbage", "Carrots", "Celeriac", "Celery", "Chicory", "Jerusalem Artichokes", "Kale", "Leeks", "Mushrooms", "Onions", "Parsnips", "Pears", "Spring Greens", "Spring Onions", "Squash", "Swedes", "Turnips"],
    2: ["Apples", "Beetroot", "Brussels Sprouts", "Cabbage", "Carrots", "Celeriac", "Chicory", "Jerusalem Artichokes", "Kale", "Leeks", "Mushrooms", "Onions", "Parsnips", "Pears", "Purple Sprouting Broccoli", "Spring greens", "Spring Onions", "Squash", "Swedes"],
    3: ["Artichoke", "Beetroot", "Cabbage", "Carrots", "Chicory", "Cucumber", "Leeks", "Parsnip", "Purple Sprouting Broccoli", "Radishes", "Rhubarb", "Sorrel", "Spring Greens", "Spring Onions", "Watercress"],
    4: ["Artichoke", "Beetroot", "Cabbage", "Carrots", "Chicory", "New Potatoes", "Kale", "Morel Mushrooms", "Parsnips", "Radishes", "Rhubarb", "Rocket", "Sorrel", "Spinach", "Spring Greens", "Spring Onions", "Watercress"],
    5: ["Artichoke", "Asparagus", "Aubergine", "Beetroot", "Chicory", "Chillies", "Elderflowers", "Lettuce", "Marrow", "New Potatoes", "Peas", "Peppers", "Radishes", "Rhubarb", "Rocket", "Samphire", "Sorrel", "Spinach", "Spring Greens", "Spring Onions", "Strawberries", "Watercress"],
    6: ["Asparagus", "Aubergine", "Beetroot", "Blackcurrants", "Broad Beans", "Broccoli", "Cauliflower", "Cherries", "Chicory", "Chillies", "Courgettes", "Cucumber", "Elderflowers", "Gooseberries", "Lettuce", "Marrow", "New Potatoes", "Peas", "Peppers", "Radishes", "Raspberries", "Redcurrants", "Rhubarb", "Rocket", "Runner Beans", "Samphire", "Sorrel", "Spring Greens", "Spring Onions", "Strawberries", "Summer Squash", "Swiss Chard", "Tayberries", "Turnips", "Watercress"],
    7:["Aubergine", "Beetroot", "Blackberries", "Blackcurrants", "Blueberries", "Broad Beans", "Broccoli", "Carrots", "Cauliflower", "Cherries", "Chicory", "Chillies", "Courgettes", "Cucumber", "Gooseberries", "Greengages", "Fennel", "French Beans", "Garlic", "Kohlrabi", "Loganberries", "New Potatoes", "Onions", "Peas", "Potatoes", "Radishes", "Raspberries", "Redcurrants", "Rhubarb", "Rocket", "Runner Beans", "Samphire", "Sorrel", "Spring Greens", "Spring Onions", "Strawberries", "Summer Squash", "Swish Chard", "Tomatoes", "Turnips", "Watercress"],
    8:["Aubergine", "Beetroot", "Blackberries", "Blackcurrants", "Broad Beans", "Broccoli", "Carrots", "Cauliflower", "Cherries", "Chicory", "Chillies", "Courgettes", "Cucumber", "Damsons", "Fennel", "French Beans", "Garlic", "Greengages", "Kohlrabi", "Leeks", "Lettuce", "Loganberries", "Mangetout", "Marrow", "Mushrooms", "Parsnips", "Peas", "Peppers", "Potatoes", "Plums", "Pumpkin", "Radishes", "Raspberries", "Redcurrants", "Rhubarb", "Rocket", "Runner Beans", "Samphire", "Sorrel", "Spring Greens", "Spring Onions", "Strawberries", "Summer Squash", "Sweetcorn", "Swiss Chard", "Tomatoes", "Watercress"],
    9: ["Aubergine", "Beetroot", "Blackberries", "Broccoli", "Brussels Sprouts", "Butternut Squash", "Carrots", "Cauliflower", "Celery", "Courgettes", "Chicory", "Chillies", "Cucumber", "Damsons", "Garlic", "Kale", "Kohlrabi", "Leeks", "Lettuce", "Mangetout", "Marrow", "Onions", "Parsnips", "Pears", "Peas", "Peppers", "Plums", "Potatoes", "Pumpkin", "Radishes", "Raspberries", "Rhubarb", "Rocket", "Runner Beans", "Samphire", "Sorrel", "Spinach", "Spring Greens", "Spring Onions", "Strawberries", "Summer Squash", "Sweetcorn", "Swiss Chard", "Tomatoes", "Turnips", "Watercress", "Wild Mushrooms"],
    10:["Aubergine", "Apples", "Beetroot", "Blackberries", "Broccoli", "Brussels Sprouts", "Butternut Squash", "Carrots", "Cauliflower", "Celeriac", "Celery", "Chestnuts", "Chicory", "Chillies", "Courgette", "Cucumber", "Elderberries", "Kale", "Leeks", "Lettuce", "Marrow", "Onions", "Parsnips", "Pears", "Peas", "Potatoes", "Pumpkin", "Radishes", "Rocket", "Runner Beans", "Spinach", "Spring Greens", "Spring Onions", "Summer Squash", "Swede", "Sweetcorn", "Swiss Chard", "Tomatoes", "Turnips", "Watercress", "Wild Mushrooms", "Winter Squash"],
    11:["Apples", "Beetroot", "Brussels Sprouts", "Butternut Squash", "Cabbage", "Carrots", "Cauliflower", "Celeriac", "Celery", "Chestnuts", "Chicory", "Cranberries", "Elderberries", "Jerusalem Artichokes", "Kale", "Leeks", "Onions", "Parsnips", "Pears", "Potatoes", "Pumpkin", "Swede", "Swiss Chard", "Turnips", "Watercress", "Wild Mushrooms", "Winter Squash"],
    12:["Apples", "Beetroot", "Brussels Sprouts", "Carrots", "Celeriac", "Celery", "Chestnuts", "Chicory", "Cranberries", "Jerusalem Artichokes", "Kale", "Leeks", "Mushrooms", "Onions", "Parsnips", "Pears", "Potatoes", "Pumpkin", "Red Cabbage", "Swede", "Swiss Chard", "Turnips", "Watercress", "Winter Squash"],
}

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('got event{}'.format(event))

    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token_secret = os.environ['access_token_secret']
    access_token_key = os.environ['access_token_key']

    api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

    month = date.today().month
    seasonalVeg = ", ".join(random.sample(foods[month],3))
    status = api.PostUpdate("the following veg is in season this month: "+ seasonalVeg)
    
    logger.info('got status{}'.format(status))
    
    return "finshed"

def destroyStatuses(api: twitter.api):
    timeline = api.GetUserTimeline(count=200)
    for status in timeline:
        api.DestroyStatus(status.id)

if __name__=="__main__":
    lambda_handler(None,None)
