#!/usr/bin/env python

__doc__ = "DeepScrape - Web Scraping using OSINT"
__author__ = "ThisLimn0"
__license__ = "MIT"
__version__ = "0.2.3"
__maintainer__ = "ThisLimn0"
__status__ = "Development"

#Standard library imports
from socket import timeout
import requests as req
from os import system

#Other library imports
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

##
##

class cC():
    """
    consoleColor
    source: https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDCC = '\033[0m'
    def Disable():
        cC.HEADER = ''
        cC.OKBLUE = ''
        cC.OKCYAN = ''
        cC.OKGREEN = ''
        cC.YELLOW = ''
        cC.RED = ''
        cC.WARNING = ''
        cC.FAIL = ''
        cC.GRAY = ''
        cC.BOLD = ''
        cC.UNDERLINE = ''
        cC.ENDCC = ''

##
##    

class ServerURL():
    
    def isAvailable(url, standardTimeout):
        """Checks whether a URL is available or not.

        Module Type: run on request

        Args:
            url (str): The URL to check.
            standardTimeout (int): The timeout to use for the request.

        Returns:
            bool: True if the URL is available, False if the URL is not available.
            Exception: An exception is raised if the request is returning an error.
        """
        try:
            headers = {
                'User-Agent': userAgentString
            }
            request = req.get(url, timeout=standardTimeout, headers=headers)
            if request.status_code == 200:
                # print("[*] Server is available.")
                return True
            else:
                return False
        except req.exceptions.RequestException:
            # print(f"{cC.GRAY}[E] Exception! Cannot scrape {url}{cC.ENDCC}")
            return False, Exception

    def hasSitemap(url, standardTimeout):
        '''Checks whether a sitemap exists at the given URL.

        ModuleType: run once
        
        Args:
            url (str): The URL to check.
            standardTimeout (int): The timeout to use for the request.
        
        #TODO: Maybe add support for direct host checking.
        
        Returns:
            bool: True if the sitemap exists, False if the sitemap does not exist.
            Exception: An exception is raised if the request is returning an error.
        '''
        standardSitemapLocation = url + "/sitemap.xml"
        try:
            headers = {
                'User-Agent': userAgentString
            }
            request = req.get(standardSitemapLocation, timeout=standardTimeout, headers=headers)
            if request.status_code == 200:
                return True
            else:
                return False
        except req.exceptions.RequestException:
            return False
    
    def isValid(url):
        """Checks whether `url` is a valid URL.

        Module Type: run on request

        Args:
            url (str): The URL to check.

        Returns:
            Tuple[bool]: True if the URL is in a valid format and scheme, False if the URL is not valid.

        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

##
##

class DeepScrape():

    def linkSegmentation(url):
        """
        Segments the URL into its components.
        """
        parsed = urlparse(url)
        return parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment

##
##

def splashScreen(url):
    print("\n")
    print("  `7MM'''Yb.                                .M'''bgd                                             ")
    print("    MM    `Yb.                             ,MI    'Y                                             ")
    print("    MM     `Mb  .gP'Ya   .gP'Ya `7MMpdMAo. `MMb.      ,p6'bo `7Mb,od8 ,6'Yb. `7MMpdMAo.  .gP'Ya  ")
    print("    MM      MM ,M'   Yb ,M'   Yb  MM   `Wb   `YMMNq. 6M'  OO   MM' ''8)   MM   MM   `Wb ,M'   Yb ")
    print("    MM     ,MP 8MwewR7' 8MwewR7'  MM    M8 .     `MM 8M        MM     ,pm9MX   MM    M8 8MwewR7' ")
    print("    MM    ,dP' YM.    , YM.    ,  MM   ,AP Mb     dM YM.    ,  MM    8M   MM   MM   ,AP YM.    , ")
    print("  .JMMmmmdP'    `Mbmmd'  `Mbmmd'  MMbmmd'  P*Ybmmd'   YMbmd' .JMML.  `Moo9^Yo. MMbmmd'   `Mbmmd' ")
    print("                                  MM                                           MM                ")
    print("                                .JMML.      O     S     I     N     T        .JMML.              ")
    print(f"                                          {cC.BOLD}DeepScrape v{__version__} by {__maintainer__}{cC.ENDCC}")
    print(f"                                                        {cC.BOLD}{cC.GRAY} Follow {cC.OKBLUE}every{cC.ENDCC}{cC.BOLD}{cC.GRAY} link... {cC.ENDCC}")
    print("\n")
    print(f"{cC.BOLD}[*]{cC.ENDCC} Provided destination: {cC.OKGREEN}{url}{cC.ENDCC}")

