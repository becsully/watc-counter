from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re


#given the URL of a show rundown, this will return a dictionary of each story in the rundown with links
def get_links(rundown):
    r = requests.get(rundown)
    soup = BeautifulSoup(r.text)
    articles = soup.findAll("article", {"class": "story clearfix"})
    story_dict = {}
    count = 0
    for article in articles:
        if article.h1:
            count += 1
            head = article.h1
            ref = head.a
            slug = head.get_text()
            link = ref.get('href')
            story_dict[count] = {'Slug': slug, 'URL': link}
        else: pass
    return story_dict


#this function checks to see if there is a transcript linked on the story page. if so, it will return True and the link.
def is_transcript(URL):
    baseurl = 'http://www.npr.org'
    r = requests.get(URL)
    soup = BeautifulSoup(r.text)
    transcript_link = soup.findAll("a", {"class": "trans"})
    if transcript_link:
        link = baseurl + transcript_link[0].get('href')
        return True, link
    else:
        return False, None


#this function runs each of the links from get_links() story_dict through the is_transcript() checker, and returns story_dict with finalized links - each page should have a transcript.
def transcript_links(story_dict):
    for story in story_dict:
        transcript_bool, transcript_link = is_transcript(story_dict[story]["URL"])
        if transcript_bool:
            story_dict[story]["URL"] = transcript_link
        else: pass
    return story_dict


#this runs through the transcript and returns the names of people quoted. this might not work for people with same last names.
def name_getter(STORY_URL):
    r = requests.get(STORY_URL)
    soup = BeautifulSoup(r.text)
    raw_trans = soup.find("div", {"class": re.compile("^transcript")})
    paragraphs = raw_trans.findAll("p")
    raw_names = []
    for p in paragraphs:
        paragraph = p.get_text()
        name = (paragraph.split(":"))[0]
        if name.isupper():
            raw_names.append(name)
    names = []
    for name in raw_names:
        if any(name in n for n in names):
            pass
        else:
            names.append(name)
    return names


#takes the story_dict and adds the guests' names, per the name_getter
def add_names(story_dict):
    for story in story_dict:
        story_dict[story]["Guests"] = name_getter(story_dict[story]["URL"])
    return story_dict


#prints 'em
def printer(story_dict):
    for story in story_dict:
        print str(story) + ". " + story_dict[story]["Slug"]
        for guest in story_dict[story]["Guests"]:
            print guest
        print


def test():
    NPR_URL = "http://www.npr.org/programs/all-things-considered/2015/03/07/391454506?showDate=2015-03-07"
    story_dict = add_names(transcript_links(get_links(NPR_URL)))
    printer(story_dict)


if __name__ == "__main__":
    test()
