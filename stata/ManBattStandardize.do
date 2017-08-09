* This do-file standardizes the battalion names in the Manchester battalions.

* Key for abbreviations:
*    SB    Service Battalion
*    RB    Reserve Battalion
*    GaB   Garrison Battalion
*    GrB   Graduated Battalion
*    YB	   Young Soldier Battalion
*    PB	   Provisional Battalion
*    HS    Home Service
*    TB    Training Battalion
*    CoOnly Company only (not enough information)
*    Dep   Depot
*    Bty   Battery
*    SpR   Special Reserve
*    ArR   Army Reserve
*    SiB   Siege Battery
*    Hos   Hospital
*    ROnly Reserve Only
*    Brig  Brigade
*    FiB   Filed Battery
*    OC    Officers Commanding Battalion
*    Pio   Pioneer (not 24th, Pals)
*    MCB   Military Cross Battalion
*    NM	   Not Manchester
*    CaB    Cavalry Battalion

clear 

cd "/home/jonasmg/Prog/scrapinghistory"

import delimited /Data/

ManBattListTyped.csv

* unclear what this is
drop v5

* Variables that Jonas had previously imputed
rename type type_jmg
rename reserve reserve_jmg

* rename for ease later
gen x = unitbattalion

* Determine Reserve Battalions - these will be excluded
gen reserve = (strpos(x,"Reserve") > 0 | strpos(x,"reserve"))
* in some cases, we want to consider the later battalions that a solider served in
replace reserve = .5 if strpos(x,",") > 0 & (strpos(x,"Reserve") > 0 | strpos(unitbattalion,"reserve"))

* Standardize Battalion number

* Method 1: First listed battalion
gen batt1 = ""

* SERVICE BATTALIONS
* no follow
forval i=1/9{
	replace batt1 = "`i' SB" if (substr(x,1,2) == "`i'," ///
			| substr(x,1,3) == "`i' ," ///
			| substr(x,1,3) == "`i' B" ///
			| substr(x,1,2) == "`i'B" ///
			| substr(x,1,4) == "`i' (S" ///
			| substr(x,1,4) == "`i' (s" ///
			| substr(x,1,3) == "`i' S" ///
		    | substr(x,1,4) == "`i' s" )
}
forval i=10/99{
	replace batt1 = "`i' SB" if (substr(x,1,3) == "`i'," ///
			| substr(x,1,4) == "`i' ," ///
			| substr(x,1,4) == "`i' B" ///
			| substr(x,1,3) == "`i'B" ///
			| substr(x,1,5) == "`i' (S" ///
			| substr(x,1,5) == "`i' (s" ///
			| substr(x,1,4) == "`i' S" ///
		    | substr(x,1,5) == "`i' s" )
}
* "st"s 
replace batt1 = "1 SB" if (substr(x,1,4) == "1st," ///
			| substr(x,1,5) == "1st ," ///
			| substr(x,1,5) == "1st B" ///
			| substr(x,1,4) == "1stB" ///
			| substr(x,1,6) == "1st (S" ///
			| substr(x,1,6) == "1st (s" ///
			| substr(x,1,5) == "1st S" ///
		    | substr(x,1,5) == "1st s" )
forval i = 2/9{
	replace batt1 = "`i'1 SB" if (substr(x,1,5)=="`i'1st," ///
			| substr(x,1,6) == "`i'1st ," ///
			| substr(x,1,6) == "`i'1st B" ///
			| substr(x,1,5) == "`i'1stB" ///
		    | substr(x,1,7) == "`i'1st (S" ///
			| substr(x,1,7) == "`i'1st (s" ///
			| substr(x,1,6) == "`i'1st S" ///
		    | substr(x,1,6) == "`i'1st s" )
}
* "nd"s
replace batt1 = "2 SB" if (substr(x,1,4) == "2nd," ///
			| substr(x,1,5) == "2nd ," ///
			| substr(x,1,5) == "2nd B" ///
			| substr(x,1,4) == "2ndB" ///
		    | substr(x,1,6) == "2nd (S" ///
			| substr(x,1,6) == "2nd (s" ///
			| substr(x,1,5) == "2nd S" ///
		    | substr(x,1,5) == "2nd s" )
