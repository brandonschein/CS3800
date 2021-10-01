# Homework2
Time Spent: 6 hours

Resources:
- Lectures/Textbook
- https://docs.python.org/3/library/xml.etree.elementtree.html
- https://www.geeksforgeeks.org/create-xml-documents-using-python/
- https://www.google.com/url?sa=i&url=https%3A%2F%2Fcs.stackexchange.com%2Fquestions%2F6893%2Fis-this-intersection-of-dfas-correct&psig=AOvVaw0k7av6_WV7sv-7UqVOFPw3&ust=1633196714828000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCODnnITiqfMCFQAAAAAdAAAAABAD

Challenges: 
I faced some challenges in figuring out how I'm going to translate the xml files that had transitions in terms of each states 'id' 
while I was using each states 'name' to figure out the correct transition. I ended up building an "identity array" when getting the 
states from the xml that I would use later on to change my transitions from id based to state based and vise versa. Another challenge 
I faced was figuring out a way to build all possible strings of length 5 out of the alphabet. Using recursion I was able to solve this. 
One other challenge I had was figuring out how to print out the xml in stdout form as opposed to creating an xml file when finished running things 
like dfa2-xml and union. 
