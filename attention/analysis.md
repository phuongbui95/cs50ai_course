# Analysis

## Layer 8, Head 7: End-of-Sequence Context

This head appears to learn sequence completion patterns by paying attention to the `[SEP]` token. It's particularly interesting in how it helps predict contextually appropriate endings.

Example Sentences:
- "The cat sat on the [MASK]." (high attention between "sat" and "[SEP]")
  - Predicts: mat, floor, couch
- "My favorite color is [MASK]." (strong attention from "is" to "[SEP]")
  - Predicts: blue, red, green

## Layer 1, Head 2: Pronoun Resolution

This head demonstrates strong pronoun-antecedent relationships, helping resolve references in complex sentences.

Example Sentences:
- "The dog chased its [MASK]." (high attention between "its" and "dog")
  - Predicts: tail, owner, ball
- "She told him that she would [MASK] tomorrow." (attention links both instances of "she")
  - Predicts: come, return, leave

## Layer 5, Head 3: Verb-Object Relationships

This head shows consistent attention patterns between verbs and their direct objects, helping predict semantically appropriate completions.

Example Sentences:
- "The chef cooked the [MASK]." (strong attention from "cooked" to predicted object)
  - Predicts: food, meal, dinner
- "Students read their [MASK] carefully." (attention from "read" to object)
  - Predicts: books, notes, assignments

## Layer 2, Head 8: Adjective-Noun Agreement

This head appears to learn adjective-noun relationships, helping ensure semantic consistency in descriptions.

Example Sentences:
- "The tall green [MASK] stood in the garden." (attention between adjectives and predicted noun)
  - Predicts: tree, plant, shrub
- "An ancient stone [MASK] was discovered." (strong attention from modifiers to noun)
  - Predicts: temple, statue, monument
