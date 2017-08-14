* Surrey Battalion Classification
* Melanie Wallskog
* 8.2.17

* This do-file classifies the battalions in the Surrey data.
* This process is mostly manual, using the data in PalsList_total.csv, 
* which is the list of Pals Battalions, taken from the Wikipedia.

clear 

cd "/home/jonasmg/Prog/scrapinghistory/data"

*******************************************************
* DATA: Import
*******************************************************

import delimited SCBattList.csv

*******************************************************
* CLASSIFICATION
*******************************************************

gen pals_temp = . /* holder for classification data */ 
lab var pals_temp "=1 if Pals, =2 if contains Pals, =3 if contains Pals but no local, =0 otherwise"

gen x = regiment
sort x

local y replace pals_temp /* save time typing */

`y' = 0 if strpos(x,"Yeomanry")>0 /* placed here, can be overwritten*/
`y' = 0 if x == "3rd West Riding (2nd Batn)"
`y' = 3 if x == "Argyll & Sutherland Highlanders"
`y' = 3 if x == "Bedfordshire Regiment" | x == "Bedforshire Regiment"
`y' = 0 if strpos(x,"Bedfordshire")>0 & strpos(x,"Batn")>0
`y' = 3 if x == "Berkshire Regiment"
`y' = 3 if strpos(x,"Black Watch")>0
`y' = 2 if x == "Border Regiment"
`y' = 0 if strpos(x,"Border")>0 & strpos(x,"Batn")>0
`y' = 0 if x == "Buckinghamshire Regiment"
`y' = 0 if x == "Cambridgeshire Regiment"
`y' = 3 if x == "Cameron Highlanders" 
`y' = 2 if x == "Cheshire Regiment"
`y' = 0 if strpos(x,"Cheshire")>0 & strpos(x,"Batn")>0
`y' = 0 if x == "Coldstream Guards"
`y' = 3 if x == "Connaught Rangers"
`y' = 0 if x == "Corps Of Lon Of The Line"
`y' = 3 if x == "Devonshire Regiment"
`y' = 0 if strpos(x,"Devonshire")>0 & strpos(x,"Batn")>0
`y' = 3 if x == "Dorset Regiment" | x == "Dorsetshire Regiment"
`y' = 3 if x == "Dublin Fusiliers" | x == "Royal Dublin Fusiliers" | x == "Royal Dublin Fusilliers"
`y' = 2 if strpos(x,"Duke Of Cor")>0
`y' = 2 if x == "Durham Light Infantry"
`y' = 0 if strpos(x,"Durham")>0 & strpos(x,"Batn")>0
`y' = 3 if x == "East Kent Regiment"
`y' = 0 if strpos(x,"East Kent")>0 & strpos(x,"Batn")>0
`y' = 3 if x == "East Lancashire Regiment"
`y' = 0 if strpos(x,"East Lancashire")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "East Surey Regiment" | x == "East Surrey Regiment"
`y' = 1 if strpos(x,"East Surrey")>0 & (strpos(x,"12")>0|strpos(x,"13")>0|strpos(x,"14")>0)
`y' = 0 if strpos(x,"East Surrey")>0 & strpos(x,"12")==0 & strpos(x,"13") == 0 & strpos(x,"14")==0 & strpos(x,"Batn")>0
`y' = 0 if x == "East Surrey Regiment, 10th Batt" /* typo */
`y' = 2 if x == "East Yorkshire Regiment"
`y' = 0 if strpos(x,"East Yorkshire")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Essex Regiment"
`y' = 1 if strpos(x,"Essex")>0 & (strpos(x,"13")>0|strpos(x,"14")>0)
`y' = 0 if strpos(x,"Essex")>0 & strpos(x,"13")==0 & strpos(x,"14")==0 & strpos(x,"Batn")>0
`y' = 0 if x == "Essex Yeomanry"
`y' = 0 if x == "Farnborough"
`y' = 0 if x == "Foot Guards"
`y' = 2 if x == "Fusiliers" /* Royal Fusiliers */
`y' = 1 if x == "Fusillers (25th Batn Frontiersman)" 
`y' = 2 if x == "Gloucestershire Regiment"
`y' = 0 if strpos(x,"Gloucestershire")>0 & strpos(x,"Batn")>0
`y' = 3 if x == "Gordon Highlanders"
`y' = 0 if strpos(x,"Gordon")>0 & strpos(x,"Batn")>0
`y' = 0 if strpos(x,"Grenadier")>0
`y' = 0 if strpos(x,"Guards")>0
`y' = 2 if x == "Hampshire Regiment"
`y' = 0 if strpos(x,"Hampshire")>0 & strpos(x,"Batn")>0
`y' = 0 if x == "Hertfordshire Regiment"
`y' = 2 if x == "Highland Light Infantry"
`y' = 0 if x == "Inns Of Court (Otc)" | x == "Inns Of Court Otc"
`y' = 2 if x == "Irish Fusiliers" | x == "Royal Irish Fusiliers"
`y' = 2 if x == "Kings (Liverpool Regiment)" | x == "Liverpool Regiment" | x == "Liverpool Regiment (Kings)"
`y' = 3 if x == "Kings Own Scottish Borderers"
`y' = 0 if strpos(x,"Kings Own Scottish")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Kings Royal Rifle Corps"
`y' = 1 if strpos(x,"Kings Royal Rifle")>0 & (strpos(x,"16")>0|strpos(x,"17")>0 ///
	|strpos(x,"18")>0|strpos(x,"19")>0|strpos(x,"20")>0|strpos(x,"21")>0 ///
	|strpos(x,"22")>0|strpos(x,"23")>0|strpos(x,"24")>0)
