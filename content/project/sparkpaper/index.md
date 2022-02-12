---
title: Econometrics at Scale
summary: This project and the associated repository document how to used Spark to run several regresion frameworks frequently employed in economics. 
tags:
- Data engineering
date: "2019-04-27T00:00:00Z"

# Optional external URL for project (replaces project detail page).
external_link: ""

image:
  caption: Authors graph
  focal_point: Smart

links:
- icon: github
  icon_pack: fab
  name: Github
  url: https://github.com/benjaminbluhm/econometrics_at_scale
url_code: ""
url_pdf: ""
url_slides: ""
url_video: ""

# Slides (optional).
#   Associate this project with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
#slides: example
---


The [github repository](https://github.com/benjaminbluhm/econometrics_at_scale) contains the source code and dataset to reproduce the parallel computing exercise described in the paper:

### Econometrics at Scale: Spark Up Big Data in Economics
##### Benjamin Bluhm & Jannic Cutura

#### Abstract
*This paper provides an overview of how to use ''big data'' for economic research. We investigate the performance and ease of use of different Spark applications running on a distributed file system to enable the handling and analysis of data sets which were previously not usable due to their size. More specifically, we explain how to use Spark to (i) explore big data sets which exceed retail grade computers memory size and (ii) run typical econometric tasks including microeconometric, panel data and time series regression models which are prohibitively expensive to evaluate on stand-alone machines. By bridging the gap between the abstract concept of Spark and ready-to-use examples which can easily be altered to suite the researchers need, we provide economists and social scientists more generally with the theory and practice to handle the ever growing datasets available. The ease of reproducing the examples in this paper makes this guide a useful reference for researchers with a limited background in data handling and distributed computing.*

#### Replication files
This repository contains all codes to replicate the results of our paper. 

Link to the paper: 
 - [Journal of Data Science]()
 - [Supplementary Material](https://github.com/benjaminbluhm/econometrics_at_scale/blob/master/supplementary_material/supplementary_material.pdf)

Data download: 

| Data set        | Url                                                                          |
|-----------------|------------------------------------------------------------------------------|
| HDMA(1)           |  `https://www.dropbox.com/sh/y5vrc3fnhwvw14o/AAAkgKja5YVpTT2vSUM0dW6-a?dl=0` |
| HDMA subset     |  `https://www.dropbox.com/s/z690uga5a0qrezv/HMDA_subsample.csv?dl=0`         |    
| Simulated panel |  `https://www.dropbox.com/sh/vk2ra1ufupi0yky/AABHUX6FZxIOWdk9LMnNTy5ea?dl=0` |
| Time series     |  See Chapter 4.4 for simulation code                                         |


(1) The original data can be obtained from the [FFIEC website](https://www.consumerfinance.gov/data-research/hmda/explore).