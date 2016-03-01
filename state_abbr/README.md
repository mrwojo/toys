# US state abbreviations

US states have well-known 2-letter postal abbreviations, such as "CA" for California and "TX" for Texas.

## Ordering

Are the postal abbreviations in the same alphabetical order as the state names?

**No.** The ordering is obviously contradicted at a glance. The first two state names in alpha-order are Alabama and Alaska. Their abbreviations are AL and AK, which are in reverse order.

How could state names be abbreviated to have the same order?

An algorithm like this might work:

1. For each state name,
    1. The first letter of the abbreviation is the first letter of the state name.
    2. If the state name is a single word,
        1. The second letter of the abbreviation is the next letter of the state name that distinguishes it from the previous state name.
    3. Else:
        1. The second letter of the abbreviation is the next letter in the second word of the state name that distinguishes it from the previous state name.

So step through for ALABAMA and then ALASKA:

* (1) ALABAMA, (1.1) "A", (1.2.1) "L" second letter (there's no previous state name).
* (1) ALASKA, (1.1) "A", (1.2.1) "L" same as previous, "A" same as previous, "S" second letter.

Alabama is AL and Alaska is AS.

What are potential issues with this algorithm?

If new states are added with names that come between existing state names, then their abbreviations will be out of order.

Example: A new state called "Alaardvark" would claim the "AL" abbreviation.

## Trivia

* All state names starting with "W" also have the sequence "in": Wash*in*gton, West Virg*in*ia, Wiscons*in*, Wyom*in*g.
