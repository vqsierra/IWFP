
// SENSITIVITY ANALYSIS #1 - School-Level Clustering Adjustment
// Predicting Suicidal Ideation in Native American High Schoolers (CHKS Dataset)
// Author: Valentín Quiroz Sierra, PhD, MSW
// Last updated: March 2025
// Description: This script prepares variables and runs a LASSO logistic regression model with 10-fold cross-validation,
// adjusting for clustering at the school level to assess the robustness of the primary model.



// Restrict to Native American youth
keep if a7 == 1

// ---------------------------
// Outcome Variable
// ---------------------------
gen si = .
replace si = a131_a119
recode si (1 = 0) (2 = 1)
drop if missing(si)

// ---------------------------
// Predictor Variables
// ---------------------------

// -- Individual Level --
gen gender = .
replace gender = a4
recode gender (1 = 0) (2 = 1)
drop if missing(gender)

gen trans = .
replace trans = a5
recode trans (1 = 0) (2 = 1) (3 = 1) (4 = 0)
drop if missing(trans)

gen lgbt = .
replace lgbt = a18
recode lgbt (1 = 0) (2/6 = 1)
drop if missing(lgbt)

gen grade2 = .
replace grade2 = grade
recode grade2 (7 8 13 = .) (9 = 1) (10 = 2) (11 = 3) (12 = 4)
drop if missing(grade2)

gen academic = .
replace academic = a20
recode academic (1 = 7)(2 = 6)(3 = 5)(4 = 4)(5 = 3)(6 = 2)(7 = 1)(8 = 0)
egen zacademic = std(academic)
drop if missing(zacademic)

gen lifealc = .
replace lifealc = a51_a52
recode lifealc (1=0) (2=1) (3=2) (4=3) (5=4) (6=5)
egen zlifealc = std(lifealc)
drop if missing(zlifealc)

gen lifecig = .
replace lifecig = a48_a49
recode lifecig (1=0) (2=1) (3=2) (4=3) (5=4) (6=5)
egen zlifecig = std(lifecig)
drop if missing(zlifecig)

gen lifevape = .
replace lifevape = a50_a51
recode lifevape (1=0) (2=1) (3=2) (4=3) (5=4) (6=5)
egen zlifevape = std(lifevape)
drop if missing(zlifevape)

gen lifecan = .
replace lifecan = a52_a53
recode lifecan (1=0) (2=1) (3=2) (4=3) (5=4) (6=5)
egen zlifecan = std(lifecan)
drop if missing(zlifecan)

// Lifetime Drug Use (mean of 11 indicators)
foreach var in a53_a54 a54 a55 a56 a57 a58 a59 a60 a61 a62 a63_a56 {
    recode `var' (1=0) (2=1) (3=2) (4=3) (5=4) (6=5)
}
gen lifedrug = (a53_a54 + a54 + a55 + a56 + a57 + a58 + a59 + a60 + a61 + a62 + a63_a56) / 11
egen zlifedrug = std(lifedrug)
drop if missing(zlifedrug)

// -- Emotional/Social --
gen foster = .
replace foster = a9
recode foster (5 = 1) (1/4 6/8 = 0)
drop if missing(foster)

gen parented = .
replace parented = a10
recode parented (1 = 0)(2 = 1)(3 = 2)(4 = 3)(5 = .)
egen zparented = std(parented)
drop if missing(zparented)

// Drug Education (reverse coded average)
local orig_vars a87_a78 a88_a79 a89_a80 a90_a81 a91_a82 a92_a83 a93_a84 a94_a85
local rev_vars  rev_a87_a78 rev_a88_a79 rev_a89_a80 rev_a90_a81 ///
                rev_a91_a82 rev_a92_a83 rev_a93_a84 rev_a94_a85

forvalues i = 1/8 {
    local orig : word `i' of `orig_vars'
    local rev : word `i' of `rev_vars'
    
    gen `rev' = `orig'
    recode `rev' (1=3) (2=2) (3=1) (4=0)
}

gen druged = (rev_a87_a78 + rev_a88_a79 + rev_a89_a80 + rev_a90_a81 + ///
              rev_a91_a82 + rev_a92_a83 + rev_a93_a84 + rev_a94_a85) / 8
egen zdruged = std(druged)
drop if missing(zdruged)

// Drug Access
foreach var in a95_a86 a96_a87 a97_a88 a98_a89 {
    recode `var' (1=0) (2=1) (3=2) (4=3) (5=.)
}
gen drugaccess = (a95_a86 + a96_a87 + a97_a88 + a98_a89) / 4
egen zdrugaccess = std(drugaccess)
drop if missing(zdrugaccess)

// Bullying (average of 24 indicators)
foreach var in a106_a94 a107_a95 a108_a96 a109_a97 a110_a98 a111_a99 ///
               a112_a100 a113_a101 a114_a102 a115_a103 a116_a104 a117_a105 ///
               a118_a106 a119_a107 a120_a108 a121_a109 a122_a110 a123_a111 ///
               a124_a112 a125_a113 a126_a114 a127_a115 a128_a116 {
    recode `var' (1=0) (2=1) (3=2) (4=3)
}
gen bully = (a106_a94 + a107_a95 + a108_a96 + a109_a97 + a110_a98 + a111_a99 + ///
             a112_a100 + a113_a101 + a114_a102 + a115_a103 + a116_a104 + a117_a105 + ///
             a118_a106 + a119_a107 + a120_a108 + a121_a109 + a122_a110 + a123_a111 + ///
             a124_a112 + a125_a113 + a126_a114 + a127_a115 + a128_a116) / 24
egen zbully = std(bully)
drop if missing(zbully)

// -- Mental/Political --
gen depression = .
replace depression = a130_a118
recode depression (1 = 0)(2 = 1)
drop if missing(depression)

// -- Physical/Economic --
gen homeless = .
replace homeless = a9
recode homeless (6/8 = 1)(1/5 = 0)
drop if missing(homeless)

gen breakfast = .
replace breakfast = a132_a120
recode breakfast (1 = 0)(2 = 1)
drop if missing(breakfast)

// ---------------------------
// Model: LASSO Logistic Regression
// ---------------------------
lasso logit si i.gender i.trans i.lgbt i.foster i.depression i.homeless i.breakfast ///
    zparented zacademic zlifealc zlifecig zlifevape zlifecan zlifedrug ///
    zdruged zdrugaccess zbully, ///
    selection(cv) rseed(1533) folds(10) cluster(schlno)

estimates store si_cluster
lassocoef si_estimates, display(coef, standardized) sort(coef, standardized)

// ---------------------------
// Predictions & Performance
// ---------------------------
predict double si_clusterPR3, pr
calibrationbelt si si_clusterPR3, devel("internal") cLevel1(0.95) cLevel2(0.99) maxDeg(4) thres(0.95)
cvauroc si si_clusterPR3, kfold(10) seed(1533) fit detail graphlowess
brier si si_clusterPR3
sum si_clusterPR3, detail
