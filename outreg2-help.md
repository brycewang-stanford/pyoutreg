[Skip to Main Content](#s-lg-guide-main)

1. [Princeton University Library](https://library.princeton.edu)
2. [Research Guides](https://libguides.princeton.edu/)
3. [Data Analysis](https://libguides.princeton.edu/data-guides)
4. [Using outreg2 to make publication-quality tables in Stata](https://libguides.princeton.edu/outreg2)
5. A Hands-on Tutorial

Search this Guide

Search

# Using outreg2 to make publication-quality tables in Stata: A Hands-on Tutorial

Using outreg2 to report regression outputs, summary statistics, and basic cross-tabulations

#### A Hands-on Tutorial

## Table of Contents

###### [1.](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36209163)[Using outreg2 for Reporting Regression Outputs in Stata](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36209163)

###### [1.1. Linear regression: producing publication-quality output tables](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36209164)

###### [1.2. Fixed effects regression: producing publication-quality output tables](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36209165)

###### [1.3. Comparing different linear models using outreg2](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36209170)

###### [1.4. Reporting logit/probit outputs using outreg2](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36284860)

###### [2. Using outreg2 for Reporting Basic Statistics in Stata](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36285107)

###### [2.1. Using outreg2 for reporting summary statistics in Stata](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36285112)

###### [2.2. Using outreg2 for reporting basic cross-tab outputs in Stata](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36285290)

###### [References / Useful Resources](https://libguides.princeton.edu/c.php?g=1322965&p=9734327#s-lg-box-wrapper-36209177)

## 1. Using outreg2 for Reporting Regression Outputs in Stata

Output tables presented in Stata result windows can be saved in Word, Text, or Excel files using the **outreg2** command. The **outreg2** command produces output tables that resemble those reported in journal articles. Before using the **outreg2**command, we need to install it first because it is a user-written command. Remember, if you install it once, you will not need to install it again. To install the command, type:

ssc install outreg2

Note: Besides the **outreg2** command, the **asdoc** command is also helpful for making publication-quality tables in Stata. This tutorial focuses on the **outreg2** command. To learn about the **asdoc** command, type **help asdoc** in the Stata command window.

## 1.1. Linear regression: producing publication-quality output tables

We will use the National Longitudinal Survey data available on the Stata website.

To load the data, type:

webuse nlswork, clear

Note that the clear option erases any loaded data in your current Stata session.

For exporting outputs from linear regression to a Word file, type

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace

We will get the following outputs in the Stata output window.

outreg2 using myreg.doc

myreg.doc
dir : seeout

If you are a Windows user, click on myreg.doc to open the file myreg.doc in Word (you can replace this name with your own).

If you are a Mac user, click on dir to go to the directory where myreg.doc is saved, and open it with Word (you can replace this name with your own).

The regression outputs in the Word file will look as follows.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outreg2.jpg)

NOTE: If you want to export the output table in Excel, use the extension \*.xls instead of using \*.doc

We can **add a new column** to an output table using the option append.

The regression in the new column adds three new variables age, race, and union

***Note:*** make sure to close the current output file myreg.doc before running new Stata codes.

Type:

reg ln\_wage grade ttl\_exp hours age race union
outreg2 using myreg.doc, append

Opening the Word file from the directory will give us the following table.![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable2.jpg)

NOTE: Follow the same instructions to add more columns to your table.

We can **name colum****ns with customized titles** by using the option ctitle

Note: make sure to close the current output file myreg.doc before running new Stata codes.

Type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace ctitle (Model 1)
reg ln\_wage grade ttl\_exp hours age race union
outreg2 using myreg.doc, append ctitle (Model 2)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable3.jpg)

We can **show variable labels instead of variable names** by using the option label

Note: make sure to close the current output file myreg.doc before running new Stata codes.

Type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace ctitle (Model 1) label
reg ln\_wage grade ttl\_exp hours age race union
outreg2 using myreg.doc, append ctitle (Model 2) label

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable4.jpg)

We can **adjust decimal places of the coefficients and standard errors** by using the option dec()

Note: make sure to close the current output file myreg.doc before running new Stata codes.

Type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace ctitle (Model 1) label dec(2)
reg ln\_wage grade ttl\_exp hours age race union
outreg2 using myreg.doc, append ctitle (Model 2) label dec(2)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable5.jpg)

We can assign different decimal places for coefficients and standard errors by using the options bdec() and  sdec()

Note: make sure to close the current output file myreg.doc before running new Stata codes.

Type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace ctitle (Model 1) label bdec(3) sdec (4)
reg ln\_wage grade ttl\_exp hours age race union
outreg2 using myreg.doc, append ctitle (Model 2) label bdec(3) sdec (4)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable6.jpg)

