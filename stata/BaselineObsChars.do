* Melanie Wallskog
* 8/21/17

* This do-file performs a balancing test for pals and non-pals in 1914, 
* i.e. a baseline measure of how comparable the groups are

clear 

cd "/home/jonasmg/Prog/scrapinghistory"


use "STATAOUTPUT/FirstSample_ALLhisclass.dta"

merge m:1 regiment using "data/SCBattTypes.dta", gen(batt_type_merge)

drop if batt_type_merge==2

save "STATAOUTPUT/FirstSample_Pals.dta", replace

* Compare Pals==1 to Pals==0 group

drop if contains_pals==1 | nolocal_pals==1
drop if hisclass_1914<0

gen feet_temp = substr(height,1,1)
gen inch_temp = substr(height,5,1)
replace inch_temp = substr(height,5,2) if substr(height,6,1)!="i"
replace inch_temp = substr(height,5,3) if substr(height,6,1)=="."
replace feet_temp = "." if feet_temp==""
replace inch_temp = "." if inch_temp==""
* fix
destring(feet_temp inch_temp),replace

gen height_float = .

local chars ageyears birthyear attestationyear weight chestsize hisclass_1914

foreach x of local chars{
	reg `x' pals
}

reg hisclass_1914 pals ageyears weight chestsize 

log close


* Compare difference

drop if hisclass_1939<0

gen class_change = hisclass_1939 - hisclass_1914 
* note: lower number is higher class, so if this is a positive number, the person fell in social class

reg class_change pals
reg class_change pals ageyears weight chestsize