`y' = 0 if strpos(x,"Kings Royal Rifle")>0 & strpos(x,"16")==0&strpos(x,"17")==0 ///
	&strpos(x,"18")==0&strpos(x,"19")==0&strpos(x,"20")==0&strpos(x,"21")==0 ///
	&strpos(x,"22")==0&strpos(x,"23")==0&strpos(x,"24")==0 & strpos(x,"Batn")>0
`y' = 2 if x == "Lancashire Fusiliers"
`y' = 1 if strpos(x,"Lancashire Fusiliers")>0 & (strpos(x,"16")>0|strpos(x,"17")>0 ///
	|strpos(x,"18")>0|strpos(x,"19")>0|strpos(x,"20")>0|strpos(x,"21")>0 ///
	|strpos(x,"22")>0)
`y' = 0 if strpos(x,"Lancashire Fusiliers")>0 & strpos(x,"16")==0&strpos(x,"17")==0 ///
	&strpos(x,"18")==0&strpos(x,"19")==0&strpos(x,"20")==0&strpos(x,"21")==0 ///
	&strpos(x,"22")==0 & strpos(x,"Batn")>0
`y' = 2 if x == "Leicestershire Regiment"
`y' = 0 if strpos(x,"Leicestershire")>0 & strpos(x,"Batn")>0
`y' = 3 if strpos(x,"Leinster Regiment")>0
`y' = 2 if x == "Lincolnshire Regiment"
`y' = 0 if strpos(x,"Lincolnshire")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "London Regiment" | x == "Royal Fusiliers"
`y' = 1 if (strpos(x,"London Regiment")>0|strpos(x,"Royal Fusiliers")>0) & (strpos(x,"10")>0|strpos(x,"17")>0 ///
	|strpos(x,"18")>0|strpos(x,"19")>0|strpos(x,"20")>0|strpos(x,"21")>0 ///
	|strpos(x,"22")>0|strpos(x,"23")>0|strpos(x,"24")>0|strpos(x,"25")>0 ///
	|strpos(x,"26")>0|strpos(x,"27")>0|strpos(x,"28")>0|strpos(x,"29")>0 ///
	|strpos(x,"30")>0|strpos(x,"31")>0|strpos(x,"32")>0)
`y' = 0 if (strpos(x,"London Regiment")>0|strpos(x,"Royal Fusiliers")>0) & strpos(x,"10")==0&strpos(x,"17")==0 ///
	&strpos(x,"18")==0&strpos(x,"19")==0&strpos(x,"20")==0&strpos(x,"21")==0 ///
	&strpos(x,"22")==0 &strpos(x,"23")==0&strpos(x,"24")==0&strpos(x,"25")==0 ///
	&strpos(x,"26")==0&strpos(x,"27")==0&strpos(x,"28")==0&strpos(x,"29")==0 ///
	&strpos(x,"30")==0&strpos(x,"31")==0&strpos(x,"32")==0&strpos(x,"Batn")>0
`y' = 1 if x == "Royal Fusiiliers (29th Batn)" | x == "Royal Fusillers (17th Batn)" /// 
	| x == "Royal Fusillers (10th Batn)" | x == "Royal Fusillers (25th Batn)"| x == "Royal Fusillers (10th)" /* typos */
