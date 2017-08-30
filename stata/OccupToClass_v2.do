* Melanie Wallskog
* 8/18/17

* This do-file runs the 1939-war records merged dataset through HISCLASS and HISCO

clear all
cd "E:\Dropbox\HistoryData\Data"

import delimited "SC1939FirstSampleJustOccup.csv"
count /* 3,556 observations */

save "FirstSample_start_v1.dta", replace
* Occupation_x is the 1939 occupation, 
* Occupation_y is the 1914/1915 occupation as stated at attestation
keep occupation_y
rename occupation_y occ
save "FirstSample_start1914_v1.dta", replace
use "FirstSample_start_v1.dta", clear
keep occupation_x
rename occupation_x occ
save "FirstSample_start1939_v1.dta", replace
append using "FirstSample_start1914_v1.dta"
save "FirstSample_start_v2.dta", replace
lab var occ "occupation"
gen counter = 1 
collapse (sum) counter, by(occ) 

gen occ_rev = "" 
lab var occ_rev "Revised occupation for improved HISCO matching"

* Revise occupations
gen revised = (occ_rev!="")

local w replace occ_rev /* save time typing */
`w' = "Assistant" if (strpos(occ,"Asst")>0 | strpos(occ,"Assnt")>0 | strpos(occ,"Assist")>0) & occ_rev==""
`w' = "Attendant" if occ == "Attendent"
`w' = "Porter" if (strpos(occ,"Porter")>0|strpos(occ,"Load")>0) & occ_rev==""
`w' = "Salesman" if strpos(occ,"Salesman")>0 & occ_rev ==""
`w' = "Storekeeper" if strpos(occ,"Store")>0 & occ_rev == ""
`w' = "Traindriver" if strpos(occ,"Train")>0 & strpos(occ,"Driver")>0 & occ_rev==""
`w' = "Tram conductor" if (strpos(occ,"Tram")>0 | occ=="Conductor") & occ_rev==""
`w' = "Driver" if strpos(occ,"Driver")>0 & occ_rev == ""
`w' = "Attendant" if strpos(occ,"Attendant")>0 & occ_rev == ""
`w' = "Bookseller" if occ=="Book Seller" | strpos(occ,"Librarian")>0 /* unsure */
`w' = "Brewer" if (strpos(occ,"Brewer")>0 | strpos(occ,"Beer")>0 ) & occ_rev == ""
`w' = "Builder" if strpos(occ,"Builder")>0 & occ_rev==""
`w' = "Omnibus driver" if strpos(occ,"Bus")>0 & occ_rev==""
`w' = "Wharfinger" if strpos(occ,"Wharf")>0 & occ_rev==""
`w' = "Tobacconist" if occ == "Tobaconist"
`w' = "Cashier" if (strpos(occ,"Cashier")>0 | strpos(occ,"Checker")>0) & occ_rev==""
`w' = "Banker" if occ == "Bank Official"| occ=="Financier"
`w' = "Artist" if occ == "Artiste" | (strpos(occ,"Actor")>0 & occ_rev=="")
`w' = "Grover" if occ == "Banana Inspector" /* unclear */
`w' = "Asylum attendant" if occ == "Asylum Attendent"
`w' = "Bargeman" if strpos(occ,"Barge")>0 & occ_rev==""
`w' = "Billposter" if occ=="Bill Poster"
`w' = "Manufacturer" if strpos(occ,"Manufacturer")>0 & occ_rev==""
`w' = "Bagmaker" if  occ=="Belt Maker" /*80310*/
`w' = "Boilermaker" if strpos(occ,"Boiler")>0 & occ_rev==""
`w' = "Bootmaker" if strpos(occ,"Boot")>0 & occ_rev==""
`w' = "Brass finisher" if occ=="Brass Polisher"
`w' = "Brass caster" if strpos(occ,"Brass")>0 & occ_rev==""
`w' = "Painter" if strpos(occ,"Painter")>0 & occ_rev==""
`w' = "Butcher" if (strpos(occ,"Butcher")>0 | strpos(occ,"Slaughter")>0) & occ_rev==""
`w' = "Cabinetmaker" if strpos(occ,"Cabinet")>0 & occ_rev==""
`w' = "Butter dealer" if strpos(occ,"Butter")>0 & occ_rev==""
`w' = "Carpenter" if (strpos(occ,"Carpenter")>0|strpos(occ,"Erector")>0|strpos(occ,"Frame")>0|strpos(occ,"Fence")>0) & occ_rev==""
`w' = "Mangling" if occ=="Carpetcleaner" | occ=="Carpet Cleaner"
`w' = "Chauffeur" if (strpos(occ,"Chauffeur")>0|strpos(occ,"Chauffuer")>0|occ=="Trucker") & occ_rev==""
`w' = "Polisher" if strpos(occ,"Polisher")>0 & occ_rev==""
`w' = "Metal smith" if (strpos(occ,"Metal")>0|occ=="Fetler") & occ_rev=="" /* latter is typo for fettler, I believ */
`w' = "City missionary" if strpos(occ,"Missionary") & occ_rev==""
`w' = "Traveller in millinery" if occ=="Millers Traveller"
`w' = "Miller" if (strpos(occ,"Mill")>0 | strpos(occ,"Rubber")>0) & occ_rev==""
`w' = "Milkman" if strpos(occ,"Milk")>0 & occ_rev==""
`w' = "Manufacturer" if strpos(occ,"Munitions")>0 & occ_rev=="" /* couln't find anything better*/
`w' = "Plumber" if (strpos(occ,"Plumb")>0|strpos(occ,"Sewer")>0) & occ_rev==""
`w' = "Farmer labourer" if strpos(occ,"Plough")>0 & occ_rev==""
`w' = "Clerk in post office" if occ=="Post Clerk"
`w' = "Professor of music" if strpos(occ,"Prof")>0 & strpos(occ,"Music")>0 & occ_rev==""
`w' = "Traffic foreman" if occ=="Road Foreman"
`w' = "Roadman" if strpos(occ,"Road")>0 & occ_rev==""
`w' = "Saddler" if occ=="Sadler"
`w' = "Salesman" if occ=="Salesmn"
`w' = "Teacher" if (strpos(occ,"School")>0|strpos(occ,"Instructor")>0|strpos(occ,"Teacher")>0|strpos(occ,"Techer")>0) & occ_rev==""
`w' = "Assistant in shop" if occ=="Shop Hand"
`w' = "Groom" if strpos(occ,"Stable")>0 & occ_rev==""
`w' = "Horsekeeper" if occ=="Stock Keeper" | occ=="Stockkeeper"
`w' = "Banker" if occ=="Stock Jobber" | occ=="Stockbroker"
`w' = "Superintendent of police" if (strpos(occ,"Superintendant")>0 | strpos(occ,"Supt")>0) & occ_rev==""
`w' = "Varnish maker" if strpos(occ,"Varnish")>0 & occ_rev=="" /* unclear */
`w' = "Book-keeper" if occ=="Book Keeper"
`w' = "Cellarman" if occ == "Cellerman"
`w' = "Waiter" if (strpos(occ,"Caterer")>0|strpos(occ,"Waiter")>0) & occ_rev=="" /* unclear */
`w' = "Caster" if strpos(occ,"Clay")>0 & occ_rev==""
`w' = "Coal setter" if occ=="Coal Loader Foreman" | occ=="Coal Manager" /* not sure how to better show skill */
`w' = "Coalheaver" if strpos(occ,"Coal")>0 & occ_rev==""
`w' = "Coffeehouse keeper" if strpos(occ,"Coffee")>0 & occ_rev==""
`w' = "Dealer" if (strpos(occ,"Buyer")>0 | strpos(occ,"Dealer")>0) & occ_rev==""
`w' = "Commission agent" if occ=="Commissionaire"
`w' = "Corn merchant" if strpos(occ,"Corn")>0 & occ_rev==""
`w' = "Customs official" if strpos(occ,"Customs")>0 & occ_rev==""
`w' = "Bicycle maker" if (strpos(occ,"Cycl")>0 | strpos(occ,"Bicycle")>0) & occ_rev==""
`w' = "Dentist" if strpos(occ,"Dental")>0 & occ_rev==""
`w' = "Plater" if occ=="Electro Plater"
`w' = "Chaser" if occ=="Embosser"
`w' = "Gasman" if (strpos(occ,"Distill")>0 | strpos(occ,"Draught")>0) & occ_rev==""
`w' = "Gardener" if occ=="Gardner"
`w' = "Gentleman's servant" if occ=="Gentlemans Servant"
`w' = "Greengrocer" if (strpos(occ,"Grocer")>0 | occ=="Greenman"|strpos(occ,"Greengrocer")>0) & occ_rev==""
`w' = "Horse driver" if occ=="Horsedriver"
`w' = "Horse dealer" if occ=="Horsedealer"
`w' = "Horsebreaker" if occ=="Horse Breaker"
`w' = "Horsekeeper" if occ=="Horse Keeper"
`w' = "Housekeeper" if occ=="House Keeper"
`w' = "Insurance agent" if strpos(occ,"Insurance")>0 & occ_rev==""
`w' = "Ostler" if strpos(occ,"Kennel")>0 & occ_rev==""
`w' = "Lamplighter" if strpos(occ,"Lamp")>0 & occ_rev==""
`w' = "Land agent" if strpos(occ,"Land")>0 & occ_rev==""
`w' = "Clothier" if strpos(occ,"Proprietor")>0 & occ_rev=="" /* stand-in for business proprietor */ 
`w' = "Miner" if (strpos(occ,"Lead ")>0|strpos(occ,"Mining")>0) & occ_rev=="" /* stone, not leader */
`w' = "Leather dresser" if strpos(occ,"Leather")>0 & occ_rev==""
`w' = "Brass finisher" if occ=="Machine Grinder" /* stand in for group */
`w' = "Machinist" if occ=="Machinst"
`w' = "Winder" if occ=="Machine Winder"
`w' = "Nurse" if strpos(occ,"Nurse")>0 & occ_rev==""
`w' = "Meat salesman" if strpos(occ,"Meat")>0 & occ_rev==""
`w' = "Newsagent" if (strpos(occ,"News")>0 | strpos(occ,"Advertising")>0) & occ_rev=="" /* unsure */
`w' = "Oil refiner" if strpos(occ,"Oil")>0 & occ_rev==""
`w' = "Piano forte maker" if (strpos(occ,"Piano")>0|strpos(occ,"Organ")>0) & occ_rev==""
`w' = "Policeman" if strpos(occ,"Police")>0 & occ_rev==""
`w' = "Cailico printer" if occ=="Photo Engraver"
`w' = "Paperhanger" if occ=="Paper Hanger"
`w' = "House carpenter" if strpos(occ,"Scaffold")>0 & occ_rev==""
`w' = "Printer" if occ=="Sign Writer" /* unsure */
`w' = "Tile maker" if strpos(occ,"Tile")>0 & occ_rev==""
`w' = "Wire cleaner" if strpos(occ,"Wire")>0 & occ_rev==""
`w' = "Carver" if strpos(occ,"Carver")>0 & occ_rev==""
`w' = "Woolsorter" if occ=="Wool Sorter"
`w' = "Wool salesman" if occ=="Wool Trader"
`w' = "Woolen factory worker" if strpos(occ,"Wool")>0 & occ_rev==""
`w' = "Mason" if occ=="Block Floorer"
`w' = "Messenger" if strpos(occ,"Messenger")>0 & occ_rev==""
`w' = "Bellows maker" if strpos(occ,"Billiard")>0 & occ_rev=="" /* stand in for group */
`w' = "Seedsman" if occ=="Botanist" /* unsure */
`w' = "Wine bottler" if strpos(occ,"Bottler")>0 & occ_rev==""
`w' = "Bellhanger" if strpos(occ,"Cable")>0 & occ_rev=="" /* stand in for group */
`w' = "Billposter" if (strpos(occ,"Caddie")>0|strpos(occ,"Caddy")>0|strpos(occ,"Golf")>0) & occ_rev=="" /* stand in for group */
`w' = "Baker" if strpos(occ,"Cake")>0 & occ_rev==""
`w' = "Cutter paper mill" if (strpos(occ,"Candle")>0|strpos(occ,"Cutter")>0) & occ_rev=="" /* stand in for group */
`w' = "Labourer" if strpos(occ,"Filler")>0 & occ_rev==""
`w' = "Chemist" if strpos(occ,"Chemical")>0 & occ_rev==""
`w' = "China dealer and Brazier" if strpos(occ,"China")>0 & occ_rev==""
`w' = "Toll collector" if (strpos(occ,"Cinema")>0|occ=="Box Office"|strpos(occ,"Film")>0) & occ_rev=="" /* stand in for group */
`w' = "Registrar of births" if strpos(occ,"Civil Service")>0 & occ_rev=="" /* stand in for group */
`w' = "Railway clerk" if occ=="Clerk Railway"
`w' = "Bed sacking manufacturer" if (strpos(occ,"Curtain")>0|strpos(occ,"Tarpaulin")>0) & occ_rev=="" /* stand in for group */
`w' = "Mangling" if (strpos(occ,"Cleaner")>0|strpos(occ,"Washer")>0) & occ_rev=="" /* stand in for group */
`w' = "Chemist and druggist" if strpos(occ,"Drugest")>0 & occ_rev==""
`w' = "Salt seller" if strpos(occ,"Salt")>0 & occ_rev==""
`w' = "Engineer" if strpos(occ,"Engineer")>0 & occ_rev==""
`w' = "Molecatcher" if (strpos(occ,"Errand")>0|strpos(occ,"Lift")>0) & occ_rev==""
`w' = "Engraver" if strpos(occ,"Etch")>0 & occ_rev==""
`w' = "Inspector" if occ=="Examiner"|occ=="Censor"
`w' = "Milliners apprentice" if strpos(occ,"Felt")>0 & occ_rev==""
`w' = "Fish salesman" if strpos(occ,"Fish")>0 & occ_rev==""
`w' = "Fitter" if strpos(occ,"Fitter")>0 & occ_rev==""
`w' = "Bed sacking manufacturer" if strpos(occ,"Furn")>0 & occ_rev =="" /* stand in for group */
`w' = "Gasworker" if strpos(occ,"Gas")>0 & occ_rev==""
`w' = "Glass drop cutter" if occ=="Glass Cutter"
`w' = "Glass sorter" if strpos(occ,"Glass")>0 & occ_rev=="" /* stand in for group */
`w' = "Groom" if strpos(occ,"Groom")>0 & occ_rev==""
`w' = "Rabbit catcher" if (strpos(occ,"Grounds")>0|strpos(occ,"Rounds")>0) & occ_rev=="" /* stand in for group */
`w' = "Hairdresser" if strpos(occ,"Hair")>0 & occ_rev==""
`w' = "Hammer man" if strpos(occ,"Hammer")>0 & occ_rev==""
`w' = "Leather dresser" if strpos(occ,"Hide")>0 & occ_rev==""
`w' = "Independent" if occ=="Independant" /* typo */
`w' = "Joiner" if strpos(occ,"Jointer")>0 & occ_rev=="" /* typo */
`w' = "Water purifier" if strpos(occ,"Purifier")>0 & occ_rev=="" /* unsure */
`w' = "Caster" if (strpos(occ,"Linotype")>0|strpos(occ,"Litho")>0|strpos(occ,"Ruler")>0|strpos(occ,"Printer")>0|strpos(occ,"Monotype")>0|strpos(occ,"Stereotype")>0|strpos(occ,"Typist")>0) & occ_rev==""
`w' = "Engine worker" if strpos(occ,"Greaser")>0 & occ_rev==""
`w' = "Operator in chain factory" if strpos(occ,"Operator")>0 & occ_rev=="" /* unsure */
`w' = "Dairyman" if occ=="Pasteuriser"
`w' = "Paviour" if occ=="Pavior" /* typo */
`w' = "Plater" if strpos(occ,"Plater")>0 & occ_rev==""
`w' = "Poultry keeper" if strpos(occ,"Poultry")>0 & occ_rev==""
`w' = "Estate agent" if strpos(occ,"Property")>0 & occ_rev==""
`w' = "Presser" if strpos(occ,"Press")>0 & occ_rev==""
`w' = "Provision merchant" if strpos(occ,"Provision")>0 & occ_rev==""
`w' = "Woolsorter" if strpos(occ,"Sorter")>0 & occ_rev=="" /* unsure */
`w' = "Registrar of births" if strpos(occ,"Registrar")>0 & occ_rev==""
`w' = "Scavenger" if occ=="Scavanger" /* typo */
`w' = "Sawyer" if strpos(occ,"Sawyer")>0 & occ_rev==""
`w' = "Tea dealer" if strpos(occ,"Tea")>0 & occ_rev==""
`w' = "Telegraph inspector" if (strpos(occ,"Telephon")>0|strpos(occ,"Despatch")>0) & occ_rev=="" /* stand in for group */
`w' = "Garden labourer" if occ=="Under Gardener"
`w' = "Artist (singer)" if occ=="Vocalist"
`w' = "Horse driver" if occ=="Jockey" /* unsure */
`w' = "Machine minder" if occ=="Machine Mender" /* typo */
`w' = "Colourmixer" if occ=="Mixer" /* unsure */
`w' = "Waggon repairer" if occ=="Repairer" /* unsure */
`w' = "Stocktaker" if occ=="Tallyman"
`w' = "Pawnbroker" if occ=="Ticket Writer" /* from http://www.iwm.org.uk/collections/item/object/80009535 */
`w' = "Lawyer's clerk" if occ=="Engrosser" /* https://books.google.com/books?id=cdMOAQAAIAAJ&pg=PA483&lpg=PA483&dq=%22engrosser%22+job+britain+1915&source=bl&ots=Y2hPHRACMp&sig=xQ2fp5Ogx5vfRhJdi4TX8yoAbXI&hl=en&sa=X&ved=0ahUKEwiskeCb-OjVAhVG92MKHWijC64Q6AEIRDAK#v=onepage&q=%22engrosser%22%20job%20britain%201915&f=false */
`w' = "Domestic servant" if occ=="Washhouseman" /* unsure */
`w' = "Shopkeeper" if occ=="Window Dresser" /* unsure */
`w' = "Boat owner" if occ=="Ship Broker"
`w' = "Water bailiff" if occ=="Turn Cock"
* General:
`w' = "Labourer" if (strpos(occ,"Labour")>0|strpos(occ,"Dig")>0|occ=="Lifter") & occ_rev==""
`w' = "Maker" if (strpos(occ,"Maker")>0|strpos(occ,"maker")>0) & occ_rev==""
`w' = "Assistant" if strpos(occ,"Hand")>0 & occ_rev=="" /* generalization */
`w' = "Worker" if strpos(occ,"Worker")>0 & occ_rev=="" /* generalization */
`w' = "Foreman" if (strpos(occ,"Foreman")>0|strpos(occ,"Ganger")>0) & occ_rev=="" /* generalization */
`w' = "General servant" if strpos(occ,"Servant")>0 & occ_rev==""
`w' = "Manager" if (strpos(occ,"Manager")>0|strpos(occ,"Trainer")>0) & occ_rev==""

`w' = "Nil/Unclear" if occ=="?"|occ=="Nil"|occ=="Snob"|occ=="Sca??monger?"|occ=="Vanguard"

