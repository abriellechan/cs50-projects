# LOGOS DESIGN FILE

## why I chose python
I chose to use python in order to create this webapp because I have much more experience with python, and there are
many libraries that are avaliable for me to utilize. For example, preproccessing tools for images, and the
pytesseract function that I needed to use. Python is slower than C or Swift, but I still decided to use python because
the program most likely will not be used to read very large images with large amounts of text, (which would be
where python slows down the program substantially.)

Although PHP could create more control in uploading the proper files, I did not choose it because Python libraries
were more accessible to me.

Even though using C or Swift would make the program run much faster, if I used Swift, my program would only be
accessible on mobile phones, which can be harder to test.

## pytesseract

I chose pytesseract in order to proccess images because it was an open source ocr resource that was also free.
It was also very easy to implement and use.
It is a wrapper for Google Tesseract.


## regex

There were many options to chose from when trying to make my program match words from the concern list to the
text output from my ocr function. I didn't want to make it so that the words needed to match exactly.

I took a look at fuzzywuzzy using Levenshtein distance, as well as spellcheck using Levenshtein distance.
However, I chose regex because it could compare a list to a long string, without needing to deal with commas
or special characters.