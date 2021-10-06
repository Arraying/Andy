import andy
import json
import jsonschema
import sys

# The configuration file schema.
config_schema = {
    "type": "object",
    "properties": {
        "domain": {
            "type": "object",
            "minProperties": 1,
            "patternProperties": {
                "^I_": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "domain_keywords": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "path": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "query": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
    },
    "required": ["domain", "domain_keywords", "path", "query"]
}

# Get the command line options.
args = sys.argv[1:]
# Ensure that all command line options are there.
if len(args) < 1:
    print("Please provide the config file.")
    sys.exit(1)
if len(args) < 2:
    print("Please provide a text file of legitimate links.")
    sys.exit(1)
if len(args) < 3:
    print("Please provide a text file of scam links.")
    sys.exit(1)

# Load the files.
try:
    with open(args[0], "r") as config_file:
        # Load the config and validate it.
        config_json = json.load(config_file)
        jsonschema.validate(schema=config_schema, instance=config_json)

        # Test run against the legit set - check for false positives.
        with open(args[1]) as legit:
            legit_link = legit.readlines()
            result = andy.assess(config_json, legit_link, False)
            print(f"False positive count: {len(result)}")
            for issue in result:
                print(f"- {issue}")

        # Test run against the scam set - check for false negatives.
        with open(args[2]) as scams:
            scam_link = scams.readlines()
            result = andy.assess(config_json, scam_link, True)
            print(f"False negative count: {len(result)}")
            for issue in result:
                print(f"- {issue}")

except (json.JSONDecodeError, jsonschema.ValidationError) as error:
    print("Config parsing/validation error, please check the structure.")
    print(error)
    sys.exit(1)

except IOError as error:
    print("An error occurred opening one of the files.")
    print(error)
    sys.exit(1)