`w' = "Foreman" if (strpos(occ,"Forem")>0|strpos(occ,"Foer")>0) & occ_rev==""
`w' = "Retired" if strpos(occ,"Retired")>0 | strpos(occ,"Former")>0
`w' = "Nil/Unclear" if strpos(occ,"Unemployed")>0 | strpos(occ,"Invalid")>0
`w' = "Accountant" if strpos(occ,"Accountant")>0 & occ_rev==""
`w' = "Artist" if strpos(occ,"Artist")>0 & occ_rev==""
`w' = "Gardener" if strpos(occ,"Garden")>0 & occ_rev==""
`w' = "Watchman" if strpos(occ,"Watchman")>0 & occ_rev==""
`w' = "Mechanic" if strpos(occ,"Mechanic")>0 & occ_rev==""
`w' = "Collector" if strpos(occ,"Collector")>0 & occ_rev==""
`w' = "Army pensioner" if strpos(occ,"Army Pensioner")>0 & occ_rev==""
`w' = "Needlework" if strpos(occ,"Needlework")>0 & occ_rev==""
`w' = "Insurance agent" if strpos(occ,"Assurance")>0 & occ_rev==""
`w' = "Auctioneer" if strpos(occ,"Auction")>0 & occ_rev==""
`w' = "Fireman" if strpos(occ,"Fire")>0 & occ_rev=="" /* 58110 */
`w' = "Baker" if strpos(occ,"Baker")>0 & occ_rev==""
`w' = "Grover" if (strpos(occ,"Banana")>0|strpos(occ,"Fruit")>0) & occ_rev=="" /* consistent with 1914 */
`w' = "Bank manager" if strpos(occ,"Bankmanager")>0 & occ_rev==""
`w' = "Banker" if strpos(occ,"Bank Officer")>0 & occ_rev==""
`w' = "Inspector" if strpos(occ,"Inspector")>0 & occ_rev==""
`w' = "Minister" if (strpos(occ,"Minister")>0 | strpos(occ,"Priest")>0 | strpos(occ,"Vicar")>0) & occ_rev=="" /* stand in for group */
`w' = "Barrister" if strpos(occ,"Barrister")>0 & occ_rev==""
`w' = "Metal smith" if strpos(occ,"Fettler")>0 & occ_rev=="" /* consistent with 1914 */
`w' = "Cellarman" if strpos(occ,"Cell")>0 & occ_rev==""
`w' = "Machine minder" if strpos(occ,"Machine Mind")>0 & occ_rev=="" /* consistent with 1914 */
`w' = "Boarding house keeper" if strpos(occ,"Boarding House")>0 & occ_rev==""
`w' = "Book stitcher" if (strpos(occ,"Book Binder")>0|strpos(occ,"Bookbuild")>0) & occ_rev==""
`w' = "Book-keeper" if strpos(occ,"Book Keeper")>0 & occ_rev==""
`w' = "Bookseller" if (strpos(occ,"Book")>0 & strpos(occ,"Publish")>0 | strpos(occ,"sel")>0) & occ_rev==""
`w' = "Caretaker" if (strpos(occ,"Caretake")>0|strpos(occ,"Hall Keep")>0|strpos(occ,"Street Orderly")>0) & occ_rev==""
`w' = "Bricklayer" if strpos(occ,"Brick")>0 & occ_rev==""
`w' = "Broker" if strpos(occ,"Broker")>0 & occ_rev==""
`w' = "Contractor" if strpos(occ,"Contractor")>0 & occ_rev==""
`w' = "Butler" if strpos(occ,"Butler")>0 & occ_rev==""
`w' = "Cashier" if strpos(occ,"Cahier")>0 & occ_rev=="" /* typo */
`w' = "Fringe manufacturer" if strpos(occ,"Canvas")>0 & occ_rev==""
`w' = "Carpenter" if occ=="Capenter" /* typo */
`w' = "Waiter" if (strpos(occ,"Cater")>0|strpos(occ,"Restaurant")>0) & occ_rev=="" /* consistent with 1914 */
`w' = "Drover" if strpos(occ,"Drover")>0 & occ_rev==""
`w' = "Collector" if strpos(occ,"Collector")>0 & occ_rev==""
`w' = "Chauffeur" if occ=="Chaffeur" | occ=="Chanffeur"/* typo */
`w' = "Architect" if strpos(occ,"Architect")>0 & occ_rev==""
`w' = "Secretary" if strpos(occ,"Secretary")>0 & occ_rev==""
`w' = "Chemist and druggist" if (strpos(occ,"Dispenser")>0 | strpos(occ,"Sundries")>0) & occ_rev==""
`w' = "Doctor" if (strpos(occ,"Med")>0|strpos(occ,"Physician")>0) & occ_rev==""
`w' = "Verger" if strpos(occ,"Verger")>0 & occ_rev==""
`w' = "Steward" if strpos(occ,"Steward")>0 & occ_rev==""
`w' = "Shoe dealer" if strpos(occ,"Shoe Trade")>0 & occ_rev==""
`w' = "Coach trimmer" if strpos(occ,"Coach Trimmer")>0 & occ_rev==""
`w' = "Guard" if strpos(occ,"guard")>0 & occ_rev==""
`w' = "Electrician" if (strpos(occ,"Electri")>0|strpos(occ,"Coke")>0) & occ_rev==""
`w' = "Colliery agent" if strpos(occ,"Colliery")>0 & strpos(occ,"Clerk")==0 & occ_rev==""
`w' = "Commercial traveller" if (strpos(occ,"Commercial Travel")>0|strpos(occ,"Commercail Travel")>0) & occ_rev==""
`w' = "Commission agent" if strpos(occ,"Commission Agent")>0 & occ_rev==""
`w' = "Compositor" if strpos(occ,"Compositor")>0 & occ_rev==""
`w' = "Drainer" if strpos(occ,"Concrete")>0 & occ_rev==""
`w' = "Tram conductor" if strpos(occ,"Conductor")>0 & occ_rev==""
`w' = "Tobacconist" if strpos(occ,"Tobacco")>0 & occ_rev==""
`w' = "Biscuit maker" if strpos(occ,"Confection")>0 & occ_rev=="" /* stand in for group */
`w' = "Cook" if (strpos(occ,"Cook")>0 | strpos(occ,"Chef")>0)  & occ_rev==""
`w' = "Optician" if strpos(occ,"Optician")>0  & occ_rev==""
`w' = "Tanner" if strpos(occ,"Lesther")>0  & occ_rev=="" /* typo */
`w' = "Cotton factory weaver" if (strpos(occ,"Cotton Loom")>0|strpos(occ,"Spin")>0) & occ_rev==""
`w' = "Cowman" if strpos(occ,"Cowman")>0 & occ_rev==""
`w' = "Crane driver" if strpos(occ,"Crane")>0 & occ_rev==""
`w' = "Dairyman" if strpos(occ,"Dairy")>0 & occ_rev==""
`w' = "Decorator" if strpos(occ,"Decorator")>0 & occ_rev==""
`w' = "Draper" if strpos(occ,"Draper")>0 & strpos(occ,"Credit")==0 & occ_rev==""
`w' = "Grocer" if (strpos(occ,"Egg")>0 | strpos(occ,"Groc")>0) & occ_rev==""
`w' = "Plater" if strpos(occ,"Plate")>0 & occ_rev==""
`w' = "Engraver" if strpos(occ,"Engraver")>0 & occ_rev==""
`w' = "Policeman" if strpos(occ,"Enquiry Agent")>0  & occ_rev=="" /* private eye, proxy */
`w' = "Postman" if (strpos(occ,"Postman")>0|strpos(occ,"Post  Man")>0)  & occ_rev==""
`w' = "Estate agent" if strpos(occ,"Estate")>0 & occ_rev==""
`w' = "Export packer" if strpos(occ,"Export Pack")>0 & occ_rev==""
`w' = "Gatekeeper" if strpos(occ,"Gate")>0 & occ_rev==""
`w' = "Timekeeper" if (strpos(occ,"Time Keep")>0|strpos(occ,"Timekeep")>0) & occ_rev==""
`w' = "Warehouseman" if (strpos(occ,"Warehouse")>0|strpos(occ,"Wharehouseman")>0) & occ_rev==""
`w' = "Farm servant" if occ=="Farm Carter"
`w' = "Farmer" if strpos(occ,"Farmer")>0 & occ_rev==""
`w' = "Dairy keeper" if occ=="Farmerdairy"
`w' = "Packer" if strpos(occ,"Pack")>0  & occ_rev==""
`w' = "Florist" if strpos(occ,"Flower Seller")>0 & occ_rev==""
`w' = "Undertaker" if strpos(occ,"Funeral")>0 & occ_rev==""
`w' = "Furrier" if strpos(occ,"Furrier")>0 & occ_rev==""
`w' = "Telegraph inspector" if (strpos(occ,"Telec")>0|strpos(occ,"Teleg")>0) & occ_rev=="" /* stand in for line */
`w' = "Builder" if strpos(occ,"Garage")>0 & occ_rev=="" /* unsure */
`w' = "Gardener" if strpos(occ,"Gardner")>0 & occ_rev=="" /* typo */
`w' = "General labourer" if strpos(occ,"General")>0 & strpos(occ,"Labo")>0 & occ_rev==""
`w' = "Hairdresser" if (strpos(occ,"Hairdresser")>0|strpos(occ,"Haid")>0) & occ_rev==""
`w' = "Tailor" if strpos(occ,"Tailor")>0 & occ_rev==""
`w' = "Colliery agent" if strpos(occ,"Goods Agent")>0 & occ_rev=="" /* stand in for group */
`w' = "Greengrocer" if strpos(occ,"Green")>0 & occ_rev==""
`w' = "Hawker" if strpos(occ,"Hawk")>0 & occ_rev==""
`w' = "Turner" if strpos(occ,"Turner")>0 & occ_rev==""
`w' = "Horseman" if strpos(occ,"Horse")>0 & occ_rev==""
`w' = "Hotel servant" if strpos(occ,"Hotel")>0 & occ_rev==""
`w' = "House decorator" if occ=="House Docorator" /* typo */
`w' = "House carpenter" if (strpos(occ,"Properly Repairer")>0|strpos(occ,"House Repair")>0) & occ_rev=="" /* typo */
`w' = "House agent" if strpos(occ,"House Det")>0 & occ_rev=="" /* unsure */
`w' = "House servant" if strpos(occ,"House") & strpos(occ,"Domestic") & occ_rev==""
`w' = "Housekeeper" if strpos(occ,"Housekeeper")>0 & occ_rev==""
`w' = "Watchman" if occ== "Houseman Museum" /* unsure */
`w' = "Innkeeper" if strpos(occ,"Inn")>0 & occ_rev==""
`w' = "Ironmonger" if strpos(occ,"Ironmo")>0 & occ_rev==""
`w' = "Joiner" if strpos(occ,"Joiner")>0 & occ_rev==""
`w' = "Railway inspector" if strpos(occ,"Train Reg")>0 & occ_rev==""
`w' = "Hosier" if strpos(occ,"Hosier")>0 & occ_rev==""
`w' = "Laundryman" if strpos(occ,"Laundry")>0 & occ_rev==""
`w' = "Lawyer" if occ=="Law Writer"|occ=="Solicitors" /* unsure */
`w' = "Lawyer's clerk" if occ=="Law &amp; Com Stationer" /* unsure */
`w' = "Railwayman" if (strpos(occ,"Railway")>0|strpos(occ,"Length Man")>0) & occ_rev==""
`w' = "Caster" if occ=="Letter Process Machine"|strpos(occ,"Moonotype")>0|((strpos(occ,"Printing")>0|strpos(occ,"Type")>0)&occ_rev=="") /* unsure, trying to be consistent with 1914 */
`w' = "Licensed victualler" if strpos(occ,"Victual")>0 & occ_rev==""
`w' = "Lighterman" if strpos(occ,"Lighter")>0  & occ_rev==""
`w' = "Carpet planner" if strpos(occ,"Carpet Plan")>0 & occ_rev==""
`w' = "Registrar of births" if (strpos(occ,"Local Gov")>0|strpos(occ,"County Council")>0|strpos(occ,"Birth")>0|strpos(occ,"Civil Serv")>0)  & occ_rev=="" /* stand in for group, consistent with 1914 */
`w' = "Locomotive engineer" if strpos(occ,"Locomotive Eng")>0 & occ_rev==""
`w' = "Chauffeur" if strpos(occ,"Lorry")>0  & occ_rev=="" /* consistent with 1914 */
`w' = "Machinist" if strpos(occ,"Machinist")>0 & occ_rev=="" /* 83410 */
`w' = "Refiner" if strpos(occ,"Refine")>0  & occ_rev==""
`w' = "Newsagent" if (strpos(occ,"Market Research")>0|strpos(occ,"Advert")>0) & occ_rev=="" /* unsure, consistent with 1914 */
`w' = "Blacksmith" if strpos(occ,"Blacksmith")>0 & occ_rev==""
`w' = "Master mariner" if strpos(occ,"Master Mariner")>0 & occ_rev==""
`w' = "Boot and shoemaker" if strpos(occ,"Shoe")>0 & occ_rev==""
`w' = "Boat unloader" if strpos(occ,"Stevedore")>0 & occ_rev==""
`w' = "Cap maker" if strpos(occ,"Cap Man")>0 & occ_rev==""
`w' = "Ovenman" if strpos(occ,"Oven Man")>0 & occ_rev==""
`w' = "Broker" if (strpos(occ,"Stock Exch")>0|strpos(occ,"Exchange Stock")>0) & occ_rev==""
`w' = "Omnibus driver" if strpos(occ,"Omnibus")>0 & occ_rev==""
`w' = "Paperhanger" if (strpos(occ,"Paper Hanger")>0|strpos(occ,"Paper Langer")>0) & occ_rev==""
`w' = "Rabbit catcher" if strpos(occ,"Park")>0 & occ_rev=="" /* stand in for group, consistent with 1914 */
`w' = "Railwayman" if strpos(occ,"Permanent Way")>0 & occ_rev=="" /* comapany(?) */
`w' = "Planer" if strpos(occ,"Plan Man")>0 & occ_rev=="" /* typo(?) */
`w' = "Plasterer" if strpos(occ,"Plasterer")>0 & occ_rev==""
`w' = "Office cleaner" if strpos(occ,"Office Clean")>0 & occ_rev==""
`w' = "Engraver" if strpos(occ,"Engraving")>0 & occ_rev==""
`w' = "Artist (singer)" if strpos(occ,"Vocalist")>0 & occ_rev==""
`w' = "Photographer" if strpos(occ,"Photograph")>0 & occ_rev==""
`w' = "Publican" if strpos(occ,"Publician")>0 & occ_rev=="" /* typo*/
`w' = "Stocktaker" if (strpos(occ,"Quantity")>0|strpos(occ,"Record Keeper")>0|strpos(occ,"Stock Keeper")>0) & occ_rev==""
`w' = "Driller" if strpos(occ,"Driller")>0 & occ_rev==""
`w' = "Dentist" if strpos(occ,"Dentist")>0 & occ_rev==""
`w' = "Secretary" if (strpos(occ,"Shorthand")>0|strpos(occ,"Secty")>0) & occ_rev==""
`w' = "Shipwright" if strpos(occ,"Shipwright")>0 & occ_rev==""
`w' = "Shopkeeper" if strpos(occ,"Shop Keep")>0 & occ_rev==""
`w' = "Skinner" if strpos(occ,"Skin")>0 & occ_rev==""
`w' = "Stationmaster" if strpos(occ,"Station Master")>0 & occ_rev==""
`w' = "Stoker" if (strpos(occ,"Stoker")>0|strpos(occ,"Soker")>0) & occ_rev==""
`w' = "Brass caster" if strpos(occ,"Steel Mould")>0 & occ_rev=="" /* consistent with 1914 */
`w' = "Broker" if strpos(occ,"broker")>0 & occ_rev==""
`w' = "Mason" if strpos(occ,"Stone")>0 & occ_rev==""
`w' = "Sweep" if strpos(occ,"Sweeper")>0 & occ_rev==""
`w' = "Surveyor" if strpos(occ,"Surveyor")>0 & occ_rev==""
`w' = "Yardman" if strpos(occ,"Yard Man")>0 & occ_rev==""
`w' = "Waggon repairer" if strpos(occ,"Waggon Repair")>0 & occ_rev==""
`w' = "Tool setter" if (strpos(occ,"Machine Tool")>0 | strpos(occ,"Tool Setter")>0) & occ_rev==""
`w' = "Jeweller" if strpos(occ,"Jeweller")>0 & occ_rev==""
`w' = "Watchmaker" if strpos(occ,"Watch")>0 & strpos(occ,"Clock")>0 & occ_rev==""
`w' = "Warrant Officer" if strpos(occ,"Warrant")>0 & occ_rev==""
`w' = "Farmer labourer" if strpos(occ,"Farm Jober")>0 & occ_rev==""
`w' = "Vanman" if strpos(occ,"Van")>0 & occ_rev=="" /* unsure */
`w' = "Upholsterer" if strpos(occ,"Upholster")>0 & occ_rev==""
`w' = "Domestic" if strpos(occ,"Domestic")>0 & occ_rev==""
`w' = "Banker" if strpos(occ,"Auditor")>0 & occ_rev==""
`w' = "Greengrocer" if (strpos(occ,"Food")>0|strpos(occ,"Bacon")>0) & occ_rev==""
`w' = "Wine merchant" if strpos(occ,"Wine")>0 & occ_rev==""
`w' = "Instrument maker" if strpos(occ,"Optical")>0  & occ_rev==""
`w' = "Accountant" if (strpos(occ,"Accountant")>0|strpos(occ,"Accoutant")>0) & occ_rev==""
`w' = "Roller" if strpos(occ,"Roller")>0 & occ_rev==""
`w' = "Timber dealer" if strpos(occ,"Timber")>0 & occ_rev==""
`w' = "Cailico printer" if strpos(occ,"Designer")>0 & occ_rev==""
`w' = "Bleacher" if occ=="Textile Chemist" /* unsure */
`w' = "Clothier" if (strpos(occ,"Coat")>0|strpos(occ,"Fashion")>0|strpos(occ,"Gown")>0|strpos(occ,"Textil")>0) & occ_rev==""
`w' = "Butcher" if strpos(occ,"Taxiderm")>0 & occ_rev=="" /* unsure */
`w' = "Artist" if strpos(occ,"Art ")>0 & occ_rev==""
`w' = "Caster" if strpos(occ,"Automatic")>0 & occ_rev=="" /* unsure */
`w' = "Colour maker" if strpos(occ,"Colour")>0 & occ_rev=="" 
`w' = "Artist" if strpos(occ,"Comedian")>0 & occ_rev=="" 
`w' = "Civil engineer" if strpos(occ,"Constructional Eng")>0 & occ_rev=="" 
`w' = "Pawnbroker" if strpos(occ,"Credit")>0 & occ_rev=="" /* unsure, proxy */
`w' = "Glazier" if strpos(occ,"Glazier")>0 & occ_rev=="" 
`w' = "Journalist" if strpos(occ,"B B C")>0 & occ_rev=="" /* unsure, proxy */
`w' = "Fitter" if occ=="Revitter" /* unsure, typo */
`w' = "Rivetter" if strpos(occ,"Rivet")>0 & occ_rev=="" 
`w' = "Slater" if strpos(occ,"Slater")>0 & occ_rev=="" 
`w' = "Wood sawyer" if strpos(occ,"Wood Scourer")>0 & occ_rev=="" /* unsure */
`w' = "Relieving officer" if strpos(occ,"Welfare")>0 & occ_rev=="" /* unsure */
`w' = "Glass sorter" if strpos(occ,"Annealer")>0 & occ_rev=="" /* unsure, stands in for group */

