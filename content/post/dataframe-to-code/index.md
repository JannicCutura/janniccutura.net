---
title: Turning a pandas dataframe into code
subtitle: A short cut to reproducible pandas examples


# Summary for listings and search engines
summary: On sites like stack overflow, providing a minimal example to reproduce a problem makes the live of everyone much easier. This post shows a python function that turns your existing dataframe into a string of python code to ease the burden of providing a minial example. 

# Link this post with a project
projects: []

# Date published
date: "2022-02-02T00:00:00Z"

# Date updated
lastmod: "2022-02-02T00:00:00Z"

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: false

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  caption: 'Image credit: **Authors graph**'
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin


tags:
- Data engineering

#categories:
#- Demo
#- 教程
---
I love the [Stack Overflow](https://stackoverflow.com/) community! Over the course of the past ten years it has saved me coountless
hours and prevented  situations that what would have resulted in rage quits. Given the overwhelming willingness of complete
strangeres to help one another, the least one can do is make it as easy and comfortable as possible for them to help. 

It is therefore highly recommended to incluce a minimal example that reproduces the problem/issue at hand. Often I find myself
in situtations however, where I have a rather complex dataframe in memory that would take me quite some time to code up from scratch. 
Often have I wished there was a function `df_to_code(df)` that turns a pandas dataframe into python code that someone else can run
in oder to recreate that dataframe on their end. If you also wished such a thing existed, your wish has been answered ;)  


So, suppose you have the following dataframe in memory:
```python
df

Out[1]: 
   col_1 col_2
0      1     a
1      2     b
2      3     c
```

and have some problem that you would like to showcase on the data. You could of course provide code that creates the dataframe 
yourself: 
```python
df = pd.DataFrame(data={"col_1":[1,2,3], "col_2":["a","b","c"]})
```
but this can be annoying for more complicated frames. Instead of manually writing it, 
you can simply use `df_to_code()` in order to hand it to anyone (read: post it on StackOverflow):
```
df_to_code(df)
Out[95]: 'df = pd.DataFrame( np.array([[1,2,3], ["a", "b", "c"], ]), columns = ["col_1", "col_2"], index = [0, 1, 2] )'
```
	
All you need is the function below. It already covers most data types but I will add more in the future as I encounter problems. 
Drop me an email if you have encountered (and solved?) a problem with it:
```python
def df_to_code(df, n=10):
    """Takes a dataframe and returns python code to create it.
    Args:
        - df (pandas.core.DataFrame): A dataframe to convert to code
        - n (int): number of rows to keep
    Returns:
        - code (str): The code to create that DataFrame
    """
    df = df.convert_dtypes()
    df = df.head(n)
    columns = df.columns
    index = [str(id) for id in df.index]

    lists_of_data  = ""

    for column in df.columns:
        if df[column].dtype.name == "string":
            this_column_as_str = f"""["{'", "'.join(df[column].astype(str).to_list())}"], """
        else:
            this_column_as_str = f'[{",".join(df[column].astype(str).to_list())}], '


        lists_of_data += this_column_as_str

    code = f"""
    df = pd.DataFrame(
        np.array([{lists_of_data}]),
        columns = ["{'", "'.join(columns)}"],
        index = [{", ".join(index)}]
    )"""

    code = code.replace("\n","")
    code = code.replace("\'", "'")
    code = code.replace("nan", "np.NaN")
    code = ' '.join(code.split())

    return code
```