`y' = 1 if x == "Royal Fusillers (Sports Battalion)" /* either 23 or 24, according to Wikipedia */ 
`y' = 0 if x == "Royal Fusiliers (Depot)" | x == "Royal Fusiliers (S Reserve)"
`y' = 3 if x == "Loyal North Lancashire Regiment" | x == "North Lancashire Regiment"
`y' = 2 if x == "Manchester Regiment"
`y' = 0 if strpos(x,"Manchester")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Middlesex Regiment"
`y' = 1 if strpos(x,"Middlesex")>0 & (strpos(x,"16")>0|strpos(x,"17")>0 ///
	|strpos(x,"18")>0|strpos(x,"19")>0|strpos(x,"20")>0|strpos(x,"21")>0 ///
	|strpos(x,"22")>0|strpos(x,"23")>0|strpos(x,"24")>0|strpos(x,"25")>0 ///
	|strpos(x,"26")>0|strpos(x,"27")>0|strpos(x,"28")>0)
`y' = 0 if strpos(x,"Middlesex")>0 & strpos(x,"16")==0&strpos(x,"17")==0 ///
	&strpos(x,"18")==0&strpos(x,"19")==0&strpos(x,"20")==0&strpos(x,"21")==0 ///
	&strpos(x,"22")==0 &strpos(x,"23")==0&strpos(x,"24")==0&strpos(x,"25")==0 ///
	&strpos(x,"26")==0&strpos(x,"27")==0&strpos(x,"28")==0&strpos(x,"Batn")>0
`y' = 0 if strpos(x,"Non Combatant")>0
`y' = 3 if x == "Norfolk Regiment"
`y' = 0 if strpos(x,"Norfolk")>0 & strpos(x,"Batn")>0
`y' = 3 if x == "Northamptonshire Regiment"
`y' = 0 if strpos(x,"Northamptonshire")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Northumberland Regiment" | x == "Northumberland Fusiliers"
`y' = 0 if strpos(x,"Northumberland")>0 & strpos(x,"Batn")>0
`y' = 2 if strpos(x,"Nott")>0 & strpos(x,"Derby")>0
`y' = 3 if x == "Oxfordshire & Bucks Light Infantry" | x == "Oxfordshire And Bucks Light Infantry"
`y' = 0 if strpos(x,"Oxfordshire & Bucks Light Infantry")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Rifle Brigade" | x == "Rifle Brigrade"
`y' = 0 if strpos(x,"Rifle Brigade (")>0 & strpos(x,"Batn")>0
`y' = 3 if x == "Royal Berkshire Regiment"
`y' = 0 if strpos(x,"Royal Berkshire")>0 & strpos(x,"Batn")>0	
`y' = 0 if x == "Royal Household Batn"
`y' = 2 if x == "Royal Inskilling Fusillers" /* typo */
`y' = 0 if (strpos(x,"Royal Inniskilling")>0|strpos(x,"Royal Inniskillan")>0) & strpos(x,"Batn")>0
`y' = 2 if x == "Royal Irish Rifles"
`y' = 1 if x == "Royal Irish Rifles (12th Batn)" | x == "Royal Irish Rifles (20th Batn)"
`y' = 0 if x == "Royal Irish Rifles (4th Batn)"
`y' = 0 if x == "Royal Lancashire Regiment" /* may be the one below, 2*/
`y' = 2 if x == "Royal Lancaster Regiment"
`y' = 3 if x == "Royal Munster Fusiliers"
`y' = 3 if x == "Royal Scots Fusiliers" | x == "Royal Scots Fusillers"
`y' = 2 if x == "Royal Scots (Lothian Regiment)" 
`y' = 0 if strpos(x,"Royal Scots")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Royal Sussex Regiment"
`y' = 0 if strpos(x,"Royal Sussex")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Royal Warwickshire Regiment" | x == "Warwickshire Regiment"
`y' = 2 if x == "Royal Welsh Fusiliers" | x == "Royal Welsh Fusillers"
`y' = 1 if x == "Royal Welsh Fusiliers (18th Batn)"
`y' = 0 if x == "Royal Welsh Fusiliers (22nd Batn)" | x == "Royal Welsh Fusiliers (7th & 5th Batn)" 
`y' = 2 if x == "Royal West Kent Regiment"
`y' = 1 if strpos(x,"Royal West Kent")>0 & (strpos(x,"10")>0|strpos(x,"11")>0|strpos(x,"12")>0)
`y' = 0 if strpos(x,"Royal West Kent")>0 & strpos(x,"10")==0&strpos(x,"11")==0&strpos(x,"12")==0& strpos(x,"Batn")>0
`y' = 2 if x == "Royal West Surrey Regiment"
`y' = 1 if strpos(x,"Royal West Surrey")>0 & (strpos(x,"10")>0|strpos(x,"11")>0|strpos(x,"12")>0)
`y' = 0 if strpos(x,"Royal West Surrey")>0 & strpos(x,"10")==0&strpos(x,"11")==0&strpos(x,"12")==0& strpos(x,"Batn")>0
`y' = 2 if x == "Royal Worcestershire Regiment"
`y' = 2 if x == "Scottish Rifles"| x == "Scottish Rifles (Cameronians)"
`y' = 1 if x == "Scottish Rifles (13th Batn Cameronians)" 
`y' = 0 if strpos(x,"Scottish Rifles")>0 & strpos(x,"13")==0 & strpos(x,"Batn")>0
`y' = 3 if x == "Seaforth Highlanders"
`y' = 3 if x == "Shropshire Light Infantry"
`y' = 3 if x == "Somerset Light Infantry" | x == "Somerset Regiment" | x == "Somerset(Shropshire) Light Infantry"
`y' = 0 if strpos(x,"Somerset")>0 & strpos(x,"Batn")>0
`y' = 2 if strpos(x,"South Lancashire")>0 & strpos(x,"Batn")==0
`y' = 0 if strpos(x,"South Lancashire")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "South Wales Borderers"
`y' = 1 if strpos(x,"South Wales Borderers")>0 & strpos(x,"12")>0
`y' = 0 if strpos(x,"South Wales Borderers *")>0 & strpos(x,"12")==0
`y' = 0 if x == "South Wales Borderers (Bantam)" | x == "South Wales Borderers (Bantams)"
`y' = 2 if x == "Suffolk Regiment"
`y' = 1 if strpos(x,"Suffolk")>0 & (strpos(x,"11")>0|strpos(x,"12")>0|strpos(x,"13")>0)
`y' = 0 if strpos(x,"Suffolk")>0 & strpos(x,"11")==0&strpos(x,"12")==0&strpos(x,"13")==0 & strpos(x,"Batn")>0
`y' = 0 if x == "Sufffolk Regiment (10th Batn)" | x == "Suffolk Regiment (Res Garrison Ramc)" /* typo */
`y' = 0 if strpos(x,"The Prince")>0
`y' = 2 if x == "Welch Regiment" | x == "Welsh Regiment"
`y' = 0 if (strpos(x,"Welch Regiment")>0 | strpos(x,"Welsh Regiment")>0) & strpos(x,"Batn")>0
`y' = 2 if x == "West Yorkshire Regiment"
`y' = 3 if x == "Wiltshire Regiment"
`y' = 0 if strpos(x,"Wiltshire")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Worcestershire Regiment"
`y' = 0 if strpos(x,"Worcestershire")>0 & strpos(x,"Batn")>0
`y' = 2 if x == "Yorkshire & Lancashire Regiment"
`y' = 2 if x == "Yorkshire Regiment"
`y' = 0 if strpos(x,"Yorkshire Regiment")>0 & strpos(x,"Batn")>0
`y' = 0 if x == "Yorkshire Regiment (W Riding)"
`y' = 2 if x == "Yorkshire Light Infantry" 
`y' = 0 if x == "Lancashire Regiment (16th Batn)"| x == "Lancashire Regiment (9th Batn)"

*******************************************************
* CLASSIFICATION SUMMARY
*******************************************************

gen pals = (pals_temp==1)
lab var pals "=1 Pals Battalion"

gen contains_pals = (pals_temp==2) /* i.e. not enough info, just regiment */
lab var contains_pals "=1 Regiment that contains some battalions that are Pals"

gen nolocal_pals = (pals_temp==3) 
lab var nolocal_pals "=1 Listed as Pals but no local raised battalions"

drop pals_temp

*******************************************************
save SCBattTypes.dta, replace

export delimited SCBattsTypes.csv
/* 
Total: 360 (listed battalions)
Pals: 66
Contains Pals: 57
Pals, No Local Batts Raised: 37
Other: 200

*/