def init():
    # Default Value for requests to time out: 10 Seconds
    global standardTimeout
    standardTimeout = 10

    # Default User Agent String for web requests
    global userAgentString
    userAgentString = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"

    # Default Value for SSL Verification of requests
    global verifySSL
    verifySSL = True

    # Default Value for maximum number of urls to scrape: 500
    global maxUrls
    maxUrls = 500

    # Initialize sets of unique objects (internal/external URLs, found email_adresses, etc.)
    global queue
    queue = set()
    global urls
    urls = set()
    global internal_urls
    internal_urls = set()
    global external_urls
    external_urls = set()
    global email_adresses
    email_adresses = set()
    global phone_numbers
    phone_numbers = set()
    global open_directories
    open_directories = set()

    # Initialize basic variables
    global total_urls_visited
    total_urls_visited = 0

def manualAfterwork(url):
    '''
    looks for links in non html websites
    parsing the website and looking for links
    '''
    Scheme = urlparse(url).scheme
    Host = urlparse(url).netloc
    Website = req.get(url)
    WebsiteLines = Website.text.splitlines()
    for line in WebsiteLines:
        if not line.find("url:") == -1:
            line = line.split("url:")[1]
            line = line.split(":")[0]
            line = line.replace(" ", "")
            line = line.replace('"', '')
            line = line.replace(",", "")
            # line = line.replace("../", "")
            line = line.replace("//", "/")
            manualLink = Scheme + "://" + Host + "/" + line
            if not len(line) < 100:
                pass
            if manualLink not in internal_urls:
                if ServerURL.isValid(manualLink):
                    HTTP_RESPONSE = ServerURL.isAvailable(manualLink)
                    if HTTP_RESPONSE:
                        print(f"{cC.BOLD}[*]{cC.ENDCC} There may be more on {cC.OKGREEN}{manualLink}{cC.ENDCC}{cC.GRAY} is_valid_and_available:" + str(HTTP_RESPONSE) + "{cC.ENDCC}")
                        return manualLink
                    else:
                        manualLink = manualLink + "/"
                        HTTP_RESPONSE = ServerURL.isAvailable(manualLink)
                        if HTTP_RESPONSE:
                            print(f"{cC.BOLD}[*]{cC.ENDCC} There may be more on {cC.OKGREEN}{manualLink}{cC.ENDCC}{cC.GRAY} is_valid_and_available:" + str(HTTP_RESPONSE) + "{cC.ENDCC}")
                            return manualLink
    return False

def edgeCases():
    pass

def scrapeEmbedsScriptTag(url, standardTimeout):
    request = req.get(url, timeout=standardTimeout, verify=verifySSL).text
    # soup = BeautifulSoup(request, 'html.parser', from_encoding="iso-8859-1")
    soup = BeautifulSoup(request, 'html.parser')
    for script_tag in soup.findAll("script"):
        src = script_tag.attrs.get("src")
        if src == "" or src is None:
            # <src> tag is empty
            continue
        # join the URL if it's relative (not absolute link)
        src = urljoin(url, src)
        parsed_src = urlparse(src)
        # remove URL GET parameters, URL fragments, etc.
        src = parsed_src.scheme + "://" + parsed_src.netloc + parsed_src.path
        if not ServerURL.isValid(src):
            # not a valid URL
            continue
        if src in internal_urls:
            # already in the set
            continue
        if parsed_src.scheme == "javascript":
            # do not crawl links with "javascript"
            continue
        if parsed_src.scheme == "tel":
            src = src.split("tel:")[1]
            src = src.replace("/", "")
            src = src.replace("-", "/", 1)
            src = src.replace("  ", " ")
            if src not in phone_numbers:
                print(f"{cC.GRAY}[s] Phone number found: {src}{cC.ENDCC}")
                phone_numbers.add(src)
            continue
        if parsed_src.scheme == "mailto":
            src = src.split("mailto:")[1]
            src = src.replace("/", "")
            src = src.replace("'", "")
            src = src.replace(" ", "")
            src = src.replace("%40", "@")
            if not src in email_adresses:
                print(f"{cC.YELLOW}[s] E-Mail adress found: {src}{cC.ENDCC}")
                email_adresses.add(src)
            continue
        if domain not in src:
            # external link
            if src not in external_urls:
                # print(f"{cC.GRAY}[s] External link: {src}{cC.ENDCC}")
                external_urls.add(src)
            continue
        print(f"{cC.OKGREEN}[s] Internal link: {src}{cC.ENDCC}")
        urls.add(src)
        internal_urls.add(src)

