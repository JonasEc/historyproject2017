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
*    MCB   Military Cross rBattalion
*    NM	   Not Manchester
*    CaB    Cavalry Battalion
*    ClOnly Class only (not enough information)
*    LB    Labour Battalion
*    RD    Recruit's Distribution
*    HoS   Horse Service
*    UC	   Unclear
*    CyB   Cyclist Battalion
*    IB    Infantry Battalion
*    DU	   Dispersal Unit
*    DB    Divisional Battalion
*    PcB   Protection Battalion
*    AB    Artillery Battalion
*    Ri    Rifles
*    Lo    Local
*    En	   Engineers

clear 

cd "/home/jonasmg/Prog/scrapinghistory"

import delimited /Data/ManBattListTyped.csv

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
			| substr(x,1,3) == "`i' b" ///
			| substr(x,1,2) == "`i'B" ///
			| substr(x,1,4) == "`i' (S" ///
			| substr(x,1,3) == "`i'(S" ///
			| substr(x,1,4) == "`i' (s" ///
			| substr(x,1,3) == "`i' S" ///
		    | substr(x,1,4) == "`i' s" )
}
forval i=10/99{
	replace batt1 = "`i' SB" if (substr(x,1,3) == "`i'," ///
			| substr(x,1,4) == "`i' ," ///
			| substr(x,1,4) == "`i' B" ///
			| substr(x,1,3) == "`i' b" ///
			| substr(x,1,3) == "`i'B" ///
			| substr(x,1,5) == "`i' (S" ///
			| substr(x,1,4) == "`i'(S" ///
			| substr(x,1,5) == "`i' (s" ///
			| substr(x,1,4) == "`i' S" ///
		    | substr(x,1,5) == "`i' s" )
}
* "st"s 
replace batt1 = "1 SB" if (substr(x,1,4) == "1st," ///
			| substr(x,1,5) == "1st ," ///
			| substr(x,1,5) == "1st B" ///
			| substr(x,1,5) == "1st b" ///
			| substr(x,1,4) == "1stB" ///
			| substr(x,1,6) == "1st (S" ///
			| substr(x,1,5) == "1st(S" ///
			| substr(x,1,6) == "1st (s" ///
			| substr(x,1,5) == "1st S" ///
		    | substr(x,1,5) == "1st s" )
forval i = 2/9{
	replace batt1 = "`i'1 SB" if (substr(x,1,5)=="`i'1st," ///
			| substr(x,1,6) == "`i'1st ," ///
			| substr(x,1,6) == "`i'1st B" ///
			| substr(x,1,6) == "`i'1st b" ///
			| substr(x,1,5) == "`i'1stB" ///
		    | substr(x,1,7) == "`i'1st (S" ///
			| substr(x,1,6) == "`i'1st(S" ///
			| substr(x,1,7) == "`i'1st (s" ///
			| substr(x,1,6) == "`i'1st S" ///
		    | substr(x,1,6) == "`i'1st s" )
}
* "nd"s
replace batt1 = "2 SB" if (substr(x,1,4) == "2nd," ///
			| substr(x,1,5) == "2nd ," ///
			| substr(x,1,5) == "2nd B" ///
			| substr(x,1,5) == "2nd b" ///
			| substr(x,1,4) == "2ndB" ///
		    | substr(x,1,6) == "2nd (S" ///
			| substr(x,1,5) == "2nd(S" ///
			| substr(x,1,6) == "2nd (s" ///
			| substr(x,1,5) == "2nd S" ///
		    | substr(x,1,5) == "2nd s" )
