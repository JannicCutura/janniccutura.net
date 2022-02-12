---
title: Stata's reghdfe in R
subtitle: How to mimic Stata's regdhfe regressions in R


# Summary for listings and search engines
summary: In this post I show how you can get Stata quality regression results in R including popular regression features in economics such as high dimesional fixed effects, instrumental variables and standard error clustering.
# Link this post with a project
projects: []

# Date published
date: "2022-01-13T00:00:00Z"

# Date updated
lastmod: "2022-01-13T00:00:00Z"

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: false


links:
 - icon: github
   icon_pack: fab
   name: Github
   url: https://github.com/JannicCutura/reghdfe-in-r

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  caption: 'Image credit: [**Authors graph**](https://github.com/JannicCutura/reghdfe-in-r)'
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin


tags:
- Academic

#categories:
#- Demo
#- 教程
---

If you are like me, you love Stata's `reghdfe` command for linear regression.
It offers a wide range of functionality desired in (financial) economics research, like multi dimensional fixed effects, instrumental variables and standard error clustering.
Yet, for some modern data pipelines (in particular on distributed systems), it is not trivial to integrate Stata. 
R on the other hand has a lot of APIs that are useful in such a context (for example sparklyr package to write spark applications). 
In this post I am showing how you can use R's linear fixed effects `lfe` packge and its `felm` command to replicate regression results
from Stata's `reghdfe`. If you are reading this post, chances are you are familiar with Stata's `reghdfe`, so I won't spend much time explaining what the below Stata code does.
In a nutshell we have seven regression models here, that we are trying to replicate in R next:

	cls
	webuse nlswork, clear
	xtset idcode year
	gen cons = 1

	* model 1
	reg ln_w grade age ttl_exp tenure not_smsa south

	* model 2
	reghdfe ln_w grade age ttl_exp tenure not_smsa south, abs(idcode) 

	* model 3
	reghdfe ln_w grade age ttl_exp tenure not_smsa south, abs(idcode)  cluster(idcode)

	* model 4
	reghdfe ln_w grade age ttl_exp tenure not_smsa south, abs(year)  cluster(idcode)
	xtreg ln_w grade age ttl_exp tenure not_smsa south i.year, re cluster(idcode)

	* model 5
	reghdfe ln_w  age ttl_exp tenure not_smsa south, abs(idcode year)  cluster(idcode)

	* model 6
	reghdfe ln_w  age ttl_exp tenure not_smsa south, abs(idcode year)  cluster(idcode year)

	* model 7
	reghdfe ln_w grade age ttl_exp tenure not_smsa south, abs(idcode year)  cluster(idcode wks_work)

I only print the results of the last model 7: 


	HDFE Linear regression                            Number of obs   =     26,834
	Absorbing 2 HDFE groups                           F(   5,    104) =     107.26
	Statistics robust to heteroskedasticity           Prob > F        =     0.0000
													  R-squared       =     0.6797
													  Adj R-squared   =     0.6215
	Number of clusters (idcode)  =      4,107         Within R-sq.    =     0.0539
	Number of clusters (wks_work) =        105        Root MSE        =     0.2922

	  (Std. Err. adjusted for 105 clusters in idcode wks_work)
	------------------------------------------------------------------------------
			 |               Robust
		 ln_wage |      Coef.   Std. Err.      t    P>|t|     [95% Conf. Interval]
	-------------+----------------------------------------------------------------
		   grade |          0  (omitted)
		     age |   .0122875    .011843     1.04   0.302    -.0111976    .0357725
		 ttl_exp |   .0329553   .0026807    12.29   0.000     .0276395    .0382712
		  tenure |   .0101173    .002155     4.69   0.000     .0058438    .0143907
		not_smsa |  -.0953025   .0139339    -6.84   0.000     -.122934   -.0676711
		   south |  -.0652122   .0168939    -3.86   0.000    -.0987133    -.031711
		   _cons |   1.137644   .3446994     3.30   0.001     .4540922    1.821196
	------------------------------------------------------------------------------

	Absorbed degrees of freedom:
	-----------------------------------------------------+
	 Absorbed FE | Categories  - Redundant  = Num. Coefs |
	-------------+---------------------------------------|
	      idcode |      4107        4107           0    *|
		year |        15           0          15     |
	-----------------------------------------------------+
	* = FE nested within cluster; treated as redundant for DoF computation

In this model we have two dimensional fixed effects (`idcode` and `year`) and two-way standard error clustering (`idcode` and `wks_work`). 

First, prepare the workspace in R:

	# clear work space
	rm(list=ls()) # delete global environment
	library(foreign)   
	library(readstata13)
	library(lfe)

	# get sample data
	df = read.dta13("http://www.stata-press.com/data/r14/nlswork.dta")


We can recreate the regression results from `reghdfe` using:


	model7 = felm(
		  # define regression model
		  ln_wage ~  age + ttl_exp + tenure+  not_smsa  + south
		  # define fixed effects | instruments | standard errors
		  | idcode + year | 0 | idcode + wks_work, 
		  # the data
		  data = df,
		  # the method to compute SE
		  cmethod = 'cgm2',
		  # whether degree of freedom should be computed exactly
		  exactDOF=TRUE
		  )
	
	summary(model7)

Note that you need the latest version of `lfe` in order to be able to use the `cgm2` method. Otherwise standard errors will be different from Stata.


	Call:
	   felm(formula = ln_wage ~ age + ttl_exp + tenure + not_smsa +      south | idcode + year | 0 | idcode + wks_work, data = df,      exactDOF = TRUE, cmethod = "cgm2") 

	Residuals:
		 Min       1Q   Median       3Q      Max 
	-1.91479 -0.11707  0.00583  0.12838  2.96827 

	Coefficients:
		  Estimate     Cluster s.e.   t value       Pr(>|t|)    
	age       0.012287     0.011840       1.038     0.301767    
	ttl_exp   0.032955     0.002680      12.297      < 2e-16 ***
	tenure    0.010117     0.002154       4.696     8.13e-06 ***
	not_smsa -0.095303     0.013930      -6.841     5.57e-10 ***
	south    -0.065212     0.016889      -3.861     0.000196 ***
	---
	Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

	Residual standard error: 0.2921 on 22708 degrees of freedom
	  (1133 observations deleted due to missingness)
	Multiple R-squared(full model): 0.689   Adjusted R-squared: 0.6248 
	Multiple R-squared(proj model): 0.05386   Adjusted R-squared: -0.1416 
	F-statistic(full model, *iid*):10.72 on 4692 and 22708 DF, p-value: < 2.2e-16 
	F-statistic(proj model): 107.3 on 5 and 104 DF, p-value: < 2.2e-16 



In the [repo](https://github.com/JannicCutura/reghdfe-in-r) I stored the codes for model 1-6.
The results are practically dentical (see the [github issue](https://github.com/sgaure/lfe/issues/1#issuecomment-530561314) page on remaining differences).
At least they are close enough to win the [star wars](https://ftp.iza.org/dp7268.pdf) ;) 