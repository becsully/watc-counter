from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re


#given the URL of a show rundown, this will return a dictionary of each story in the rundown with links
def get_links(RUNDOWN_URL):
    r = requests.get(RUNDOWN_URL)
    soup = BeautifulSoup(r.text,'html.parser')
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
    #print URL #for testing
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


# accepts a dictionary of names and accompanying "paragraphs" (if applicable) --
# runs through them and returns final list of names
def name_checker(list_of_lists):

    namelist = []
    for pair in list_of_lists:
        if any(pair[0] in s for s in namelist):
            pass
        else: namelist.append(pair[0])

    # print namelist # for testing

    for item in list_of_lists:
        name = item[0]
        paragraph = item[1]

        # some basics:
        if ( "SOUNDBITE" in name ) or ( "(As " in paragraph ) or ( "LAUGHTER" in name ) or ( "(Singing)" in paragraph ):
            try: namelist.pop(namelist.index(name))
            except ValueError: pass
        if "UNIDENTIFIED" in name and len(paragraph.split(" ")) < 10:
            try: namelist.pop(namelist.index(name))
            except ValueError: pass
        if name.split(" ")[0] == "UNIDENTIFIED" and name.split(" ")[1] != "MAN" and name.split(" ")[1] != "WOMAN":
            try: namelist.pop(namelist.index(name))
            except ValueError: pass

        # checks for first initials
        if any(name[-1] in s for s in namelist):
            matches = []
            for s in namelist:
                s = s.split(" ")
                initialized_s = s[0][0] + ". " + s[-1]
                matches.append(initialized_s)
            if name in matches:
                namelist.pop(namelist.index(name))

    return namelist


#this runs through the transcript and returns the names of people quoted. this might not work for people with same last names.
def name_getter(STORY_URL):
    r = requests.get(STORY_URL)
    soup = BeautifulSoup(r.text)
    raw_trans = soup.find("div", {"class": re.compile("^transcript")})
    paragraphs = raw_trans.findAll("p")
    raw_names = []
    for p in paragraphs:
        raw_paragraph = p.get_text()
        try:
            colon = raw_paragraph.index(":")
            name = raw_paragraph[0:colon]
            paragraph = raw_paragraph[colon+1:]
        except ValueError:
            name = raw_paragraph
            paragraph = ""
        if name.isupper():
            raw_names.append([name, paragraph])
    # pprint(raw_names) # for testing
    final_names = name_checker(raw_names)
    return final_names


#takes the story_dict and adds the guests' names, per the name_getter
def add_names(story_dict):
    for story in story_dict:
        story_dict[story]["Guests"] = name_getter(story_dict[story]["URL"])
        #pprint(story_dict[story]) #for testing
    return story_dict


#prints 'em
def printer(story_dict):
    for story in story_dict:
        print str(story) + ". " + story_dict[story]["Slug"]
        for guest in story_dict[story]["Guests"]:
            print guest
        print


def test():
    #STORYURL = "http://www.npr.org/templates/transcript/transcript.php?storyId=391253086"
    #pprint(name_getter(STORYURL))
    NPR_URL = "http://www.npr.org/programs/all-things-considered/2015/03/10/392142419/all-things-considered-for-march-10-2015?showDate=2015-03-10"
    story_dict = add_names(transcript_links(get_links(NPR_URL)))
    printer(story_dict)


def main():
    NPR_URL = raw_input("Enter a URL: ")
    story_dict = add_names(transcript_links(get_links(NPR_URL)))
    printer(story_dict)


if __name__ == "__main__":
    main()