forval i = 2/9{
	replace batt1 = "`i'2 SB" if (substr(x,1,5)=="`i'2nd," ///
			| substr(x,1,6) == "`i'2nd ," ///
			| substr(x,1,6) == "`i'2nd B" ///
			| substr(x,1,5) == "`i'2ndB" ///
			| substr(x,1,7) == "`i'2nd (S" ///
			| substr(x,1,7) == "`i'2nd (s" ///
			| substr(x,1,6) == "`i'2nd S" ///
		    | substr(x,1,6) == "`i'2nd s" )
}
* "rd"s
replace batt1 = "3 SB" if (substr(x,1,4) == "3rd," ///
			| substr(x,1,5) == "3rd ," ///
			| substr(x,1,5) == "3rd B" ///
			| substr(x,1,4) == "3rdB" ///
			| substr(x,1,6) == "3rd (S" ///
			| substr(x,1,6) == "3rd (s" ///
			| substr(x,1,5) == "3rd S" ///
		    | substr(x,1,5) == "3rd s" )
forval i = 2/9{
	replace batt1 = "`i'3 SB" if (substr(x,1,5)=="`i'3rd," ///
			| substr(x,1,6) == "`i'3rd ," ///
			| substr(x,1,6) == "`i'3rd B" ///
			| substr(x,1,5) == "`i'3rdB" ///
			| substr(x,1,7) == "`i'3rd (S" ///
			| substr(x,1,7) == "`i'3rd (s" ///
			| substr(x,1,6) == "`i'3rd S" ///
		    | substr(x,1,6) == "`i'3rd s" )
}
* "th"s
forval i = 4/9{
	replace batt1 =  "`i' SB" if (substr(x,1,4)=="`i'th," ///
			| substr(x,1,5) == "`i'th ," ///
			| substr(x,1,5) == "`i'th B" ///
			| substr(x,1,4) == "`i'thB" ///
			| substr(x,1,6) == "`i'th (S" ///
			| substr(x,1,6) == "`i'th (s" ///
			| substr(x,1,5) == "`i'th S" ///
		    | substr(x,1,5) == "`i'th s" )
}
forval i = 1/9{
	forval j = 0/9 {
		replace batt1 = "`i'`j' SB" if (substr(x,1,5)=="`i'`j'th," ///
			| substr(x,1,6) == "`i'`j'th ," ///
		    | substr(x,1,6) == "`i'`j'th B" ///
			| substr(x,1,5) == "`i'`j'thB" ///
			| substr(x,1,7) == "`i'`j'th (S" ///
			| substr(x,1,7) == "`i'`j'th (s" ///
			| substr(x,1,6) == "`i'`j'th S" ///
		    | substr(x,1,6) == "`i' s" )
	}
}

* Iterations of Battalions
forval k=1/3{
	replace batt1 = "1.`k' SB" if (substr(x,1,15) == "`k'/1st Battalion")
	forval i = 2/9{
		replace batt1 = "`i'1.`k' SB" if (substr(x,1,16) == "`k'/`i'1st Battalion")
	}
	replace batt1 = "2.`k' SB" if (substr(x,1,15) == "`k'/2nd Battalion")
	forval i = 2/9{
		replace batt1 = "`i'2.`k' SB" if ( substr(x,1,16) == "`k'/`i'2nd Battalion")
	}
	replace batt1 = "3.`k' SB" if (substr(x,1,15) == "`k'/3rd Battalion")
	forval i = 2/9{
		replace batt1 = "`i'3.`k' SB" if (substr(x,1,16) == "`k'/`i'3rd Battalion")
	}
	forval i = 4/9{
		replace batt1 =  "`i'.`k' SB" if (substr(x,1,15) == "`k'/`i'th Battalion")
	}
	forval i = 1/9{
		forval j = 0/9 {
			replace batt1 = "`i'`j'.`k' SB" if (substr(x,1,16) == "`k'/`i'`j'th Battalion")
		}
	}
}

