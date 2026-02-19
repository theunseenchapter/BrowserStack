import re
from collections import Counter


def find_repeated_words(titles):
    # collect all words from the translated titles and count them
    all_words = []
    for t in titles:
        all_words.extend(re.findall(r"[a-zA-Z]+", t.lower()))

    word_counts = Counter(all_words)

    # we only care about words that show up more than 2 times
    repeated = {}
    for word, cnt in word_counts.items():
        if cnt > 2:
            repeated[word] = cnt
    return repeated


def print_word_analysis(repeated):
    print("\n--- Word Frequency Analysis (Translated Titles) ---")
    if repeated:
        print("Words appearing more than twice across all headers:")
        for word, count in sorted(repeated.items(), key=lambda x: -x[1]):
            print(f"  {word}: {count}")
    else:
        print("  No words repeated more than twice.")
    print()
