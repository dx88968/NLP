NLP
===
Please read http://blog.csdn.net/yangliuy/article/details/8330640, I find it rather interesting.

###First work version

evaluation.py dataset_type path mode output

<code>
python evaluation.py beetle ../SemEval/train/beetle/Core/ 3 o.test
</code>

Adout WSD before LSA/pLSA, There are 2 options:
1. Considering Semantic info for each word: http://svn.ask.it.usyd.edu.au/trac/candc/wiki/boxer
2. Replace 同义词、反义词 to a semantic space:http://blog.sina.cn/dpool/blog/s/blog_630aa24f01010xbb.html