* RESERVE BATTALIONS
* "st"s 
replace batt1 = "1 RB" if (substr(x,1,13) == "1st (Reserve)" ///
			| substr(x,1,11) == "1st Reserve")
forval i = 2/9{
	replace batt1 = "`i'1 RB" if (substr(x,1,14) == "`i'1st (Reserve)" ///
			| substr(x,1,12) == "`i'1st Reserve")
}
* "nd"s
replace batt1 = "2 RB" if (substr(x,1,13) == "2nd (Reserve)" ///
			| substr(x,1,11) == "2nd Reserve")
forval i = 2/9{
	replace batt1 = "`i'2 RB" if (substr(x,1,14) == "`i'2nd (Reserve)" ///
			| substr(x,1,12) == "`i'2nd Reserve")
}
* "rd"s
replace batt1 = "3 RB" if (substr(x,1,13) == "3rd (Reserve)" ///
			| substr(x,1,11) == "3rd Reserve")
forval i = 2/9{
	replace batt1 = "`i'3 RB" if (substr(x,1,14) == "`i'3rd (Reserve)" ///
			| substr(x,1,12) == "`i'3rd Reserve")
}
* "th"s
forval i = 4/9{
	replace batt1 =  "`i' RB" if (substr(x,1,13) == "`i'th (Reserve)" ///
			| substr(x,1,11) == "`i'th Reserve")
}
forval i = 1/9{
	forval j = 0/9 {
		replace batt1 = "`i'`j' RB" if (substr(x,1,14) == "`i'`j'th (Reserve)" ///
			| substr(x,1,12) == "`i'`j'th Reserve")
	}
}

* Iterations of Battalions
forval k=1/3{
	replace batt1 = "1.`k' RB" if (substr(x,1,15) == "`k'/1st (Reserve)" | substr(x,1,13) == "`k'/1st Reserve")
	forval i = 2/9{
		replace batt1 = "`i'1.`k' RB" if (substr(x,1,16) == "`k'/`i'1st (Reserve)" | substr(x,1,14) == "`k'/`i'1st Reserve")
	}
	replace batt1 = "2.`k' RB" if (substr(x,1,15) == "`k'/2nd (Reserve)" | substr(x,1,13) == "`k'/2nd Reserve")
	forval i = 2/9{
		replace batt1 = "`i'2.`k' RB" if (substr(x,1,16) == "`k'/`i'2nd (Reserve)" | substr(x,1,14) == "`k'/`i'2nd Reserve")
	}
	replace batt1 = "3.`k' RB" if (substr(x,1,15) == "`k'/3rd (Reserve)" | substr(x,1,13) == "`k'/3rd Reserve")
	forval i = 2/9{
		replace batt1 = "`i'3.`k' RB" if (substr(x,1,16) == "`k'/`i'3rd (Reserve)" | substr(x,1,14) == "`k'/`i'3rd Reserve")
	}
	forval i = 4/9{
		replace batt1 =  "`i'.`k' RB" if (substr(x,1,15) == "`k'/`i'th (Reserve)" | substr(x,1,13) == "`k'/`i'th Reserve")
	}
	forval i = 1/9{
		forval j = 0/9 {
			replace batt1 = "`i'`j'.`k' RB" if (substr(x,1,16) == "`k'/`i'`j'th (Reserve)" | substr(x,1,14) == "`k'/`i'`j'th Reserve")
		}
	}
}

* Pals/city 
forval i = 1/8{
	local num = `i'+15
	replace batt1 = "`num' SB" if (strpos(x,"City")>0 & substr(x,1,1)=="`i'")
}
replace batt1 = "24 SB" if (substr(x,1,6) == "Oldham" | substr(x,1,11) == "24th Oldham" ///
	| substr(x,1,7) == "Pioneer" | substr(x,1,12) == "24th Pioneer")