forval i = 2/9{
	replace batt1 = "`i'2 SB" if (substr(x,1,5)=="`i'2nd," ///
			| substr(x,1,6) == "`i'2nd ," ///
			| substr(x,1,6) == "`i'2nd B" ///
			| substr(x,1,6) == "`i'2nd b" ///
			| substr(x,1,5) == "`i'2ndB" ///
			| substr(x,1,7) == "`i'2nd (S" ///
			| substr(x,1,6) == "`i'2nd(S" ///
			| substr(x,1,7) == "`i'2nd (s" ///
			| substr(x,1,6) == "`i'2nd S" ///
		    | substr(x,1,6) == "`i'2nd s" )
}
* "rd"s
replace batt1 = "3 SB" if (substr(x,1,4) == "3rd," ///
			| substr(x,1,5) == "3rd ," ///
			| substr(x,1,5) == "3rd B" ///
			| substr(x,1,5) == "3rd b" ///
			| substr(x,1,4) == "3rdB" ///
			| substr(x,1,6) == "3rd (S" ///
			| substr(x,1,5) == "3rd(S" ///
			| substr(x,1,6) == "3rd (s" ///
			| substr(x,1,5) == "3rd S" ///
		    | substr(x,1,5) == "3rd s" )
forval i = 2/9{
	replace batt1 = "`i'3 SB" if (substr(x,1,5)=="`i'3rd," ///
			| substr(x,1,6) == "`i'3rd ," ///
			| substr(x,1,6) == "`i'3rd B" ///
			| substr(x,1,6) == "`i'3rd b" ///
			| substr(x,1,5) == "`i'3rdB" ///
			| substr(x,1,7) == "`i'3rd (S" ///
		    | substr(x,1,6) == "`i'3rd(S" ///
			| substr(x,1,7) == "`i'3rd (s" ///
			| substr(x,1,6) == "`i'3rd S" ///
		    | substr(x,1,6) == "`i'3rd s" )
}
* "th"s
forval i = 4/9{
	replace batt1 =  "`i' SB" if (substr(x,1,4)=="`i'th," ///
			| substr(x,1,5) == "`i'th ," ///
			| substr(x,1,5) == "`i'th B" ///
			| substr(x,1,5) == "`i'th b" ///
			| substr(x,1,4) == "`i'thB" ///
			| substr(x,1,6) == "`i'th (S" ///
			| substr(x,1,5) == "`i'th(S" ///
			| substr(x,1,6) == "`i'th (s" ///
			| substr(x,1,5) == "`i'th S" ///
		    | substr(x,1,5) == "`i'th s" )
}
forval i = 1/9{
	forval j = 0/9 {
		replace batt1 = "`i'`j' SB" if (substr(x,1,5)=="`i'`j'th," ///
			| substr(x,1,6) == "`i'`j'th ," ///
		    | substr(x,1,6) == "`i'`j'th B" ///
			| substr(x,1,6) == "`i'`j'th b" ///
			| substr(x,1,5) == "`i'`j'thB" ///
			| substr(x,1,7) == "`i'`j'th (S" ///
			| substr(x,1,6) == "`i'`j'th(S" ///
			| substr(x,1,7) == "`i'`j'th (s" ///
			| substr(x,1,6) == "`i'`j'th S" ///
		    | substr(x,1,6) == "`i' s" )
	}
}
* 100s
forval i = 1/9{
	forval j = 0/9 {
		forval l = 0/9{
			replace batt1 = "`i'`j'`l' SB" if (substr(x,1,3)=="`i'`j'`l'" & /// 
			(substr(x,7,1)=="B" | substr(x,6,1)==","))
		}
	}
}

* Iterations of Battalions
forval k=1/3{
	replace batt1 = "1.`k' SB" if (substr(x,1,15) == "`k'/1st Battalion" | substr(x,1,6) == "`k'/1st,")
	forval i = 2/9{
		replace batt1 = "`i'1.`k' SB" if (substr(x,1,16) == "`k'/`i'1st Battalion" | substr(x,1,7) == "`k'/`i'1st,")
	}
	replace batt1 = "2.`k' SB" if (substr(x,1,15) == "`k'/2nd Battalion" | substr(x,1,6) == "`k'/2nd,")
	forval i = 2/9{
		replace batt1 = "`i'2.`k' SB" if ( substr(x,1,16) == "`k'/`i'2nd Battalion" | substr(x,1,7) == "`k'/`i'2nd,")
	}
	replace batt1 = "3.`k' SB" if (substr(x,1,15) == "`k'/3rd Battalion" | substr(x,1,6) == "`k'/3rd,")
	forval i = 2/9{
		replace batt1 = "`i'3.`k' SB" if (substr(x,1,16) == "`k'/`i'3rd Battalion" | substr(x,1,7) == "`k'/`i'3rd,")
	}
	forval i = 4/9{
		replace batt1 =  "`i'.`k' SB" if (substr(x,1,15) == "`k'/`i'th Battalion" | substr(x,1,6) == "`k'/`i'th,")
	}
	forval i = 1/9{
		forval j = 0/9 {
			replace batt1 = "`i'`j'.`k' SB" if (substr(x,1,16) == "`k'/`i'`j'th Battalion" | substr(x,1,7) == "`k'/`i'`j'th,")
		}
	}
}

