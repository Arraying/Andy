import typing
import urllib.parse
import tldextract


# noinspection PyTypeChecker
def levenshtein(s1: str, s2: str) -> float:
    """
    Computes the normalized Levenshtein distance between two strings.
    A value of 1 indicates a perfect match, 0 indicates completely different.
    This value will be continuous.
    Obtained from StackOverflow.
    :param s1: The first string.
    :param s2: The second string.
    :return: A value [0, 1].
    """
    l1 = len(s1)
    l2 = len(s2)
    matrix = [list(range(l1 + 1))] * (l2 + 1)
    for zz in list(range(l2 + 1)):
        matrix[zz] = list(range(zz, zz + l1 + 1))
    for zz in list(range(0, l2)):
        for sz in list(range(0, l1)):
            if s1[sz] == s2[zz]:
                matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
            else:
                matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
    distance = float(matrix[l2][l1])
    result = 1.0-distance/max(l1, l2)
    return result


def likeliness(value_to_match: str, against: typing.List[str]) -> float:
    """
    Evaluates the highest match for each component of the value to match.
    Components are strings separated by a dash.
    :param value_to_match: The value to match.
    :param against: A target list of strings to match the values against.
    :return: A value [0-1] where 1 implies at least one component was a perfect match.
    """
    parts = value_to_match.split('-')
    ceil = 0
    for safe in against:
        for i, part in enumerate(parts):
            check = levenshtein(part, safe)
            if check > ceil:
                ceil = check

    return ceil


def is_scam(config: dict, parsed: urllib.parse.ParseResult) -> bool:
    """
    Whether or not a specific parsed URL is flagged as a scam.
    This will try to evaluate the decision based off of at least one of these indicators:
    1. Domain very similar but not the same to a legit domain.
    2. Domain fairly similar to a legit domain and containing specific keywords.
    3. Domain path very similar to that of a legit domain.
    4. Domain querystring very similar to that of a legit domain.
    :param config: The config to use.
    :param parsed: The parsed URL.
    :return: True if it is, false otherwise.
    """

    # Load the criteria from the config.
    domain_tld = config["domain"]
    domain_keywords = config["domain_keywords"]
    against_domain = domain_tld.keys()
    against_path = config["path"]
    against_querystring = config["query"]
    threshold_domain = config["domain_threshold"]
    threshold_keywords = config["domain_keywords_threshold"]
    threshold_path = config["path_threshold"]
    threshold_querystring = config["query_threshold"]

    # Testing the main domain.
    netloc = parsed.netloc
    netloc_extract = tldextract.extract(netloc)
    domain = netloc_extract.domain
    check_domain = likeliness(domain, against_domain)
    if check_domain == 1:
        # We have an exact match, but we need to check against TLD.
        # If the TLD is different, this is 100% a scam.
        if domain not in against_domain:
            # One of the parts is a scam but the rest may not be, scam.
            return True
        return netloc_extract.suffix not in domain_tld[domain]
    # Anything above 0.8 is very suspicious.
    suspicious = check_domain > threshold_domain

    # We can ignore something not very suspicious.

    # We return early here since we can skip the other checks.
    if suspicious:
        return True

    # Testing for domain keywords.
    # This is only done for elevated risk domains.
    if check_domain > threshold_keywords:
        for keyword in domain_keywords:
            check_keyword = keyword in domain
            suspicious = suspicious or check_keyword

    # Testing for values in a path.
    path_values = parsed.path.split("/")
    for path in path_values:
        # Ignore empty paths.
        if not path:
            continue
        check_path = likeliness(path, against_path)
        # If there is an exact match, then it's a scam.
        # Use higher threshold for checking.
        suspicious = suspicious or check_path > threshold_path

    # Testing for certain query strings.
    query_values = urllib.parse.parse_qs(parsed.query)
    for query in query_values:
        # Ignore empty query values.
        if not query:
            continue
        check_query = likeliness(query, against_querystring)
        # Use higher threshold for checking.
        suspicious = suspicious or check_query > threshold_querystring

    # Return the final assessment.
    return suspicious


def assess(config: dict, input_lines: typing.List[str], target: bool) -> typing.List[str]:
    """
    Assesses any failures that the parser may encounter.
    :param config: The config to use.
    :param input_lines: The input lines.
    :param target: The target boolean the inputs should evaluate to.
    :return: A list of all wrongly matched URLs.
    """
    wrong = []
    for line in input_lines:
        line = line.strip()
        parsed = urllib.parse.urlparse(line)
        detected = is_scam(config, parsed)
        if detected != target:
            wrong.append(line)
    return wrong