* OTHER
* Garrison Battalions
forval i = 1/2{
	replace batt1 = "`i' GaB" if ((strpos(x,"Garr") > 0 | strpos(x,"Garrision")>0)& substr(x,1,1) == "`i'")
}
* Graduated Battalions
forval i = 51/52{
	replace batt1 = "`i' GrB" if ((strpos(x,"Grad") > 0 | strpos(x,"GRAD")>0) & substr(x,1,2)=="`i'")
}
* Young Soldier
replace batt1 = "53 YB" if (batt1 == "53 SB" | substr(x,1,2)=="53")

* EXTRANEOUS (some uncertainty)
replace batt1 = "8 SB" if x == "8th (A) Battalion"
replace batt1 = "51 GaB" if strpos(x,"51st Garrison")>0 & strpos(x,",")==0
replace batt1 = "52 GaB" if (strpos(x,"52nd Garrison")>0 | strpos(x,"52nd (Garrison)")>0) & strpos(x,",")==0
replace batt1 = "1 GrB" if (strpos(x,"Grad") > 0 & substr(x,1,1)=="1")
replace batt1 = "2 GrB" if (strpos(x,"Grad") > 0 & substr(x,1,1)=="2")

forval i = 1/50{
	replace batt1 = "`i' PB" if ((substr(x,5,4)=="Prov" | substr(x,6,4) == "Prov") & (substr(x,1,1)=="`i'" | substr(x,1,2)=="`i'"))
}
forval i = 1/9{
	replace batt1 = "`i' HS" if (substr(x,1,1)=="`i'" & (substr(x,5,4)=="Home" | substr(x,5,5)== "(Home"))
	replace batt1 = "`i' TR" if (substr(x,1,1)=="`i'" & (substr(x,5,2)=="Tr" | substr(x,5,3)=="(Tr"))
    replace batt1 = "`i' Dep" if (substr(x,1,1)=="`i'" & substr(x,5,5)=="Depot")
	replace batt1 = "`i' Bty" if (substr(x,1,1)=="`i'" & substr(x,5,7)=="Battery")
	replace batt1 = "`i' Brig" if (substr(x,1,1)=="`i'" & substr(x,5,7)=="Brigade")
	replace batt1 = "`i' Fib" if (substr(x,1,1)=="`i'" & substr(x,5,5)=="Filed")
	replace batt1 = "`i' OC" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Off")
	replace batt1 = "`i' Pio" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Pio" & `i'!=24)	
	replace batt1 = "`i' MCB" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Mil")	
}
forval i = 10/99{
	replace batt1 = "`i' HS" if (substr(x,1,2)=="`i'" & (substr(x,6,4)=="Home" | substr(x,6,5)== "(Home"))
	replace batt1 = "`i' TR" if (substr(x,1,2)=="`i'" & (substr(x,6,2)=="Tr" | substr(x,6,3)=="(Tr"))
	replace batt1 = "`i' Dep" if (substr(x,1,2)=="`i'" & substr(x,6,5)=="Depot")
	replace batt1 = "`i' Bty" if (substr(x,1,2)=="`i'" & substr(x,6,7)=="Battery")
	replace batt1 = "`i' Brig" if (substr(x,1,2)=="`i'" & substr(x,6,7)=="Brigade")
	replace batt1 = "`i' FiB" if (substr(x,1,2)=="`i'" & substr(x,6,5)=="Filed")
	replace batt1 = "`i' OC" if (substr(x,1,2)=="`i'" & substr(x,6,3)=="Off")
	replace batt1 = "`i' Pio" if (substr(x,1,2)=="`i'" & substr(x,6,3)=="Pio" & `i'!=24)	
	replace batt1 = "`i' MCB" if (substr(x,1,2)=="`i'" & substr(x,6,3)=="Mil")	
}
forval i = 100/400{
	replace batt1 = "`i' SB" if (substr(x,1,3)=="`i'" & strpos(x,"Reserve")==0)
	replace batt1 = "`i' RB" if (substr(x,1,3)=="`i'" & (substr(x,7,3)=="Res" | substr(x,7,3)=="(Re"))
	replace batt1 = "`i' HS" if (substr(x,1,3)=="`i'" & (substr(x,7,4)=="Home" | substr(x,7,5)== "(Home"))
	replace batt1 = "`i' TR" if (substr(x,1,3)=="`i'" & (substr(x,7,2)=="Tr" | substr(x,7,3)=="(Tr"))
	replace batt1 = "`i' Dep" if (substr(x,1,3)=="`i'" & substr(x,7,5)=="Depot")
	replace batt1 = "`i' Bty" if (substr(x,1,3)=="`i'" & substr(x,7,7)=="Battery")
	replace batt1 = "`i' Brig" if (substr(x,1,3)=="`i'" & substr(x,7,7)=="Brigade")
	replace batt1 = "`i' FiB" if (substr(x,1,3)=="`i'" & substr(x,7,5)=="Filed")
	replace batt1 = "`i' OC" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Off")
	replace batt1 = "`i' Pio" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Pio" & `i'!=24)	
	replace batt1 = "`i' MCB" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Mil")	
}
replace batt1 = "CoOnly" if (strpos(x,"Comp")>0 & strpos(x,"Bat")==0)
forval i = 1/30{
	replace batt1 = "`i' SB" if (strpos(x,"Company, `i'th Battalion")>0 ///
		| strpos(x,"Company, `i'nd Battalion")>0 ///
		| strpos(x,"Company, `i'st Battalion")>0 ///
		| strpos(x,"Company, `i'rd Battalion")>0)
	forval j = 1/3{
		replace batt1 = "`i'.`j' SB" if (strpos(x,"Company, `j'/`i'th Battalion")>0 ///
		| strpos(x,"Company, `j'/`i'nd Battalion")>0 ///
		| strpos(x,"Company, `j'/`i'st Battalion")>0 ///
		| strpos(x,"Company, `j'/`i'rd Battalion")>0)
	}
}
replace batt1 = "SpR" if (strpos(x,"Special Reserve")>0 & strpos(x,",")==0)
replace batt1 = "ArR" if (strpos(x,"Army Reserve")>0 & strpos(x,",")==0)
replace batt1 = "SiB" if (strpos(x,"Siege Battery")>0 & strpos(x,",")==0)
replace batt1 = "GaB" if batt1=="Garrison Battalion"
replace batt1 = "Hos" if (strpos(x,"Hospital")>0 & strpos(x,",")==0)
replace batt1 = "ROnly" if (x == "Reserve" | x == "Reserve Battalion")
replace batt1 = "Dep" if (strpos(x,"Depot")>0 & strpos(x,",")==0)
replace batt1 = "NM" if strpos(x,"London")>0

forval i=1/9{
	replace batt1 = "`i' CaB" if (substr(x,1,1)=="`i'" &  ///
		(substr(x,5,2)=="CB" | substr(x,5,2) == "CR" | substr(x,5,2) == "Ca"))
}

* Uncertain /'s - use first number
forval i = 1/9{
	forval j = 1/9{
		replace batt1 = "`j' SB" if (substr(x,1,3)=="`j'/`i'" ///
		    | substr(x,1,5)=="`j'th/`i'" ///
			| substr(x,1,5)=="`j'st/`i'" ///
			| substr(x,1,5)=="`j'nd/`i'" ///
			| substr(x,1,5)=="`j'rd/`i'" ///
			| substr(x,1,9)=="`j'th & `i'th")
	}
	forval j = 10/50{
		replace batt1 = "`j' SB" if (substr(x,1,4)=="`j'/`i'" ///
		    | substr(x,1,6)=="`j'th/`i'" ///
			| substr(x,1,6)=="`j'st/`i'" ///
			| substr(x,1,6)=="`j'nd/`i'" ///
			| substr(x,1,6)=="`j'rd/`i'" ///
			| substr(x,1,10)=="`j'th & `i'th")
	}
}
forval i = 10/50{
	forval j = 1/9{
		replace batt1 = "`j' SB" if (substr(x,1,4)=="`j'/`i'" ///
			| substr(x,1,6)=="`j'th/`i'" ///
			| substr(x,1,6)=="`j'st/`i'" ///
			| substr(x,1,6)=="`j'nd/`i'" ///
			| substr(x,1,6)=="`j'rd/`i'" ///
			| substr(x,1,10)=="`j'th & `i'th")
	}
	forval j = 10/50{
		replace batt1 = "`j' SB" if (substr(x,1,5)=="`j'/`i'" ///
		    | substr(x,1,7)=="`j'th/`i'" ///
			| substr(x,1,7)=="`j'st/`i'" ///
			| substr(x,1,7)=="`j'nd/`i'" ///
			| substr(x,1,7)=="`j'rd/`i'" ///
			| substr(x,1,11)=="`j'th & `i'th")
	}
}
replace batt1 = "1 SB" if substr(x,1,5)=="1st 3"

* 8.1 is also known as Ardwick
replace batt1 = "8.1 SB" if (substr(x,1,8)=="1st (Ard" ///
	| substr(x,1,8)=="8th (Ard" ///
	| substr(x,1,10)=="1/8th (Ard" ///
	| substr(x,1,13)=="1st, 8th (Ard" ///
	| substr(x,1,11)=="1st (AA), 8" /// 
	| substr(x,1,7) == "1st Ald")

*************************************************************

* TYPE - determined via the listings on the Long Long Trail
gen type1 = ""

replace type1 = "Regular" if ( ///
	  batt1 == "1 SB" | batt1 == "2 SB" | batt1 == "3 SB" ///
	| batt1 == "4 SB")
replace type1 = "Territorial Force" if ( ///
	  batt1 == "5 SB" | batt1 == "5.1 SB" | batt1 == "6 SB" ///
	| batt1 == "6.1 SB" | batt1 == "7 SB" | batt1 == "7.1 SB" ///
	| batt1 == "8 SB" | batt1 == "8.1 SB" | batt1 == "9 SB" ///
	| batt1 == "9.1 SB" | batt1 == "10 SB" | batt1 == "10.1 SB" ///
	| batt1 == "5.2 SB" | batt1 == "6.2 SB" | batt1 == "7.2 SB" ///
	| batt1 == "8.2 SB" | batt1 == "9.2 SB" | batt1 == "10.2 SB" ///
    | batt1 == "8.3 SB" | batt1 == "9.3 SB" | batt1 == "10.3 SB" ///
	| batt1 == "28 SB")
replace type1 = "New Armies" if ( ///
	  batt1 == "11 SB" | batt1 == "12 SB" | batt1 == "13 SB" ///
    | batt1 == "14 SB")
replace type1 = "Pals" if ( /// 
	  batt1 == "16 SB" | batt1 == "17 SB" | batt1 == "18 SB" ///
    | batt1 == "19 SB" | batt1 == "20 SB" | batt1 == "21 SB" ///
    | batt1 == "22 SB" | batt1 == "23 SB" | batt1 == "24 SB" ///
	| batt1 == "25 SB" | batt1 == "26 SB" | batt1 == "27 SB")
replace type1 = "Other" if ( ///
      batt1 == "29 SB" | batt1 == "1 GaB" | batt1 == "2 GaB" ///
    | batt1 == "51 GrB" | batt1 == "52 GrB" | batt1 == "53 YB") 
replace type1 = "Unknown" if ( ///
	  strpos(batt1,"PB")>0 | strpos(batt1,"HS")>0| strpos(batt1, "TB")>0 ///
	| strpos(batt1, "CoOnly")>0| strpos(batt1, "Dep" )>0| strpos(batt1, "Bty")>0 ///
	| strpos(batt1, "SpR")>0 | strpos(batt1, "ArR")>0 | strpos(batt1, "SiB")>0 ///
	| strpos(batt1, "GaB")>0 | strpos(batt1, "Hos")>0| strpos(batt1, "ROnly")>0 ///
	| strpos(batt1, "Brig") >0 | strpos(batt1,"FiB")>0 | strpos(batt1,"OC")>0 ///
	| strpos(batt1, "Pio")>0 | strpos(batt1,"MCB")>0 | strpos(batt1,"NM")>0 ///
	| strpos(batt1, "CaB")>0)