We can **add notes to the output table** by using the option addnote()

Note: make sure to close the current output file myreg.doc before running new Stata codes.

Type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace ctitle (Model 1) label bdec(3) sdec (4)addnote (Notes: real income is the dependent variable in both Model 1 and Model 2.)
reg ln\_wage grade ttl\_exp hours age race union
outreg2 using myreg.doc, append ctitle (Model 2) label bdec(3) sdec (4)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable7.jpg)

If you **do not want to include any note** under your table (including the default notes), use the option nonotes

Type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace ctitle (Model 1) label bdec(3) sdec (4) nonotes

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable8.jpg)

We can **add a title in the output table** by using the option title()

Note: make sure to close the current output file myreg.doc before running new Stata codes.

Type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace ctitle (Model 1) label dec(3) title (Table 1: Determinants of Income)
reg ln\_wage grade ttl\_exp hours age race union
outreg2 using myreg.doc, append ctitle (Model 2) label dec(3)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable9.jpg)

We can **add additional statistics** (e.g., F-stat, p-value of F, etc.) to an output table by using the option addstat()

Note: make sure to close the current output file myreg.doc before running new Stata codes.

Type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace ctitle (Model 1) label dec(3) addstat("F-Stat",e(F),"Prob > F",e(p))
reg ln\_wage grade ttl\_exp hours age race union
outreg2 using myreg.doc, append ctitle (Model 2) label dec(3) addstat("F-Stat",e(F),"Prob > F",e(p))

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable10.jpg)

If you run your regression with a large number of variables and want to **keep only a few variables** in the output table, use the option keep() or drop()

If using the keep option, type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace keep (grade)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable11.jpg)

If using the drop option, type:

reg ln\_wage grade ttl\_exp hours
outreg2 using myreg.doc, replace drop (ttl\_exp hours)

Opening the Word file from the directory will give us the same table as above.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable11.jpg)

## 1.2. Fixed effects regression: producing publication-quality output tables

To load the data, type:

use https://www.stata.com/data/jwooldridge/eacsap/wagepan.dta, clear

Note that the clear option erases any loaded data in your current Stata session. \* The dataset (wagepan.dta) is used in Woolridge (2010), which is available [here](https://www.stata.com/texts/eacsap/).

To declare the dataset as panel, type:

xtset nr year

For exporting outputs from a fixed effect model to a Word file, type:

xtreg lwage hours exper expersq married manuf, fe
outreg2 using myreg.doc, replace ctitle(Fixed Effects) addtext(Individual FE, YES) dec(4)

We will get the following outputs in the Stata output window.

. outreg2 using myreg.doc, replace ctitle(Fixed Effects) addtext(Individual FE, YES) dec(4)
myreg.doc
dir : seeout

If you are a Windows user, click on myreg.doc to open the file myreg.doc in Word (you can replace this name with your own).

If you are a Mac user, click on dir to go to the directory where myreg.doc is saved, and open it with Word (you can replace this name with your own).

The regression outputs in the Word file will look as follows.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable12.jpg)

In fixed effects models, you do not have to add the FE coefficients. You can just add a note indicating that the model includes fixed effects. This can be added from outreg2;see the option addtex() above.

NOTE: If you want to export the output table in Excel, use the extension \*.xls instead of using \*.doc

To **add time fixed effects** to the fixed effect model above, type:

outreg2 using myreg.doc, replace ctitle(Fixed Effects) addtext(Individual FE, YES, Year FE, YES) dec(4)

***Note:*** make sure to close the current output file myreg.doc before running new Stata codes.

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable13.jpg)

## 1.3. Comparing different linear models using outreg2

To load the data. Type:

use https://www.stata.com/data/jwooldridge/eacsap/wagepan.dta, clear

In this example, we will estimate three different models: OLS, Random Effects, and Fixed Effects. To export the outputs in a Word file, type:

xtset nr year
reg lwage hours exper expersq married manuf
outreg2 using myreg.doc, replace ctitle (OLS) dec(4)
xtreg lwage hours exper expersq married manuf, re
outreg2 using myreg.doc, append ctitle(Random Effects) dec(4)
xtreg lwage hours exper expersq married manuf, fe
outreg2 using myreg.doc, append ctitle(Fixed Effects) addtext(Individual FE, YES, Year FE, YES) dec(4)

We will get the following outputs in the Stata output window.

. outreg2 using myreg.doc, append ctitle(Fixed Effects) addtext(Individual FE, YES, Year FE, YES) dec(4)

myreg.doc
dir : seeout

If you are a Windows user, click on myreg.doc to open the file myreg.doc in Word (you can replace this name with your own).

If you are a Mac user, click on dir to go to the directory where myreg.doc is saved, and open it with Word (you can replace this name with your own).

The regression outputs in the Word file will look as follows.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable14.jpg)

NOTE: If you want to export the output table in Excel, use the extension \*.xls instead of using \*.doc

## 1.4. Reporting logit/probit outputs using outreg2

We can use outreg2 for reporting almost any regression output (linear or no linear). For logit models with odds ratios, we need to add the option eform

For exporting outputs from the logit model to a Word file, type:
use "https://dss.princeton.edu/training/logit.dta", clear
logit y\_bin x1 x2 x3 i.opinion
outreg2 using mylogit.doc, replace ctitle(Logit Coefficients)
logit y\_bin x1 x2 x3 i.opinion, or
outreg2 using mylogit.doc, append ctitle(Odds Ratio) eform

We will get the following outputs in the Stata output window.

. outreg2 using mylogit.doc, append ctitle(Odds Ratio) eform
mylogit.doc
dir : seeout

If you are a Windows user, click on mylogit.doc to open the file myreg.doc in Word (you can replace this name with your own).

If you are a Mac user, click on dir to go to the directory where mylogit.doc is saved, and open it with Word (you can replace this name with your own).

The regression outputs in the Word file will look as follows.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable15.jpg)

NOTE: If you want to export the output table in Excel, use the extension \*.xls instead of using \*.doc

We can **publish outputs from marginal effects after logit** in a Word document by using the outreg2 command. To do this, type:

use "https://dss.princeton.edu/training/logit.dta", clear
quietly logit y\_bin x1 x2 x3 i.opinion
margins, dydx(\*) atmeans post
outreg2 using marginal.doc, word replace ctitle(Marginal Effects)

Stata will give us the following outputs

. outreg2 using marginal.doc, word replace ctitle(Marginal Effects)
marginal.doc
dir : seeout

- Windows users: click on marginal.doc to open the file in Word (you can replace this name with your own).

- Mac users: click on dir to go to the directory where marginal.doc is saved, and open it with Word (you can replace this name with your own)

The outputs in the Word document look as follows.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/outregtable16.jpg)

## 2. Using outreg2 for Reporting Basic Statistics in Stata

We can save basic summary statistics, frequency, and cross-tab outputs in Word, Text, or Excel files using the **outreg2** command. Before using the **outreg2**command, we need to install it first because it is a user-written command. Remember, if you install it once, you will not need to install it again. To install the command, type:

ssc install outreg2

## 2.1. Using outreg2 for reporting summary statistics in Stata

We will use the National Longitudinal Survey data available on the Stata website.

To load the data, type:

webuse nlswork, clear

Note that the clear option erases any loaded data in your current Stata session.

For exporting **summary statistics of all variables** to a Word file, type:

outreg2 using sumstat.doc, replace sum(log)

We will get the following outputs in the Stata output window.

sumstat.doc
dir : seeout

If you are a Windows user, click on sumstat.doc to open the file myreg.doc in Word (you can replace this name with your own).

If you are a Mac user, click on dir to go to the directory where sumstat.doc is saved, and open it with Word (you can replace this name with your own).

The summary stat outputs in the Word file will look as follows.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/sumstat1.jpg)

NOTE: If you want to export the output table in Excel, use the extension \*.xls instead of using \*.doc

For exporting **summary statistics of selected variables** to a Word file, type:

outreg2 using sumstat.doc, replace sum(log)keep (year age race grade union tenure ln\_wage)

Opening the Word file from the directory will give us the following table.![](https://libapps.s3.amazonaws.com/accounts/328678/images/sumstat2.jpg)

For exporting **selected statistics of selected variables** to a Word file, type:

outreg2 using sumstat.doc, replace sum(log)keep (year age race grade union tenure ln\_wage) eqkeep (N mean sd)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/sumstat3.jpg)