def scrapeEmbedsATag(url, standardTimeout):
    request = req.get(url, timeout=standardTimeout, verify=verifySSL).text
    soup = BeautifulSoup(request, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # <a href=""> tag is empty.
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not ServerURL.isValid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if parsed_href.scheme == "javascript":
            # do not crawl links with "javascript"
            continue
        if parsed_href.scheme == "tel":
            href = href.split("tel:")[1]
            href = href.replace("/", "")
            href = href.replace("-", "/", 1)
            href = href.replace("  ", " ")
            if href not in phone_numbers:
                print(f"{cC.GRAY}[h] Phone number found: {href}{cC.ENDCC}")
                phone_numbers.add(href)
            continue
        if parsed_href.scheme == "mailto":
            href = href.split("mailto:")[1]
            href = href.replace("'", "")
            href = href.replace("/", "")
            href = href.replace(" ", "")
            href = href.replace("%40", "@")
            if not href in email_adresses:
                print(f"{cC.YELLOW}[h] E-Mail adress found: {href}{cC.ENDCC}")
                email_adresses.add(href)
            continue
        if domain not in href:
            # external link
            if href not in external_urls:
                # print(f"{cC.GRAY}[h] External link: {href}{cC.ENDCC}")
                external_urls.add(href)
            continue
        print(f"{cC.OKGREEN}[h] Internal link: {href}{cC.ENDCC}")
        urls.add(href)
        internal_urls.add(href)

def scrapeEmbedsLinkTag(url, standardTimeout):
    request = req.get(url, timeout=standardTimeout, verify=verifySSL).text
    soup = BeautifulSoup(request, "html.parser")
    for link_tag in soup.findAll("link"):
        link = link_tag.attrs.get("link")
        if link == "" or link is None:
            # link empty tag
            continue
        # join the URL if it's relative (not absolute link)
        link = urljoin(url, link)
        parsed_link = urlparse(link)
        # remove URL GET parameters, URL fragments, etc.
        link = parsed_link.scheme + "://" + parsed_link.netloc + parsed_link.path
        if not ServerURL.isValid(link):
            # not a valid URL
            continue
        if link in internal_urls:
            # already in the set
            continue
        if parsed_link.scheme == "javascript":
            # do not crawl links with "javascript"
            continue
        if parsed_link.scheme == "tel":
            link = link.split("tel:")[1]
            link = link.replace("/", "")
            link = link.replace("-", "/", 1)
            link = link.replace("  ", " ")
            if link not in phone_numbers:
                print(f"{cC.GRAY}[l] Phone number found: {link}{cC.ENDCC}")
                phone_numbers.add(link)
            continue
        if parsed_link.scheme == "mailto":
            link = link.split("mailto:")[1]
            link = link.replace("'", "")
            link = link.replace("/", "")
            link = link.replace(" ", "")
            link = link.replace("%40", "@")
            if not link in email_adresses:
                print(f"{cC.YELLOW}[l] E-Mail adress found: {link}{cC.ENDCC}")
                email_adresses.add(link)
            continue
        if domain not in link:
            # external link
            if link not in external_urls:
                # print(f"{cC.GRAY}[l] External link: {link}{cC.ENDCC}")
                external_urls.add(link)
            continue
        print(f"{cC.OKGREEN}[l] Internal link: {link}{cC.ENDCC}")
        urls.add(link)
        internal_urls.add(link)

def scrapeEmbedsImgTag(url, standardTimeout):
    request = req.get(url, timeout=standardTimeout, verify=verifySSL).text
    soup = BeautifulSoup(request, "html.parser")
    for img_tag in soup.findAll("img"):
            src = img_tag.attrs.get("src")
            if src == "" or src is None:
                # src empty tag
                continue
            # join the URL if it's relative (not absolute link)
            src = urljoin(url, src)
            parsed_src = urlparse(src)
            # remove URL GET parameters, URL fragments, etc.
            src = parsed_src.scheme + "://" + parsed_src.netloc + parsed_src.path
            if not ServerURL.isValid(src):
                # not a valid URL
                continue
            if src in internal_urls:
                # already in the set
                continue
            if parsed_src.scheme == "javascript":
                # do not crawl links with "javascript"
                continue
            if parsed_src.scheme == "tel":
                src = src.split("tel:")[1]
                src = src.replace("/", "")
                src = src.replace("-", "/", 1)
                src = src.replace("  ", " ")
                if src not in phone_numbers:
                    print(f"{cC.GRAY}[i] Phone number found: {src}{cC.ENDCC}")
                    phone_numbers.add(src)
                continue
            if parsed_src.scheme == "mailto":
                src = src.split("mailto:")[1]
                src = src.replace("'", "")
                src = src.replace("/", "")
                src = src.replace(" ", "")
                src = src.replace("%40", "@")
                if not src in email_adresses:
                    print(f"{cC.YELLOW}[i] E-Mail adress found: {src}{cC.ENDCC}")
                    email_adresses.add(src)
                continue
            if domain not in src:
                # external link
                if src not in external_urls:
                    pass
                    print(f"{cC.GRAY}[i] External link: {src}{cC.ENDCC}")
                    external_urls.add(src)
                continue
            print(f"{cC.OKGREEN}[i] Internal link: {src}{cC.ENDCC}")
            urls.add(src)
            internal_urls.add(src)

def scrapeXML(url, standardTimeout):
    pass

def scrapeJSON(url, standardTimeout):
    pass

def scrapeJavaScript(url, standardTimeout):
    pass

def scrapeCSS(url, standardTimeout):
    pass


def getAllLinks(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # domain name of the URL without the protocol
    global domain
    domain = urlparse(url).netloc

    # scheme_name = urlparse(url).scheme
    # SitemapUrl = scheme_name + "://" + domain_name + "/sitemap.xml"
    # if SitemapUrl not in urls:
    #     if check_if_sitemap_exists:
    #         print(f"{cC.GRAY}[*] {cC.ENDCC}{cC.OKGREEN}{scheme_name}://{domain_name}/sitemap.xml{cC.ENDCC}{cC.GRAY} found.{cC.ENDCC}")
    #         urls.add(SitemapUrl)
    if url in urls:
        return False
    Segments = url.rpartition('/')
    if Segments[0] not in internal_urls:
        if ServerURL.isValid(Segments[0]):
            internal_urls.add(Segments[0])
            urls.add(Segments[0])
    request = req.get(url)
    contentType = request.headers.get("Content-Type").split(";")[0]
    request = request.content
    
    soupInstance = BeautifulSoup(request, "html.parser")
    title = soupInstance.find('title')
    # contentType = soupInstance.find('meta', attrs={'http-equiv': 'Content-Type'})
    print(f"{url}: {title.text} --- {contentType}")
    '''
    If part of the title is "Index of", then it is a directory and we should definitely crawl it.
    '''
    if title and title.text.lower().find("index of") != -1:
        if url not in open_directories:
            print(f"{cC.YELLOW}[!] OPEN DIRECTORY:{cC.ENDCC}{cC.OKGREEN} {url}{cC.ENDCC}")
            open_directories.add(url)

    for a_tag in soupInstance.findAll("url"):
        if a_tag.find("loc"):
            link = a_tag.find("loc").text
            if link not in internal_urls:
                if ServerURL.isValid(link):
                    internal_urls.add(link)
                    urls.add(link)
    if contentType:
        # HTML Link Scraper
        if contentType == "text/html":
            # Get links that are in <script> tags
            scrapeEmbedsScriptTag(url, standardTimeout)
            # Get links that are in <a> tags
            scrapeEmbedsATag(url, standardTimeout)
            # Get links that are in <embed> tags
            scrapeEmbedsLinkTag(url, standardTimeout)
            # Get links that are in <img> tags
            scrapeEmbedsImgTag(url, standardTimeout)
    
        # XML Link Scraper
        if contentType == "text/xml":
            scrapeXML(url, standardTimeout)

        # JSON Link Scraper
        if contentType == "application/json":
            scrapeJSON(url, standardTimeout)

        # JavaScript Link Scraper
        if contentType == "application/javascript":
            scrapeJavaScript(url, standardTimeout)

        # CSS Link Scraper
        if contentType == "text/css":
            scrapeCSS(url, standardTimeout)

        # PDF Link Scraper
        if contentType == "application/pdf":
            pass

        # DATA Link Scraper
        if contentType == "application/data":
            pass
    else:
        print(f"{cC.RED}[x] {cC.ENDCC}{cC.OKGREEN}{url}{cC.ENDCC}{cC.GRAY} has no Content-Type.{cC.ENDCC}")
        raise Exception("No Content-Type")

    
    try:
        manualLink = manualAfterwork(url)
        if manualLink:
            if manualLink not in urls:
                print(f"[M] Manual: {manualLink}")
                urls.add(manualLink)
    except:
        pass

    return urls

def crawlJob(url, maxUrls, total_urls_visited):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        maxUrls (int): number of max urls to crawl, default is 30.
    """
    # print(f"{cC.YELLOW}[*] Crawling: {url}{cC.ENDCC}")
    UniqueUrls = set()
    UniqueUrls = getAllLinks(url)
    if UniqueUrls:
        pass
    total_urls_visited += 1
        # print(f"{cC.GRAY}[!] Error occurred while crawling the URL `{url}`{cC.ENDCC}")
        # raise Exception
    
    
    for weblink in UniqueUrls:
        if total_urls_visited > maxUrls:
             break
        # try: 
        if crawlJob(url=UniqueUrls, maxUrls=maxUrls, total_urls_visited=total_urls_visited):
            total_urls_visited += 1
        else:
            break
    # except:
        # print(Exception)
        print(f"{cC.GRAY}[!] Error occurred while crawling the URL '{UniqueUrls}'{cC.ENDCC}")
        pass
    # for obj in queue:
        # pass



if __name__ == "__main__":
    # If the script is run directly, this code will be executed.
    #
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--maxUrls", help="Number of max URLs to crawl, default is 500.", default=500, type=int)
    parser.add_argument("-t", "--timeout", help="Timeout in seconds, default is 10.", default=10, type=int)
    parser.add_argument("-d", "--dH", help="Display Header", default=True)
    args = parser.parse_args()
    #
    init()
    #
    url = args.url
    maxUrls = args.maxUrls # Default is 500
    standardTimeout = args.timeout # Default is 10
    displayHeader = args.dH # Default is True
    #
    if displayHeader:
        splashScreen(url)
    #
    # Enable logging?
    #
    print("Do you want to enable logging? [Yes/No]")
    print("                                ¯   ¯     ", end='')
    #
    if not input().lower() == "y" or "yes":
        Logging = False
        pass
    else:
        Logging = True
        pass
    #
    if ServerURL.isAvailable(url, standardTimeout):
        print(f"{cC.GRAY}[*] Server is available{cC.ENDCC}")
        print(f"{cC.YELLOW}[*] Crawling started for {url}{cC.ENDCC}")
        #
        # try:
        crawlJob(url, maxUrls, total_urls_visited)
        # except:
            # print(f"{cC.RED}Aborted operation.{cC.ENDCC}")
            # quit()
        #
        if len(open_directories) >= 1:
            print("\n")
            print("[+] Total Open Directories:", len(open_directories))
            print("[+] Open Directories:")
            for directory in sorted(open_directories):
                print(f"{cC.YELLOW}  {directory}{cC.ENDCC}")
        print("\n")
        print("Crawling finished. Report below.")
        print("------------------------------------------------------")
        print(f"{cC.OKGREEN}[+] Total URLs visited: {total_urls_visited}{cC.ENDCC}")
        print("[+] Total Internal links:", len(internal_urls))
        print("[+] Total External links:", len(external_urls))
        print("[+] Total unique URLs seen:", len(external_urls) + len(internal_urls))
        print("[+] Total E-Mail email_adresses:", len(email_adresses))
        print("[+] Total Phone numbers:", len(phone_numbers))
        #
        if Logging == True:
            # save the internal links to a file
            print("---")
            print("[+] Saving internal links to a file...")
            if len(internal_urls) >= 1:
                with open(f"{domain}_internal_links.txt", "w") as f:
                    for internal_link in sorted(internal_urls):
                        print(internal_link.strip(), file=f)

            # save the external links to a file
            print("[+] Saving external links to a file...")
            if len(external_urls) >= 1:
                with open(f"{domain}_external_links.txt", "w") as f:
                    for external_link in sorted(external_urls):
                        print(external_link.strip(), file=f)
            
            # save the phone numbers to a file
            print("[+] Saving phone numbers to a file...")
            if len(phone_numbers) >= 1:
                with open(f"{domain}_phone_numbers.txt", "w") as f:
                    for phone_number in sorted(phone_numbers):
                        print(phone_number.strip(), file=f)
            
            # save the e-mail email_adresses to a file
            print("[+] Saving e-mail email_adresses to a file...")
            if len(email_adresses) >= 1:
                with open(f"{domain}_e-mail_adresses.txt", "w") as f:
                    for adress in sorted(email_adresses):
                        print(adress.strip(), file=f)
            
            # save the open directories to a file
            print("[+] Saving open directories to a file...")
            if len(open_directories) >= 1:
                with open(f"{domain}_open_directories.txt", "w") as f:
                    for directory in sorted(open_directories):
                        print(directory.strip(), file=f)
        else:
            print("---")
            print("[+] Logging is disabled.")
    else:
        print(f"{cC.YELLOW}[!] Server is not available.{cC.ENDCC}")
        quit()
