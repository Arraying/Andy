config_schema = {
    "type": "object",
    "properties": {
        "domain": {
            "type": "object",
            "minProperties": 1,
            "patternProperties": {
                ".*": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "domain_threshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
        },
        "domain_keywords": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "domain_keywords_threshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
        },
        "path": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "path_threshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
        },
        "query": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "query_threshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
        },
    },
    "required": [
        "domain", "domain_threshold",
        "domain_keywords", "domain_keywords_threshold",
        "path", "path_threshold",
        "query", "query_threshold"
    ]
}
