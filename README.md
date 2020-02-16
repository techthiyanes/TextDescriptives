# TextDescriptives

A Python package for calculating a large variety of statistics from text(s).

Currently covers:

1. Basic descriptive statistics - mean, median, standard deviation of the following:
  * Word length
  * Sentence length, words
  * Sentence length, characters (TODO)
  * Syllables per word
  * Number of characters
  * Number of sentences
  * Number of types (unique words)
  * Number of tokens (total words)
  * Type/toḱen ratio
  * Lix
  * Rix

2. Readability measures:
  * Gunning-Fog
  * SMOG
  * Flesch reading ease
  * Flesch-Kincaid grade
  * Automated readability index
  * Coleman-Liau index
  
 3. Etymology-related measures:
  * Percentage words with Germanic origin
  * Percentage words with Latinate origin
  * Latinate/Germanic origin ratio
  
 4. Dependency distance meaures:
  * Mean dependency distance, sentence level (mean, standard deviation)
  * Mean proportion adjacent dependency relation, sentence level (mean, standard devaiation)
  
 ## Usage
 
 
 When instantiating the class you should specify which categories of measures you want to calculate.
 The categories to choose from are \['all', 'basic', 'readability', 'etymology', 'dep_distance']. Default is 'all'.
 Text input can be both a string, list of strings or Pandas series of type string. Output comes in the format of a pandas dataframe with a row for each text and a column for each measure. 

```
 from textdescriptives import Textdescriptives

#The module takes input in the following form:
Textdescriptives(text, language, category, measures, snlp_path)

test_text = 'The world is changed. I feel it in the water. I feel it in the earth. I smell it in the air. Much that once was is lost, for none now live who remember it.'

t = Textdescriptives(test_text, language = 'en', category = 'basic')
t.get_df()
```
|    | Text                                                                                                                                                        |   avg_word_length |   median_word_length |   std_word_length |   avg_sentence_length |   median_sentence_length |   std_sentence_length |   avg_syl_per_word |   median_syl_per_word |   std_syl_per_word |   type_token_ratio |     lix |   rix |   n_types |   n_sentences |   n_tokens |   n_chars |
|---:|:------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------:|---------------------:|------------------:|----------------------:|-------------------------:|----------------------:|-------------------:|----------------------:|-------------------:|-------------------:|--------:|------:|----------:|--------------:|-----------:|----------:|
|  0 | The world is changed.(...)  |           3.28571 |                    3 |           1.54127 |                     7 |                        6 |               3.09839 |            1.08571 |                     1 |           0.368117 |           0.657143 | 12.7143 |   0.4 |        24 |             5 |         35 |       121 |

If you only want a subset of the basic statistics they can be specified in the 'measures' parameter as a ĺist.

```
Textdescriptives(test_text, language = 'en', category = 'basic', measures = ['avg_word_length', 'n_chars']).get_df()
```

|    | Text                                                                                                                                                        |   avg_word_length |   n_chars |
|---:|:------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------:|----------:|
|  0 | The world is changed.(...) |           3.28571 |       121 |


### Readability

The readability measures are largely derived from the [textstat][https://github.com/shivam5992/textstat] library and are more thoroughly defined there.

### Etymology

The etymology measures are calculated using [macroetym][https://github.com/JonathanReeve/macro-etym] only slightly rewritten to be called from a script. They are calculated since in English, a greater frequency of words with a Latinate origin tends to indicate a more formal language register. 

### Dependency Distance

Mean dependency distance can be used as a way of measuring the average syntactic complexity of a text.
```

```
