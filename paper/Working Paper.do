keep if a7 == 1

********************************
* Binary Response Variable *
********************************

*** Suicide-Related Behavior ***
gen srb=.
replace srb= a131_a119
recode srb (1=0) (2=1)


********************************
**** Explanatory Variables *****
********************************
*(All Continuous)*

*** Alcohol & Other Drugs ***
gen rev_a87_a78=.
replace rev_a87_a78= a87_a78
recode rev_a87_a78 (1=4) (2=3) (3=2) (4=1) 
tab rev_a87_a78
tab a87_a78

gen rev_a88_a79=.
replace rev_a88_a79= a88_a79
recode rev_a88_a79 (1=4) (2=3) (3=2) (4=1)  
tab rev_a88_a79
tab a88_a79

gen rev_a89_a80=.
replace rev_a89_a80= a89_a80
recode rev_a89_a80 (1=4) (2=3) (3=2) (4=1)  
tab rev_a89_a80
tab a89_a80

gen rev_a90_a81=.
replace rev_a90_a81= a90_a81
recode rev_a90_a81 (1=4) (2=3) (3=2) (4=1)  
tab rev_a90_a81
tab a90_a81

gen rev_a91_a82=.
replace rev_a91_a82= a91_a82
recode rev_a91_a82 (1=4) (2=3) (3=2) (4=1)  
tab rev_a91_a82
tab a91_a82

gen rev_a92_a83=.
replace rev_a92_a83= a92_a83
recode rev_a92_a83 (1=4) (2=3) (3=2) (4=1)  
tab rev_a92_a83
tab a92_a83

gen rev_a93_a84=.
replace rev_a93_a84= a93_a84
recode rev_a93_a84 (1=4) (2=3) (3=2) (4=1)  
tab rev_a93_a84
tab a93_a84

gen rev_a94_a85=.
replace rev_a94_a85= a94_a85
recode rev_a94_a85 (1=4) (2=3) (3=2) (4=1)  
tab rev_a94_a85
tab a94_a85

gen rev_a103_a90=.
replace rev_a103_a90= a103_a90
recode rev_a103_a90 (1=2) (2=3) (3=1)  
tab rev_a103_a90
tab a103_a90

gen aod=.
replace aod= (a22i + a48_a49 + a49_a50 + a50_a51 + a51_a52 + a52_a53 + a53_a54 + a54 + a55 + a56 + a57 + a58 + a59 + a60 + a61 + a62 + a63_a56 + a64_a57 + a65_a58 + a66_a59 + a67_a60 + a68_a61 + a69_a62 + a70_a63 + a71_a64 + a72_a65 + a73_a66 + a74_a67 + a75_a68 + a76_a69 + a77 + a78_a70 + a79 + a80_a71 + a81_a72 + a82_a73 + a83_a74 + a84_a75 + a85_a76 + a86_a77 + rev_a87_a78 + rev_a88_a79 + rev_a89_a80 + rev_a90_a81 + rev_a91_a82 + rev_a92_a83 + rev_a93_a84 + rev_a94_a85 + a95_a86 + a96_a87 + a97_a88 + a98_a89 + a99 + a100 + a101 + a102 + rev_a103_a90)/57
summarize aod, detail
hist aod, norm
drop if aod ==.

*** Bullying & Harrasment ***
gen bully=.
replace bully= (a22c + a22f + a105_a92 + a106_a94 + a107_a95 + a108_a96 + a109_a97 + a110_a98 + a111_a99 + a112_a100 + a113_a101 + a114_a102 + a115_a103 + a116_a104 + a117_a105 + a118_a106 + a119_a107 + a120_a108 + a121_a109 + a122_a110 + a123_a111 + a124_a112 + a125_a113 + a126_a114 + a127_a115 + a128_a116)/26
summarize bully, detail
hist bully, norm
drop if bully ==.

*** Hopelessness ***
gen hplsnes=.
replace hplsnes= (a22d + a130_a118)/2
summarize hplsnes, detail
hist hplsnes, norm
drop if hplsnes ==.

*** Standardize Predictor Variables ***
egen zaod= std(aod)
summarize zaod, detail
hist zaod, norm

egen zbully= std(bully)
summarize zbully, detail
hist zbully, norm

egen zhplsns= std(hplsnes)
summarize zhplsns, detail
hist zhplsns, norm



********************************
****** Data Cleaning ******
********************************
keep srb zaod zbully zhplsns


********************************
** Descriptive Statistics ***
********************************
tab srb
sum zhplsns
sum zaod
sum zbully






********************************
****** Research Questions ******
********************************
*1 - Is there an association between the degree of hopelessness and the presence 
*	of suicidal ideation among Native American students in California?
	
*2 - Is there an association between the degree of substance use and the presence 
*	of suicidal ideation among Native American students in California?
	
*3 - Is there an association between the frequency of experiences of bullying 
*	and harrassment and the presence of suicidal ideation among Native 
*	American students in California?


	
****** Logistic Regression Analysis ******
logit srb zhplsns, or

logit srb zaod, or

logit srb zbully, or

*


