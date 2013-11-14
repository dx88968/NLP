NLP
===
Please read http://blog.csdn.net/yangliuy/article/details/8330640, I find it rather interesting.

###First work version
run.py method dataset_type data_path model output

* Method: lsa or plsa
* Dataset types: beetle or seb
* Model: 2 3 or 5

<code>
python run.py plsa beetle ../SemEval/train/beetle/Core/ 3 o.test
</code>

###Adout WSD before LSA/pLSA
There are 2 options:
 
* Considering Semantic info for each word: http://svn.ask.it.usyd.edu.au/trac/candc/wiki/boxer
* Replace 同义词、反义词 to a semantic space:http://blog.sina.cn/dpool/blog/s/blog_630aa24f01010xbb.html

###A complete working example
* http://www.codeproject.com/Articles/11835/WordNet-based-semantic-similarity-measurement