`w' = "Bank clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"Bank")>0 & occ_rev==""
`w' = "Colliery clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"Colliery")>0 & occ_rev==""
`w' = "General clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"General")>0 & occ_rev==""
`w' = "Lawyer's clerk" if strpos(occ,"Clerk")>0 & (strpos(occ,"Law")>0|strpos(occ,"Solicit")>0) & occ_rev==""
`w' = "Mercantile clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"Mercantile")>0 & occ_rev==""
`w' = "Merchant's clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"Merchant")>0 & occ_rev==""
`w' = "Parish clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"Parish")>0 & occ_rev==""
`w' = "Postal clerk" if ((strpos(occ,"Clerk")>0 & strpos(occ,"Post")>0)|strpos(occ,"Auxiliary Postman")>0|strpos(occ,"General Post")>0|strpos(occ,"Overse")>0) & occ_rev==""
`w' = "Telegraph clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"Tele")>0 & occ_rev==""
`w' = "Railway clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"Railway")>0 & occ_rev==""
`w' = "Commercial clerk" if strpos(occ,"Clerk")>0 & strpos(occ,"Commercial")>0 & occ_rev==""
`w' = "Clerk" if (strpos(occ,"Clerk")>0|strpos(occ,"Cleric")>0) & occ_rev=="" /* large group */
`w' = "Clerk" if occ=="Paint Mnfrs Chief Order Cler" | occ=="Shipping Cler" | occ=="Mp Courts Ass Cler"

`w' = "Commerical clerk" if strpos(occ,"Commercial")>0 & occ_rev=="" 
`w' = "Merchant" if strpos(occ,"Merchant")>0 & occ_rev==""
`w' = "Manager" if (strpos(occ,"Sup")>0|strpos(occ,"Director")>0) & occ_rev==""
`w' = "Army officer" if (strpos(occ,"R A F")>0|strpos(occ,"Army")>0|strpos(occ,"Regt")>0|strpos(occ,"Air Ministry")>0|strpos(occ,"Navy")>0|strpos(occ,"Ry")>0) & occ_rev==""
`w' = "Labourer" if (strpos(occ,"Labouer")>0 | strpos(occ,"Laborer")>0 | strpos(occ,"Labr")>0) & occ_rev=="" /* typo*/
`w' = "Labourer" if strpos(occ,"Heavy")>0 & occ_rev==""
`w' = "Traveller" if strpos(occ,"Trav")>0 & occ_rev==""
`w' = "Assistant" if strpos(occ,"Han")>0 & occ_rev=="" /* generalization, consistent with 1914 */

`w' = "Army pensioner" if strpos(occ,"Pension")>0 & (strpos(occ,"Soldier")>0 | strpos(occ,"Army")>0) & occ_rev==""
`w' = "Pensioner" if strpos(occ,"Pensioner")>0  & occ_rev==""
`w' = "Domestic duties" if strpos(occ,"Domestic Dutie")>0  & occ_rev==""
`w' = "Nil/Unclear" if (strpos(occ,"Blind")>0|strpos(occ,"Disabled")>0|strpos(occ,"Incapacit")>0|strpos(occ,"Lunatic")>0| /// 
	strpos(occ,"Male")>0| strpos(occ,"Man Ages")>0|strpos(occ,"Old Age")>0|strpos(occ,"Paper")>0 ///
	| strpos(occ,"Pickress")>0|strpos(occ,"Private Means")>0|strpos(occ,"Ra")>0|strpos(occ,"Wholesale")>0 ///
	| strpos(occ,"Unknown")>0 | strpos(occ,"Disability")>0 | strpos(occ,"Casual")>0 | strpos(occ,"Caury")>0 ///
	| strpos(occ,"Centering")>0 | strpos(occ,"Chain")>0 | strpos(occ,"Wands")>0 | strpos(occ,"Coin")>0 ///
	| strpos(occ,"Goverment Pay")>0|strpos(occ,"Laterer")>0|strpos(occ,"Seeking")>0 | strpos(occ,"Small")>0 ///
	| strpos(occ,"French")>0 | strpos(occ,"Sub")>0 | strpos(occ,"rotection")>0) & occ_rev==""
`w' = "Lawyer" if strpos(occ,"Law")>0 & occ_rev==""
	
