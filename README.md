![plot](docs/readme_pics/IHU.png)
![plot](docs/readme_pics/DORG-Lab.png)

---

<h3 align="center">GG-Extraction-2022</h3>

## 📝 Table of Contents
- [Problem Definition](#problem_statement)
- [Dependencies](#dependencies)
- [Setting up a local environment](#getting_started)
- [Usage](#usage)
- [Future Scope](#future_scope)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## 🧐 Problem Definition <a name = "problem_statement"></a>
The administration of countries as well as the structure of the respective ministries are constantly changing. This fact, leads to redefinition of internal structure between Governmental Units and their responsibilities quite often. To manually extract the information and construct organization charts in parallel with responsibility assignments between ORgs is a time-consuming process. Based on that, this tool aims to automatically extract the RELATIONS and the RESPONSIBILITIES that a Public Administration Organization Presidential Decree may contain. 

## 🏁 Getting Started <a name = "getting_started"></a>

To install, simply git clone this ![repo](https://github.com/dorg-ihu/gg-extraction-2022/tree/testing).

Afterwards you need to install the ![requirements](https://github.com/dorg-ihu/gg-extraction-2022/blob/testing/requirements_gg22.txt). This can be done by:  
`pip install -r requirements_gg22.txt`

After setting all up, one can use command line to get the results that is interested in.  
All you have to do is to execute ![main.py](https://github.com/dorg-ihu/gg-extraction-2022/blob/testing/main.py) by providing the filepath of the pdf file you wish to parse and the respective task.  
The task can be either **RE** (stands for relation-extraction) or **RSP** (responsibility assignment).  

You can directly test, using the files available on file ![fek](https://github.com/dorg-ihu/gg-extraction-2022/tree/testing/fek-organismoi-upourgeiwn).
For example Simply execute:  
`python main.py --filepath fek-organismoi-upourgeiwn/yp-metanasteushskaiasulou-106-2020.pdf --task RE`

## ✍️ Authors <a name = "authors"></a>
- [@Ioannis Konstantinidis](https://github.com/ikonstas-ds)  
- [@Konstantinos Christantonis](https://github.com/konschri)
- [@Eleni Kapantai](https://github.com/ekapantai)


See also the list of [contributors](https://github.com/dorg-ihu/gg-extraction-2022/graphs/contributors) 
who participated in this project.

## 🎉 Acknowledgments <a name = "acknowledgments"></a>
We are really grateful on the authors of the following tools:
- ![gsoc2018-GG-extraction](https://github.com/eellak/gsoc2018-GG-extraction)
- ![gsoc2018-3gm](https://github.com/eellak/gsoc2018-3gm)

on which we relied on ... +text
