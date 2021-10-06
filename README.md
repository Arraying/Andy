# Andy

Andy* is an anti-typosquatting suite created to **combat Steam Tradelink & Discord Nitro fraud** links. 
With a correct configuration, Andy will achieve a ridiculous accuracy.
In my tests, Andy achieved a 100% accuracy rate (0% false-negatives) with 0% false positives.

While Andy was developed with Steam and Discord in mind, it can hypothetically used for virtually any websites.

*\*any resemblance to persons, whether real or ficticious, is purely coincidental.*

## How it works

Given a URL, called test URL henceforth, it should be checked whether or not it is a fraudulent URL given the config provided.
In essence, Andy will compute the normalized [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) between the test URL and configured valid domains. 
If this distance shows high similarity, or it contains part of a valid domain (think `discord-nitro` containing `discord` from `discord.com`) it will flag the URL as fraudulent.
Alternatively, it will attempt to perform similar comparisons on the domain contents, URL path and URL querystrings in order to compute a final verdict.

## Configuration

Andy requires a valid configuration dictionary.
This will consist of the following keys:

| Key | Type | Description |
| --- | --- | --- |
| `domain` | dict of string keys and string array values | A dictionary of all legitimate domains (2nd/3rd level) with their associated TLDs. |
| `domain_keywords` | string array | A list of fraudulent keywords in the domain. |
| `path` | string array | A list of fraudulent keywords in the path. |
| `query` | string array | A list of fraudulent keywords in a querystring. |

**Note:** All fields except `domain_keywords` use Levenshtein distance to trigger with "similar" strings. 
For example, the keyword "gift" will cause "g1ft" to trigger too.
Additionally, there must be at least one value in `domain`.

## Example

For example, using (not all config elements are shown):
```python
"domain": {
  "discord": ["com", "gg", "gift"],
  "steamcommunity": ["com"]
}
```

The following URLs will be evaluated as follows:
* `discord.com` -> No fraud
* `d1scorrd.com` -> Fraud
* `discord.biz` -> Fraud
* `steamcommunity.com` -> No fraud
* `streamcommmunity.com` -> Fraud


## Usage (library)

Andy can be used as a library for other projects.
Documentation to be added here.

## Usage (command line)

Andy can be run from the command line to test the accuracy of dection.
For this, two files are needed.
Both files contain one domain per line (tailing and leading whitespace is ignored).
The first file, referred to as the legitimate file, will contain only URLs that are not considered fraud.
The second file, referred to as the scam file, will contain only URLs that are fraudulent.
Andy will then test how many of the URLs from the legitimate file Andy flags as fraudulent, and vice versa.

As such, 3 command line arguments are required:
1. The path of the config file (must be stored in JSON format).
2. The path of the legitimate file.
3. The path of the scam file.