replace occ_rev = occ if occ_rev=="" /* do not need to be revised */
gen matched = (occ_rev==occ)

replace occ_rev = "Nil/Unclear" if occ==""

save "hiscoALL_v2.dta", replace

* first, collapse to speed up matching process
collapse (first) occ, by(occ_rev) /* 345 unique */

export delimited "occupALL_v1.csv", replace

* Run through HISCO website

clear
import delimited "hiscoALL_v1.csv"
drop if _n==1 /* headers didn't import */
keep v1 v3 v7 

rename v1 hisco_occ
rename v3 hisco_code
rename v7 occ_rev

* get rid of quotes
replace hisco_code = subinstr(hisco_code, `"""',  "", .)
replace occ = subinstr(occ,`"""',"",.)
replace hisco_occ = subinstr(hisco_occ,`"""',"",.)
* get rid of first space
replace occ = substr(occ,2,length(occ))

rename hisco_code hisco
destring hisco, replace

* Convert HISCO (occupation code) to HISCLASS (social class code)
do recode_v1.do

replace hisco_occ = "Nil/Unclear"_ if occ=="nil/unclear"
replace hisco = -1 if hisco_occ=="Nil/Unclear"

*collapse (mean) hisclass, by(occ_rev)

save "hisclassALL_v1.dta", replace 

* merge back in
merge 1:m occ_rev using "hiscoALL_v2.dta"

drop _merge hisco_occ revised

rename occ occupation_y /* for 1914 */

save "hisclassALL_v2.dta", replace

clear
import delimited "SC1939FirstSampleJustOccup.csv"

merge m:1 occupation_y using "hisclassALL_v2.dta"

rename hisclass hisclass_1914
rename hisco hisco_1914
rename occ_rev occ_rev_1914

keep if _merge==3

save "FirstSample_1914hisclass.dta", replace
export delimited "FirstSample_1914hisclass.csv", replace

clear

use "hisclassALL_v2.dta"

rename occupation_y occupation_x /* for 1939 */

collapse (first) hisco occ_rev hisclass, by(occupation_x)

save "hisclassALL_v3.dta", replace

clear
* merge into full sample, with 1914 already done
import delimited "FirstSample_1914hisclass.csv"

merge m:1 occupation_x using "hisclassALL_v3.dta", gen(_merge2)

rename hisclass hisclass_1939
rename hisco hisco_1939
rename occ_rev occ_rev_1939

keep if _merge2==3

drop counter matched
replace hisclass_1939 = -1 if occ_rev_1939=="Nil/Unclear"
replace hisclass_1914 = -1 if occ_rev_1914=="Nil/Unclear"


save "FirstSample_ALLhisclass.dta", replace
export delimited "FirstSample_ALLhisclass.csv", replace






