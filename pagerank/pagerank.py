import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES) # Random Surfer Model
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    ranks = iterate_pagerank(corpus, DAMPING) # Iterative Algorithm
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename] 
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    output = dict()
    pages_num = len(corpus)    
    page_links = corpus[page]
    
    if page_links: # not empty
        for website in corpus:
            output[website] = (1 - damping_factor) / pages_num
            if website in page_links:
                output[website] += damping_factor / len(page_links) 
    else:
        # no outgoing links given the current page, eturn a probability distribution that chooses randomly among all pages with equal probability
        for website in corpus:
            output[website] = 1 / pages_num

    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Initialize a counter
    counter = {page: 0 for page in corpus}
    
    # Choose a starting page
    current_page = random.choice(list(corpus.keys()))

    # Simulate the random surfer
    n_steps = n
    while n_steps > 0:
        probabilities = transition_model(corpus, current_page, damping_factor)
        population = list(probabilities.keys())
        weights = list(probabilities.values())
        next_page = random.choices(
                                    population= population,
                                    weights= weights,
                                    k=1
                                ) # return a list with 1 element
        counter[next_page[0]] += 1
        current_page = next_page[0]
        n_steps -= 1

    # Normalize the counts
    for page in counter:
        counter[page] /= n
    
    # Return the result
    return counter


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    N = len(corpus)
    d = damping_factor
    threshold = 0.001

    # starting state: each page's rank is equally assigned 1/N
    page_rank = {page: 1/N for page in corpus}

    #----- PageRank Update ----#
    while True:       
        new_rank = {} 
        for p in corpus:
            sum_page_i = 0
            for i in corpus:
                # If page i links to p, add its share
                if p in corpus[i]:
                    sum_page_i += page_rank[i] / len(corpus[i])
                # If page i has no outgoing links, treat it as linking to all pages
                if len(corpus[i]) == 0:
                    sum_page_i += page_rank[i] / N

            new_rank[p] = (1-d) / N + d * sum_page_i 
            
        #----- Convergence Check ----#
        '''
        differences = [abs(new_rank[p] - page_rank[p]) for p in corpus] 
        if max(differences) < threshold:
            break
        '''
        
        if all(abs(new_rank[p] - page_rank[p]) < threshold for p in corpus):
             break # Stop the loop
        
        #----- Update Values ----#
        page_rank = new_rank

    # Return
    return page_rank

if __name__ == "__main__":
    main()