For exporting **detail statistics of selected variables** to a Word file, type:

set more off
outreg2 using sumstat.doc, replace sum(detail) keep (year age race grade union tenure ln\_wage)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/sumstat4.jpg)

NOTE: The option "sum(detail)" exports all the summary statistics shown above for the *selected variables* to the Word file. However, the command reports detailed summary statistics of *all the variables* in the dataset in the Stata output window. This is similar to typing "summarize, detail".

For exporting **selected detail statistics of selected variables** to a Word file, type:

set more off
outreg2 using sumstat.doc, replace sum(detail) keep (year age race grade union tenure ln\_wage) eqkeep (N mean sd skewness p50 p75 p99)

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/sumstat5.jpg)

For exporting **detail statistics *by group* for selected variables**, type:

set more off
bysort race: outreg2 using sumstat.doc, replace sum(log) keep (age union grade tenure ln\_wage)

NOTE: You need to specify either keeping statistics (eqkeep) and droping variables (drop) or viceversa. You can't specify eqkeep() and keep() at the same time.

Opening the Word file from the directory will give us the following table.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/sumstat6.jpg)

## 2.2. Using outreg2 for reporting basic cross-tab outputs in Stata

We will use the National Longitudinal Survey data available on the Stata website.

To load the data, type:

webuse nlswork, clear

Note that the clear option erases any loaded data in your current Stata session.

For exporting **cross-tab outputs** of two categorical variables race and collgrad to a Word file, type:

outreg2 race collgrad using ctab.doc, replace cross noaster

We will get the following outputs in the Stata output window.

. outreg2 race collgrad using ctab.doc, replace cross noaster
ctab.doc
dir : seeout

If you are a Windows user, click on ctab.doc to open the file myreg.doc in Word (you can replace this name with your own).

If you are a Mac user, click on dir to go to the directory where ctab.doc is saved, and open it with Word (you can replace this name with your own).

The cross-tab outputs in the Word file will look as follows.

![](https://libapps.s3.amazonaws.com/accounts/328678/images/ctab1.jpg)

Note: Percents in the parenthesis represent column percent.

NOTE: For reporting more varieties of cross-tab outputs, use asdoc command in Stata. Type help asdoc in Stata.

## References / Useful Resources

DSS Data Analysis Guides. Available at <https://libguides.princeton.edu/c.php?g=1415215>

Publication Style Regression Output in Stata - Part 1. The Data Hall. Available at <https://thedatahall.com/stata-outreg2-part1/>

Publication Style Regression Output in Stata - Part 1. The Data Hall. Available at <https://thedatahall.com/reporting-publication-style-regression-output-in-stata-part-2/>

Wooldridge, J. M. (2010). *Econometric analysis of cross section and panel data*. MIT Press.

## Data Consultant

[![Profile Photo](//d2jv02qf7xgjwx.cloudfront.net/accounts/328678/profiles/335053/dss1026_1.JPG)

Muhammad Al Amin](//libguides.princeton.edu/prf.php?id=621d7ed8-7cdb-11ed-9922-0ad758b798c3)

He/Him/His

Email Me

**Contact:**

Firestone Library, A-12-F.1

609-258-6051

## Data Consultant

[![Profile Photo](//d2jv02qf7xgjwx.cloudfront.net/accounts/308946/profiles/314096/thumbnail_38231665498751_.pic__1_.jpg)

Yufei Qin](//libguides.princeton.edu/prf.php?id=61080a78-7cdb-11ed-9922-0ad758b798c3)

Email Me

**Contact:**

Firestone Library, A.12F.2

6092582519

## Comments or Questions?

If you have questions or comments about this guide or method, please email data@Princeton.edu.

* Last Updated: Aug 14, 2024 6:20 PM
* URL: https://libguides.princeton.edu/outreg2
* Print Page

[Login to LibApps](https://princeton.libapps.com/libapps/login.php?site_id=77&target64=L2xpYmd1aWRlcy9hZG1pbl9jLnBocD9nPTEzMjI5NjUmcD05NzM0MzI3)

Subjects: [Data & Statistical Services](https://libguides.princeton.edu/sb.php?subject_id=213440)

Tags: [outreg2](https://libguides.princeton.edu/srch.php?tag=outreg2&default_lg=1), [stata](https://libguides.princeton.edu/srch.php?tag=stata&default_lg=1)

Report a problem.
