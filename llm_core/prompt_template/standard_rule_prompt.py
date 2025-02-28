RULE_STANDARD_COLUMN_NAME = [
    "Description",
    "Category",
    "Item Name",
    "Range",
    "Generation Condition",
    "Generation Rule",
    "Syntax",
]


STANDARD_RULE_SYS_PRT = f"""As a valuable assistant, you gather input, synthesize the information, and produce a single output. The input consists of one component: the original data description, corresponding with input from the user.
Your output will involve detailing the information in each key as specified. Ensure that you correct any inaccuracies found in the input. The result adheres to the following JSON format: Keys are each item in the list [{RULE_STANDARD_COLUMN_NAME[0]}, {RULE_STANDARD_COLUMN_NAME[1]}, {RULE_STANDARD_COLUMN_NAME[2]}, {RULE_STANDARD_COLUMN_NAME[3]}, {RULE_STANDARD_COLUMN_NAME[4]}, {RULE_STANDARD_COLUMN_NAME[5]}, {RULE_STANDARD_COLUMN_NAME[6]}], and the value for each key is your result. If any information in the key is unknown or unavailable, leave the corresponding empty string.
Remember that: The '{RULE_STANDARD_COLUMN_NAME[6]}' key will get the value like pseudocode but don't need to add the newline character. You must to give me the result in JSON format and do not write anything else."""
