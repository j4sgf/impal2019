Jafar - QnA System with Hadith Sahih-Bukhari as Corpus
TUGAS IMPAL 2019
1301154157
----------------------------------------------------

|Twitter|

The basic idea of this project is to create a system that can answer Islamic factual question. With English translation of Hadith Sahih Bukhari book as the corpus for answers. The corpus is not a knowledge base, it is a document consisting 7356 verses of Hadith. Hence, it is inherently harder for the system to read and extract answer directly. The system able to receive an input posed in natural language such as "When was Prophert Muhammad born?" or "What are the best deed we can do to pleases Allah?". A keyword based search was used. First the user question went through preprocessing phase where keyword is extracted. Then, the keywords were used to search the corpus looking for matching verses. After that, the system used scoring and ranking to find the best matched verse and then return the corresponding answer for the question.




Requirements
------------

`Python 3 <https://docs.python.org/3/>`__

Package dependencies listed in ``requirements.txt``


Features
~~~~~~~~

-  Take query in natural language as an input
-  Train SVM classifier using predefined data set
-  System able to process inputted query into a machine readable format for further processing
-  System able to extract features and keywords from input
-  Scrap internet for Hadith


TODO
~~~~

.. |Twitter| image:: https://img.shields.io/twitter/follow/openebs.svg?style=social&label=Follow
   :target: https://twitter.com/intent/follow?screen_name=jafarassagaf
