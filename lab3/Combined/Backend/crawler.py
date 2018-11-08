# Copyright (C) 2011 by Peter Goodman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''Useful notes to self: The crawler object has some useful member entities:
1. _curr_words: a list of pairs that stores word id as its first element and font size as its second element
2. _doc_id_cache: a dictionary that stores url name on the current page as its key and doc_id as its value
3. _word_id_cache: a dictionary that stores word string as key and word id as its value
4. _document_index: a list of all the documents crawled, the index of each entry is the actual document id
5. _lexicon: a list of all the words crawled, the index of each entry is the actual word id
6. _lexicon_dic: a dictionary that has each lexicon as key and their word_id as value for quick searching
7. _url_link: a list of pairs, the first element in the pair is from_doc_id, the second is to_url_id
8. _first_20_words: a dictionary that records the first 20 words on each website crawled, the key is url, value is
                    a list of the first 20 words on that website
9. _document_title: a dictionary that records the title of each website, key is url, value is a string(its title)'''


import urllib2
import urlparse
from BeautifulSoup import *
from collections import defaultdict
import re
import pageRank


def attr(elem, attr):
    """An html attribute from an html element. E.g. <a href="">, then
    attr(elem, "href") will get the href or an empty string."""
    try:
        return elem[attr]
    except:
        return ""


WORD_SEPARATORS = re.compile(r'\s|\n|\r|\t|[^a-zA-Z0-9\-_]')


class crawler(object):
    """Represents 'Googlebot'. Populates a database by crawling and indexing
    a subset of the Internet.

    This crawler keeps track of font sizes and makes it simpler to manage word
    ids and document ids."""

    def __init__(self, db_conn, url_file):
        """Initialize the crawler with a connection to the database to populate
        and with the file containing the list of seed URLs to begin indexing."""
        self._url_queue = []
        self._doc_id_cache = {}
        self._word_id_cache = {}
        # this is a list that contains all the documents' urls as elements,
        # the documents' ids are their index in this list
        # the first id (id 0) is invalid
        self._document_index=["Invalid index: indices start at 1"]
        # similar to _document_index, _lexicon stores all the words that had been crawled in the indexes
        # that is their word_id
        self._lexicon=["Invalid index: indices start at 1"]
        #a dictionary that has each lexicon as key and their word_id as value for quick searching
        self._lexicon_dic={}
        # this is a dictionary that has word id as the key, and the list of document ids that contains this word
        # as the value
        self._inverted_index={}
        # same thing as _inverted_index, but it has the actual word string as its key and actual url as its value
        self._resolved_inverted_index={}
        # a list of pairs of from_url and to_utl used by pagerank system
        self._url_link=[]
        # a dictionary of url as key and the first 20 words on that url as value
        self._first_20_words={}
        # a dictionary that stores the titles of each url crawled
        self._document_title={}

        self._curr_url_word_count=0


        # functions to call when entering and exiting specific tags
        self._enter = defaultdict(lambda *a, **ka: self._visit_ignore)
        self._exit = defaultdict(lambda *a, **ka: self._visit_ignore)

        # add a link to our graph, and indexing info to the related page
        self._enter['a'] = self._visit_a

        # record the currently indexed document's title an increase
        # the font size
        def visit_title(*args, **kargs):
            self._visit_title(*args, **kargs)
            self._increase_font_factor(7)(*args, **kargs)

        # increase the font size when we enter these tags
        self._enter['b'] = self._increase_font_factor(2)
        self._enter['strong'] = self._increase_font_factor(2)
        self._enter['i'] = self._increase_font_factor(1)
        self._enter['em'] = self._increase_font_factor(1)
        self._enter['h1'] = self._increase_font_factor(7)
        self._enter['h2'] = self._increase_font_factor(6)
        self._enter['h3'] = self._increase_font_factor(5)
        self._enter['h4'] = self._increase_font_factor(4)
        self._enter['h5'] = self._increase_font_factor(3)
        self._enter['title'] = visit_title

        # decrease the font size when we exit these tags
        self._exit['b'] = self._increase_font_factor(-2)
        self._exit['strong'] = self._increase_font_factor(-2)
        self._exit['i'] = self._increase_font_factor(-1)
        self._exit['em'] = self._increase_font_factor(-1)
        self._exit['h1'] = self._increase_font_factor(-7)
        self._exit['h2'] = self._increase_font_factor(-6)
        self._exit['h3'] = self._increase_font_factor(-5)
        self._exit['h4'] = self._increase_font_factor(-4)
        self._exit['h5'] = self._increase_font_factor(-3)
        self._exit['title'] = self._increase_font_factor(-7)

        # never go in and parse these tags
        self._ignored_tags = set([
            'meta', 'script', 'link', 'meta', 'embed', 'iframe', 'frame',
            'noscript', 'object', 'svg', 'canvas', 'applet', 'frameset',
            'textarea', 'style', 'area', 'map', 'base', 'basefont', 'param',
        ])

        # set of words to ignore
        self._ignored_words = set([
            '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ])

        # TODO remove me in real version
        self._mock_next_doc_id = 1
        self._mock_next_word_id = 1

        # keep track of some info about the page we are currently parsing
        self._curr_depth = 0
        self._curr_url = ""
        self._curr_doc_id = 0
        self._font_size = 0
        self._curr_words = None

        # get all urls into the queue
        try:
            with open(url_file, 'r') as f:
                for line in f:
                    self._url_queue.append((self._fix_url(line.strip(), ""), 0))
        except IOError:
            pass

    # TODO remove me in real version
    def _mock_insert_document(self, url):
        """A function that pretends to insert a url into a document db table
        and then returns that newly inserted document's id."""
        ret_id = self._mock_next_doc_id
        self._mock_next_doc_id += 1
        return ret_id

    # TODO remove me in real version
    def _mock_insert_word(self, word):
        """A function that pretends to inster a word into the lexicon db table
        and then returns that newly inserted word's id."""
        ret_id = self._mock_next_word_id
        self._mock_next_word_id += 1
        return ret_id

    def word_id(self, word):
        """Get the word id of some specific word.
            note: input argument word is a string"""
        if self._curr_url_word_count<=20:
            if self._curr_url_word_count==0:
                self._first_20_words[self._curr_url]=[word]
            else:
                self._first_20_words[self._curr_url].append(word)
            self._curr_url_word_count+=1
        if word in self._word_id_cache:
            self._resolved_inverted_index[word].add(self._curr_url)
            self._inverted_index[self._word_id_cache[word]].add(self._curr_doc_id)
            return self._word_id_cache[word]

        # TODO: 1) add the word to the lexicon, if that fails, then the
        #          word is in the lexicon
        #       2) query the lexicon for the id assigned to this word,
        #          store it in the word id cache, and return the id.

        # this only execute when the argument doesn't exist in _word_id_cache
        # it will add the argument as a new entry to _word_id_cache
        word_id = self._mock_insert_word(word)
        self._word_id_cache[word] = word_id
        self._lexicon.append(word)
        # adds the current document id into inverted index
        self._resolved_inverted_index[word]=set([self._curr_url])
        self._inverted_index[self._word_id_cache[word]]=set([self._curr_doc_id])
        return word_id

    def document_id(self, url):
        """Get the document id for some url."""
        if url in self._doc_id_cache:
            return self._doc_id_cache[url]

        # TODO: just like word id cache, but for documents. if the document
        #       doesn't exist in the db then only insert the url and leave
        #       the rest to their defaults.

        doc_id = self._mock_insert_document(url)
        self._doc_id_cache[url] = doc_id
        self._document_index.append(url)
        return doc_id

    def _fix_url(self, curr_url, rel):
        """Given a url and either something relative to that url or another url,
        get a properly parsed url."""

        rel_l = rel.lower()
        if rel_l.startswith("http://") or rel_l.startswith("https://"):
            curr_url, rel = rel, ""

        # compute the new url based on import
        curr_url = urlparse.urldefrag(curr_url)[0]
        parsed_url = urlparse.urlparse(curr_url)
        return urlparse.urljoin(parsed_url.geturl(), rel)

    def add_link(self, from_doc_id, to_doc_id):
        """Add a link into the database, or increase the number of links between
        two pages in the database."""
        # TODO

    def _visit_title(self, elem):
        """Called when visiting the <title> tag."""
        title_text = self._text_of(elem).strip()
        print "document title=" + repr(title_text)

        # TODO update document title for document id self._curr_doc_id
        self._document_title[self._curr_doc_id]=repr(title_text)

    def _visit_a(self, elem):
        """Called when visiting <a> tags."""

        dest_url = self._fix_url(self._curr_url, attr(elem, "href"))

        # print "href="+repr(dest_url), \
        #      "title="+repr(attr(elem,"title")), \
        #      "alt="+repr(attr(elem,"alt")), \
        #      "text="+repr(self._text_of(elem))

        # add the just found URL to the url queue
        self._url_queue.append((dest_url, self._curr_depth))

        # add a link entry into the database from the current document to the
        # other document
        self.add_link(self._curr_doc_id, self.document_id(dest_url))

        # TODO add title/alt/text to index for destination url

    def _add_words_to_document(self):
        # TODO: knowing self._curr_doc_id and the list of all words and their
        #       font sizes (in self._curr_words), add all the words into the
        #       database for this document
        print "    num words=" + str(len(self._curr_words))

    def _increase_font_factor(self, factor):
        """Increade/decrease the current font size."""

        def increase_it(elem):
            self._font_size += factor

        return increase_it

    def _visit_ignore(self, elem):
        """Ignore visiting this type of tag"""
        pass

    def _add_text(self, elem):
        """Add some text to the document. This records word ids and word font sizes
        into the self._curr_words list for later processing."""
        words = WORD_SEPARATORS.split(elem.string.lower())
        for word in words:
            word = word.strip()
            if word in self._ignored_words:
                continue
            self._curr_words.append((self.word_id(word), self._font_size))


    def _text_of(self, elem):
        """Get the text inside some element without any tags."""
        if isinstance(elem, Tag):
            text = []
            for sub_elem in elem:
                text.append(self._text_of(sub_elem))

            return " ".join(text)
        else:
            return elem.string

    def _index_document(self, soup):
        """Traverse the document in depth-first order and call functions when entering
        and leaving tags. When we come accross some text, add it into the index. This
        handles ignoring tags that we have no business looking at."""

        class DummyTag(object):
            next = False
            name = ''

        class NextTag(object):
            def __init__(self, obj):
                self.next = obj

        tag = soup.html
        stack = [DummyTag(), soup.html]

        while tag and tag.next:
            tag = tag.next

            # html tag
            if isinstance(tag, Tag):

                if tag.parent != stack[-1]:
                    self._exit[stack[-1].name.lower()](stack[-1])
                    stack.pop()

                tag_name = tag.name.lower()

                # ignore this tag and everything in it
                if tag_name in self._ignored_tags:
                    if tag.nextSibling:
                        tag = NextTag(tag.nextSibling)
                    else:
                        self._exit[stack[-1].name.lower()](stack[-1])
                        stack.pop()
                        tag = NextTag(tag.parent.nextSibling)

                    continue

                # enter the tag
                self._enter[tag_name](tag)
                stack.append(tag)

            # text (text, cdata, comments, etc.)
            else:
                self._add_text(tag)

    def print_inverted_index(self):
        for word_id in self._inverted_index:
            print str(word_id) + " : " + str(self._inverted_index[word_id])

    def print_resolved_inverted_index(self):
        for word in self._resolved_inverted_index:
            print word + " : " + str(self._resolved_inverted_index[word])

    def get_inverted_index(self, do_print=False):
        # returns the inverted index built during crawling
        if do_print:
            self.print_inverted_index()
        return self._inverted_index

    def get_resolved_inverted_index(self, do_print=False):
        # returns the resolved inverted index
        if do_print:
            self.print_resolved_inverted_index()
        return self._resolved_inverted_index

    def create_dictionary_lexicon(self):
        #add each word in lexicon list into the dictionary as key, and its index as value
        for index in range(len(self._lexicon)):
            if index==0:
                continue
            self._lexicon_dic[self._lexicon[index]]=index


    def crawl(self, depth=2, timeout=3):
        """Crawl the web!"""
        seen = set()

        while len(self._url_queue):

            url, depth_ = self._url_queue.pop()

            # skip this url; it's too deep
            if depth_ > depth:
                continue

            doc_id = self.document_id(url)

            # we've already seen this document
            if doc_id in seen:
                continue

            seen.add(doc_id)  # mark this document as haven't been visited

            socket = None
            try:
                socket = urllib2.urlopen(url, timeout=timeout)
                soup = BeautifulSoup(socket.read())
                #if self._curr_doc_id != 0:
                self._curr_url_word_count=0
                self._url_link.append((self._curr_doc_id, doc_id))

                self._curr_depth = depth_ + 1
                self._curr_url = url
                self._curr_doc_id = doc_id
                self._font_size = 0
                self._curr_words = []
                self._index_document(soup)
                self._add_words_to_document()

                # print "length of _cache_word_id is " + str(len(self._word_id_cache))
                # print "next word id is " + str(self._mock_next_word_id)
                print "    url=" + repr(self._curr_url)

            except Exception as e:
                print e
                pass
            finally:
                if socket:
                    socket.close()
                self.create_dictionary_lexicon()

def simulate_a_search(search_word, bot, result_page_rank):
    #first locate the searched word's id
    search_word_id=bot._lexicon_dic.get(search_word,0)
    if search_word_id==0:
        print "Could not find word"
        return
    #next we get the list of urls containing this word
    url_id_list=bot._inverted_index[search_word_id]
    url_id_scores={}
    doc_urls = []
    #get the score for every urls
    for url_id in url_id_list:
        url_id_scores[url_id]=result_page_rank[url_id]
    #sort the dictionary of url ids based on their score
    sorted_by_score=sorted(url_id_scores.items(), key=lambda t:t[1])
    print sorted_by_score
    url_sorted_by_score=[]
    #get the actual website urls text
    for pair in reversed(sorted_by_score):
        url_sorted_by_score.append(bot._document_index[pair[0]])
    print url_sorted_by_score








if __name__ == "__main__":
    bot = crawler(None, "urls.txt")
    bot.crawl(depth=1)
    result_page_rank=pageRank.page_rank(bot._url_link)
    searched_word="google"
    simulate_a_search(searched_word, bot, result_page_rank)