* RESERVE BATTALIONS
* "st"s 
replace batt1 = "1 RB" if (substr(x,1,13) == "1st (Reserve)" ///
			| substr(x,1,11) == "1st Reserve" | substr(x,1,10)=="1st Reseve")
forval i = 2/9{
	replace batt1 = "`i'1 RB" if (substr(x,1,14) == "`i'1st (Reserve)" ///
			| substr(x,1,12) == "`i'1st Reserve" | substr(x,1,10)=="`i'1st Reseve")
}
* "nd"s
replace batt1 = "2 RB" if (substr(x,1,13) == "2nd (Reserve)" ///
			| substr(x,1,11) == "2nd Reserve" | substr(x,1,10)=="2nd Reseve")
forval i = 2/9{
	replace batt1 = "`i'2 RB" if (substr(x,1,14) == "`i'2nd (Reserve)" ///
			| substr(x,1,12) == "`i'2nd Reserve" | substr(x,1,11)=="`i'2nd Reseve")
}
* "rd"s
replace batt1 = "3 RB" if (substr(x,1,13) == "3rd (Reserve)" ///
			| substr(x,1,11) == "3rd Reserve" | substr(x,1,10)=="3rd Reseve")
forval i = 2/9{
	replace batt1 = "`i'3 RB" if (substr(x,1,14) == "`i'3rd (Reserve)" ///
			| substr(x,1,12) == "`i'3rd Reserve" | substr(x,1,11)=="`i'3rd Reseve")
}
* "th"s
forval i = 4/9{
	replace batt1 =  "`i' RB" if (substr(x,1,13) == "`i'th (Reserve)" ///
			| substr(x,1,11) == "`i'th Reserve" | substr(x,1,10)=="`i'th Reseve")
}
forval i = 1/9{
	forval j = 0/9 {
		replace batt1 = "`i'`j' RB" if (substr(x,1,14) == "`i'`j'th (Reserve)" ///
			| substr(x,1,12) == "`i'`j'th Reserve" | substr(x,1,11)=="`i'`j'th Reseve")
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
	replace batt1 = "`num' SB" if ((strpos(x,"City")>0 | strpos(x,"city")>0)& substr(x,1,1)=="`i'")
}
replace batt1 = "24 SB" if (substr(x,1,6) == "Oldham" | substr(x,1,11) == "24th Oldham" ///
	| substr(x,1,7) == "Pioneer" | substr(x,1,12) == "24th Pioneer" | substr(x,1,7)=="24th (O" ///
	| substr(x,1,7) == "24th (P" | strpos(x,"Old Ham")>0 | substr(x,1,5)== "3rd O" | substr(x,1,5)=="4th O") /* last two are typos, I think */ 
* typo:
replace batt1 = "16 SB" if x=="Ist City Battalion" | x=="1st C Battalion"
replace batt1 = "17 SB" if substr(x,1,7)=="2nd C B"
replace batt1 = "22 SB" if substr(x,1,7)=="7th Cdy" | x=="City Battalion, 22nd Battalion"
	
* OTHER
* Garrison Battalions
forval i = 1/5{
	replace batt1 = "`i' GaB" if ((strpos(x,"Garr") > 0 | strpos(x,"Garrision")>0|strpos(x,"Grassion")>0)& substr(x,1,1) == "`i'")
}
* Graduated Battalions
forval i = 51/52{
	replace batt1 = "`i' GrB" if ((strpos(x,"Grad") > 0 | strpos(x,"GRAD")>0) & substr(x,1,2)=="`i'")
}
* Young Soldier
forval i = 52/58{
	replace batt1 = "`i' YB" if (batt1 == "`i' SB" | substr(x,1,2)=="`i'")
}

* EXTRANEOUS (some uncertainty)
replace batt1 = "51 GaB" if strpos(x,"51st Garrison")>0 & strpos(x,",")==0
replace batt1 = "52 GaB" if (strpos(x,"52nd Garrison")>0 | strpos(x,"52nd (Garrison)")>0) & strpos(x,",")==0
replace batt1 = "1 GaB" if (strpos(x,", 1st Garrison")>0)
replace batt1 = "1 GrB" if (strpos(x,"Grad") > 0 & substr(x,1,1)=="1")
replace batt1 = "2 GrB" if (strpos(x,"Grad") > 0 & substr(x,1,1)=="2")
replace batt1 = "3 GrB" if (strpos(x,"Grad") > 0 & substr(x,1,1)=="3")
replace batt1 = "61 GrB" if (strpos(x,"Grad") > 0 & substr(x,1,2)=="61")
replace batt1 = "51 GrB" if x=="51st Glad Battalion" | strpos(x,"Training Reserve, 51st Grad")>0
replace batt1 = "50 GrB" if substr(x,1,11)=="50th (Grad)"
replace batt1 = "5 GrB" if substr(x,1,8)=="5th Grad"



* Miscelaneous
replace batt1 = "SpR" if (strpos(x,"Special Reserve")>0 & strpos(x,",")==0)
replace batt1 = "ArR" if (strpos(x,"Army Reserve")>0 & strpos(x,",")==0)
replace batt1 = "SiB" if (strpos(x,"Siege Battery")>0 & strpos(x,",")==0)
replace batt1 = "GaB" if batt1=="Garrison Battalion"
replace batt1 = "Hos" if (strpos(x,"Hospital")>0 & strpos(x,",")==0)
replace batt1 = "ROnly" if (x == "Reserve" | x == "Reserve Battalion")
replace batt1 = "Dep" if (strpos(x,"Depot")>0 & strpos(x,",")==0)
replace batt1 = "NM" if (strpos(x,"London")>0 | strpos(x,"Highland")>0 | strpos(x,"Leith")>0 ///
	| strpos(x,"Northumbrian")>0 | strpos(x,"Hallamshire")>0 | strpos(x,"Irish")>0 ///
	| strpos(x,"Warwickshire")>0 | strpos(x,"Leicester")>0 | strpos(x,"Liverpool")>0 ///
	| strpos(x,"Stafford")>0)
replace batt1 = "DU" if strpos(x,"Dispers")>0

replace batt1 = "UC" if (strpos(x,"CB")>0 | strpos(x,"CR")>0 ///
	| strpos(x,"PNR")>0 | strpos(x,"PWP")>0 | strpos(x,"Volunt")>0 ///
	| strpos(x,"Glamorgan")>0 | strpos(x,"General")>0 | strpos(x,"572")>0 ///
	| strpos(x,"VB")>0 | strpos(x,"822nd") >0 | strpos(x,"NL")>0 /// 
	| strpos(x,"AA")>0 | strpos(x,"AM")>0 | strpos(x,"Admin")>0 ///
	| strpos(x,"Gymnast")>0 | strpos(x,"Pay")>0 | strpos(x,"76th Army Brigade")>0 /// 
	| strpos(x,"City Battion, 22nd Battalion")>0 | strpos(x,"1883")>0 /// 
	| strpos(x,"Military Cross")>0 | strpos(x,"Reception")>0 | strpos(x,"District Preston")>0 ///
	| strpos(x,"Rest Camp")>0 | strpos(x,"11th Or") > 0 | strpos(x,"126th L T M")>0 ///
	| strpos(x,"29th Field Amb")>0 | strpos(x,"Arttilery School")>0 | strpos(x,"3rd Border")>0 ///
	| strpos(x,"3rd Ciad")>0 | strpos(x,"51st (Grenadier")>0 | substr(x,1,6)=="8th (4" /// 
	| strpos(x,"Mechanical Transport")>0 | strpos(x,"17th OC")>0 | strpos(x,"Preston Road")>0 ///
	| x=="1st Vol Battalion" | strpos(x,"Grand Ba")>0 | x=="3rd Manchester" ///
	| strpos(x,"Fetney Camp")>0 | strpos(x,"Timmer")>0 | strpos(x,"Veterinary")>0 /// 
	| strpos(x,"Aldershot")>0 | strpos(x,"Int Brigade")>0 | strpos(x,"D/199")>0 /// 
	| strpos(x,"G/28")>0 | strpos(x,"GS/21")>0 | strpos(x,"Officer Cadet")>0 /// 
	| strpos(x,"No 5th Supernumerary, 8th")>0 | x == "No 3rd Supply, 6th Battalion" ///
	| strpos(x,"Naval")>0)  
	* I believe the 1st Vol Battalion may be the 7th (territorial) battalion
* if no numbers
replace batt1 = "UC" if (strpos(x,"0")==0 & strpos(x,"1")==0 & strpos(x,"2")==0 ///
 & strpos(x,"3")==0 & strpos(x,"4")==0 & strpos(x,"5")==0 & strpos(x,"6")==0 ///
 & strpos(x,"7")==0 & strpos(x,"8")==0 & strpos(x,"9")==0 & batt1=="")

replace batt1 = "En" if strpos(x,"Engineers")>0
forval i = 1/50{
	replace batt1 = "`i' PB" if ((substr(x,5,4)=="Prov" | substr(x,6,4) == "Prov" | substr(x,7,4)=="Prov") & (substr(x,1,1)=="`i'" | substr(x,1,2)=="`i'"))
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
	replace batt1 = "`i' LB" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Lab")	
	replace batt1 = "`i' RD" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Rec")	
	replace batt1 = "`i' HoS" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Hor")	
	replace batt1 = "`i' CyB" if (substr(x,1,1)=="`i'" & (substr(x,5,3)=="Cyc"| substr(x,5,3)=="(Cy"))	
	replace batt1 = "`i' IB" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Inf")	
	replace batt1 = "`i' DB" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Div")	
	replace batt1 = "`i' PcB" if (substr(x,1,1)=="`i'" & substr(x,5,4)=="Prot")	
	replace batt1 = "`i' AB" if (substr(x,1,1)=="`i'" & substr(x,5,3)=="Art")	
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
	replace batt1 = "`i' LB" if (substr(x,1,2)=="`i'" & substr(x,6,3)=="Lab")	
	replace batt1 = "`i' RD" if (substr(x,1,2)=="`i'" & (substr(x,6,3)=="Rec"| substr(x,6,3)=="(Re"))	
	replace batt1 = "`i' HoS" if (substr(x,1,2)=="`i'" & substr(x,6,3)=="Hor")	
	replace batt1 = "`i' CyB" if (substr(x,1,2)=="`i'" & (substr(x,6,3)=="Cyc"| substr(x,6,3)=="(Cy"))	
	replace batt1 = "`i' IB" if (substr(x,1,2)=="`i'" & substr(x,6,3)=="Inf")	
	replace batt1 = "`i' DB" if (substr(x,1,2)=="`i'" & substr(x,6,3)=="Div")	
	replace batt1 = "`i' PcB" if (substr(x,1,2)=="`i'" & substr(x,6,4)=="Prot")
	replace batt1 = "`i' AB" if (substr(x,1,2)=="`i'" & substr(x,6,3)=="Art")	
}
forval i = 100/500{
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
	replace batt1 = "`i' LB" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Lab")	
	replace batt1 = "`i' RD" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Rec")	
	replace batt1 = "`i' HoS" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Hor")	
	replace batt1 = "`i' CyB" if (substr(x,1,3)=="`i'" & (substr(x,7,3)=="Cyc"| substr(x,7,3)=="(Cy"))	
	replace batt1 = "`i' IB" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Inf")	
	replace batt1 = "`i' DB" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Div")	
	replace batt1 = "`i' PcB" if (substr(x,1,3)=="`i'" & substr(x,7,4)=="Prot")
	replace batt1 = "`i' AB" if (substr(x,1,3)=="`i'" & substr(x,7,3)=="Art")	
}

replace batt1 = "ClOnly" if (strpos(x,"Class")>0 & strpos(x,"Battalion")==0)
replace batt1 = "CoOnly" if ((strpos(x,"Comp")>0| strpos(x,"comp")>0) & strpos(x,"Battalion")==0)
replace batt1 = "CoOnly" if x == "3rd Company Battalion" /* typo */
forval i = 1/30{
	replace batt1 = "`i' SB" if (strpos(x,"Company, `i'th Battalion")>0 ///
		| strpos(x,"Company, `i'nd Battalion")>0 ///
		| strpos(x,"Company, `i'st Battalion")>0 ///
		| strpos(x,"Company, `i'rd Battalion")>0 /// 
		| strpos(x,"Company, `i'")>0 )
	replace batt1 = "`i' RB" if (strpos(x,"Company, `i'th Reserve")>0 | strpos(x,"Company, `i'st Reserve")>0 /// 
		| strpos(x,"Company, `i'nd Reserve")>0 | strpos(x,"Company, `i'rd Reserve")>0)
	forval j = 1/3{
		replace batt1 = "`i'.`j' SB" if (strpos(x,"Company, `j'/`i'th Battalion")>0 ///
		| strpos(x,"Company, `j'/`i'nd Battalion")>0 ///
		| strpos(x,"Company, `j'/`i'st Battalion")>0 ///
		| strpos(x,"Company, `j'/`i'rd Battalion")>0)
	}
}
replace batt1 = "8.1 SB" if x == "3rd Company, 1/8th, 1st Battalion"  /* typo */
replace batt1 = "18 SB" if x == "3rd Company, 18th Service Battalion"  /* typo */
replace batt1 = "1 RB" if x == "3rd Company, 1st Reserve Battalion"  /* typo */
replace batt1 = "CoOnly" if x == "1st Company Battalion"
replace batt1 = "18 SB" if x == "3rd Company Battalion, 18th Service Battalion"
replace batt1 = "11 SB" if x == "3rd Company Kitchener Battalion, 11th (General Service) Battalion"
replace batt1 = "22 SB" if x == "7th C, 22nd Service Battalion"

forval i = 1/30{
	replace batt1 = "`i' SB" if (strpos(x,"Depot, `i'")>0 )
	forval j = 1/3{
		replace batt1 = "`i'.`j'. SB" if (strpos(x,"Depot, `j'/`i'")>0)
	}
}

replace batt1 = "Lo" if substr(x,1,5)=="Local"

* Random typos/fixes
replace batt1 = "22 SB" if x == "7th C, 22nd Battalion"
replace batt1 = "26 RB" if strpos(x,"7th Company, 26") >0
replace batt1 = "3 SB" if strpos(x,"7th Company, 3") >0
replace batt1 = "2 SB" if x == "2th Battalion" /* typo */
replace batt1 = "33 SB" if x == "33rd (Yorkshire) Battalion" 
replace batt1 = "8 RB" if strpos(x,"Protection Company, 8th") > 0 
replace batt1 = "3 SB" if x == "3d Battalion" /* typo */ 
replace batt1 = "18 SB" if strpos(x,"Battaion, 18th")>0 /* typo */
replace batt1 = "5 RB" if strpos(x,"h(Reserve")>0 
replace batt1 = "26 Ri" if substr(x,1,10)=="26th Rifle"
replace batt1 = "27 Ri" if substr(x,1,10)== "27th Rifle"
replace batt1 = "60 Ri" if x == "60th Rifles"
replace batt1 = "70 SB" if strpos(x,"70thl")>0
replace batt1 = "8 Bty" if x== "8th A Battery"
replace batt1 = "8 SB" if strpos(x,"8th (a)")>0 | strpos(x,"8th Army B")>0
replace batt1 = "8 RB" if substr(x,1,1)=="8" & strpos(x,"National R")>0
replace batt1 = "90 Bty" if x== "90th Heavy Battery"
replace batt1 = "22 SB" if strpos(x,"C H Q, 22")>0
replace batt1 = "21 SB" if x== "Depot Ashton W Leyne, 21st (Service) Battalion"
replace batt1 = "22 SB" if strpos(x,"Hollinwood, 22")>0
replace batt1 = "3 HS" if strpos(x,"Home Service, 3")>0
replace batt1 = "8 SB" if strpos(x,"8th (Admiral)") >0 
replace batt1 = "53 TB" if x == "Training Reserve 53rd Battalion"
replace batt1 = "23 SB" if substr(x,1,7) == "(23rd S"
replace batt1 = "12 SB" if substr(x,1,7)=="12th (D" /*Duke of Lancaster's Yeomanry merged with 12th in 1917 */
replace batt1 = "8 SB" if substr(x,1,7)=="8th (A)" | substr(x,1,7)=="8th ( R"
replace batt1 = "8.2 RB" if substr(x,1,10)=="8th (2nd R"
replace batt1 = "LB" if substr(x,1,29)=="Western Command Labour Centre"
replace batt1 = "11 Dep" if substr(x,1,18) == "11th Command Depot"
replace batt1 = "27 RB" if substr(x,1,8) == "27th  (R" /* extra space */
replace batt1 = "9.3 SB" if x=="3\9th Battalion"
replace batt1 = "3 SB" if substr(x,1,3)=="3Rd"
replace batt1 = "3 Dep" if substr(x,1,9) == "3rd Deopt"
replace batt1 = "5 RB" if substr(x,1,7) == "5th  (R" | substr(x,1,6)=="5th Rr" /* extra space, typo */
replace batt1 = "7 SB" if x == "7th (45th Provisional Battalion)"
replace batt1 = "8 AB" if substr(x,1,8) == "8th (Art"
replace batt1 = "8 RB" if substr(x,1,6) == "8th (R)" | substr(x,1,15) == "8th Natural Res" | substr(x,1,7) == "8th Res" | strpos(x,"National Reserve, 8th")>0
replace batt1 = "1 SB" if substr(x,1,4) == "Ist,"
replace batt1 = "5 SB" if x == "Permanent Staff, 5th Battalion"
replace batt1 = "7.1 RB" if strpos(x,"Reserve Battalion, 1/7")>0
replace batt1 = "7 RB" if strpos(x,"Brigade, 7th")>0
replace batt1 = "1 RB" if strpos(x,"Special Reserve, 1s")>0
replace batt1 = "2 RB" if strpos(x,"Special Reserve, 2n")>0
replace batt1 = "7 SB" if strpos(x,"Training Centre, 7th")>0

* Entries that start with "No" 
replace batt1 = "11 SB" if substr(x,1,6) == "No 11/"
replace batt1 = "16 SB" if substr(x,1,5) == "No 16"
replace batt1 = "1 SB" if substr(x,1,5) == "No 1s"
replace batt1 = "2 SB" if substr(x,1,5) == "No 2n"
replace batt1 = "3 SB" if substr(x,1,8) == "No 3rd B"
replace batt1 = "3 RB" if substr(x,1,8) == "No 3rd R"
replace batt1 = "4 SB" if substr(x,1,5) == "No 4t"
replace batt1 = "6 SB" if substr(x,1,5) == "No 6t"
replace batt1 = "5 SB" if substr(x,1,5) == "No 5/" | substr(x,1,5) == "No 5t"
replace batt1 = "8 SB" if strpos(x,"No 5th Supernumerary, 8th")>0


* Army reserve section (B)
forval i = 1/30{
	replace batt1 = "`i' RB" if (strpos(x,"Army Reserve")>0  & ///
		(strpos(x,"B), `i'")>0 | strpos(x,"B, `i'")>0 | strpos(x,"Reserve, `i'")>0 | strpos(x,"Section, `i'")>0))
	forval j = 1/3{
		replace batt1 = "`i'.`j' RB" if (strpos(x,"Army Reserve")>0 & strpos(x,"Section B")>0 & ///
		(strpos(x,"B), `j'/`i'")>0 | strpos(x,"B, `j'/`i'")>0 | strpos(x,"Reserve, `j'/`i'")>0))
	}
}
replace batt1 = "3 RB" if strpos(x,"Army Reserve Station, 3rd")>0
 
forval i=1/9{
	replace batt1 = "`i' CaB" if (substr(x,1,1)=="`i'" &  ///
		(substr(x,5,2) == "Ca"))
}

* Uncertain /'s - use first number
forval i = 1/9{
	forval j = 1/9{
		replace batt1 = "`j' SB" if ((substr(x,1,3)=="`j'/`i'" ///
		    | substr(x,1,5)=="`j'th/`i'" ///
			| substr(x,1,5)=="`j'st/`i'" ///
			| substr(x,1,5)=="`j'nd/`i'" ///
			| substr(x,1,5)=="`j'rd/`i'" ///
			| substr(x,1,9)=="`j'th & `i'th") & batt1=="")
	}
	forval j = 10/50{
		replace batt1 = "`j' SB" if ((substr(x,1,4)=="`j'/`i'" ///
		    | substr(x,1,6)=="`j'th/`i'" ///
			| substr(x,1,6)=="`j'st/`i'" ///
			| substr(x,1,6)=="`j'nd/`i'" ///
			| substr(x,1,6)=="`j'rd/`i'" ///
			| substr(x,1,10)=="`j'th & `i'th") & batt1=="")
	}
}
forval i = 10/50{
	forval j = 1/9{
		replace batt1 = "`j' SB" if ((substr(x,1,4)=="`j'/`i'" ///
			| substr(x,1,6)=="`j'th/`i'" ///
			| substr(x,1,6)=="`j'st/`i'" ///
			| substr(x,1,6)=="`j'nd/`i'" ///
			| substr(x,1,6)=="`j'rd/`i'" ///
			| substr(x,1,10)=="`j'th & `i'th") & batt1=="")
	}
	forval j = 10/50{
		replace batt1 = "`j' SB" if ((substr(x,1,5)=="`j'/`i'" ///
		    | substr(x,1,7)=="`j'th/`i'" ///
			| substr(x,1,7)=="`j'st/`i'" ///
			| substr(x,1,7)=="`j'nd/`i'" ///
			| substr(x,1,7)=="`j'rd/`i'" ///
			| substr(x,1,11)=="`j'th & `i'th") & batt1=="")
	}
}
* Order related typos
replace batt1 = "1 SB" if substr(x,1,5)=="1st 3"
replace batt1 = "3 SB" if substr(x,1,7) == "3rd & 1" /* take first element */
replace batt1 = "4 SB" if substr(x,1,5) == "4th &"
replace batt1 = "27 SB" if substr(x,1,6) == "27th 2"
replace batt1 = "3 SB" if substr(x,1,7) == "3rd 1st"
replace batt1 = "4 SB" if substr(x,1,5) == "4th 1"
replace batt1 = "5 RB" if x = "5th to 9th (Reserve) Battalion"
replace batt1 = "85 SB" if substr(x,1,4) == "85/3"

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
	| batt1 == "28 SB" | x=="1st Vol Battalion")
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
	| strpos(batt1, "CaB")>0 | strpos(batt1,"ClOnly")>0 | strpos(batt1,"RD")>0 ///
	| strpos(batt1, "HoS")>0 | strpos(batt1,"UC")>0 | strpos(batt1,"CyB")>0 ///
	| strpos(batt1, "IB")>0 | strpos(batt1,"DU")>0 | strpos(batt1,"DB")>0 ///
	| strpos(batt1, "PcB")>0 | strpos(batt1,"Ri")>0 | strpos(batt1,"Lo")>0 ///
	| strpos(batt1, "En")>0)
