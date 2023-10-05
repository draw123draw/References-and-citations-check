# References-and-citations-check
An python code using grep to help check the consistence of the citations in an academic essay or thesis with the references in the end of it.

使用方法：
将目标文献中的所有内容通过ctrl+A全选并复制粘贴到两份txt文件中并进行删减，其中一份仅保留正文，另一份仅保留参考文献列表且尽量保证一个换行符(回车)一个参考文献的格式

大概原理：
正则表达式，也可以理解为高级的查找，查找论文文献引用的核心思想为被括号括起来，且以 "18/19/20" 年分开头的4位数字，使用python通常自带的regex库便可以运行。
