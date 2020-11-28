from flask import Flask, jsonify, request


import math
import re, string
from collections import Counter


corpus = [
    "who is the CEO??",
    "how to block a ATM card?",
    "savings bank pass book for minor account?",
    "How much cash can be deposited in Cash Recycler?",
    "want to deposit cash through cash deposit machine, tell me the charge",
    "cash deposit failed at CR",
    "what should I do if my credit card payment fails",
    "I have sent money but the transaction failed and my account is debited. What should I do?",
    "How to call customer care",
    "i want to know why the toll free number is not responding",
    "how many no of transactions i have done?",
    "can a bank account be opened using an Aadhaar card?",
    "how many aadhaar registration are done per day in aec or branch?",
    "at what time aadhaar enrollment can be done?",
    "charges for aadhar enrolment",
    "how can i change my mobile number",
    "can you tell Address updation process?",
    "online updation of address in adhaar",
    "How to contact you?",
    "introduction is necessary when i open account?",
    "without any proof of identity can i still open a bank account?",
    "minimum balance to maintain bank account",
    "What is UPI?",
    "Difference between VPA and UPI ID?",
    "Can we use the same PIN for all apps?",
    "Full form of dtaa?",
    "I have sent money but the transaction failed and my account is debited. What should I do?",
    "type of transactions done online",
    "neft transaction limit with OTP",
    "NEFT/RTGS transaction limit",
    "what is the transaction limit for walk in customer",
    "Can the transaction limit increase as per customer request in UPI transaction?",
    "UPI transaction limit?",
    "CEO ఎవరు ??",
    "ఎటిఎం కార్డును ఎలా బ్లాక్ చేయాలి",
    "మైనర్ ఖాతా కోసం సేవింగ్స్ బ్యాంక్ పాస్ బుక్?",
    "నగదు రీసైక్లర్‌లో ఎంత నగదు జమ చేయవచ్చు?",
    "నగదు డిపాజిట్ మెషిన్ ద్వారా నగదు జమ చేయాలనుకుంటున్నాను, ఛార్జ్ చెప్పండి",
    "CR వద్ద నగదు డిపాజిట్ విఫలమైంది",
    "నా క్రెడిట్ కార్డ్ చెల్లింపు విఫలమైతే నేను ఏమి చేయాలి",
    "నేను డబ్బు పంపించాను కాని లావాదేవీ విఫలమైంది మరియు నా ఖాతా డెబిట్ చేయబడింది. నేను ఏమి చేయాలి?",
    "కస్టమర్ కేర్‌ను ఎలా పిలవాలి",
    "టోల్ ఫ్రీ నంబర్ ఎందుకు స్పందించడం లేదని నేను తెలుసుకోవాలనుకుంటున్నాను",
    "నేను ఎన్ని లావాదేవీలు చేయలేదు?",
    "ఆధార్ కార్డు ఉపయోగించి బ్యాంక్ ఖాతా తెరవగలరా?",
    "ఏసి లేదా బ్రాంచ్‌లో రోజుకు ఎన్ని ఆధార్ రిజిస్ట్రేషన్ చేస్తారు?",
    "ఏ సమయంలో ఆధార్ నమోదు చేయవచ్చు?",
    "ఆధార్ నమోదు కోసం ఛార్జీలు",
    "నేను నా మొబైల్ నంబర్‌ను ఎలా మార్చగలను",
    "చిరునామా నవీకరణ ప్రక్రియను మీరు చెప్పగలరా?",
    "ఆన్‌లైన్‌లో చిరునామా నవీకరణ",
    "మిమ్మల్ని ఎలా సంప్రదించాలి?",
    "నేను ఖాతా తెరిచినప్పుడు పరిచయం అవసరం?",
    "గుర్తింపు యొక్క రుజువు లేకుండా నేను ఇప్పటికీ బ్యాంకు ఖాతాను తెరవగలనా?",
    "ఖాతా యొక్క ఆపరేషన్.త్రైమాసిక సగటు బ్యాలెన్స్ నిర్వహించకపోతే బ్యాంక్ ఖాతాను నిర్వహించడానికి కనీస బ్యాలెన్స్",
    "యుపిఐ అంటే ఏమిటి?",
    "VPA మరియు UPI ID ల మధ్య వ్యత్యాసం?",
    "మేము అన్ని అనువర్తనాల కోసం ఒకే పిన్ను ఉపయోగించవచ్చా?",
    "Dtaa యొక్క పూర్తి రూపం?",
    "నేను డబ్బు పంపించాను కాని లావాదేవీ విఫలమైంది మరియు నా ఖాతా డెబిట్ చేయబడింది. నేను ఏమి చేయాలి?",
    "ఆన్‌లైన్‌లో చేసిన లావాదేవీల రకం",
    "OTP తో నెఫ్ట్ లావాదేవీ పరిమితి",
    "NEFT / RTGS లావాదేవీ పరిమితి",
    "కస్టమర్లో నడవడానికి లావాదేవీ పరిమితి ఏమిటి",
    "యుపిఐ లావాదేవీలో కస్టమర్ అభ్యర్థన ప్రకారం లావాదేవీల పరిమితి పెరుగుతుందా?",
    "యుపిఐ లావాదేవీ పరిమితి?",
    "CEO कौन है ??",
    "एटीएम कार्ड को कैसे ब्लॉक किया जा सकता है?",
    "मामूली खाते के लिए बचत बैंक पास बुक?",
    "कैश रिसाइकलर में कितना कैश जमा किया जा सकता है?",
    "कैश डिपॉजिट मशीन के माध्यम से कैश जमा करना चाहते हैं, मुझे चार्ज बताएं",
    "CR पर कैश डिपॉजिट विफल रहा।",
    "यदि मेरा क्रेडिट कार्ड भुगतान विफल हो जाता है तो मुझे क्या करना चाहिए",
    "मैंने पैसे भेजे हैं लेकिन लेनदेन विफल हो गया है और मेरा खाता डेबिट हो गया है। मुझे क्या करना चाहिए?",
    "कस्टमर केयर पर कॉल कैसे करें",
    "मैं जानना चाहता हूं कि टोल फ्री नंबर का जवाब क्यों नहीं दिया जा रहा है",
    "मैंने कितने लेन-देन किए हैं?",
    "क्या आधार कार्ड का उपयोग करके बैंक खाता खोला जा सकता है?",
    "aec या शाखा में प्रतिदिन कितने आधार पंजीकरण किए जाते हैं?",
    "किस समय आधार नामांकन किया जा सकता है?",
    "आधार नामांकन के लिए शुल्क",
    "मैं अपना मोबाइल नंबर कैसे बदल सकता हूं",
    "क्या आप पता अपडेशन प्रक्रिया बता सकते हैं?",
    "आधार में पते का ऑनलाइन अपडेशन",
    "आपसे कैसे संपर्क करें?",
    "खाता खोलते समय परिचय आवश्यक है?",
    "पहचान के किसी भी सबूत के बिना मैं अभी भी एक बैंक खाता खोल सकता हूं?",
    "बैंक खाते को बनाए रखने के लिए न्यूनतम शेष",
    "UPI क्या है?",
    "वीपीए और यूपीआई आईडी के बीच अंतर?",
    "क्या हम सभी ऐप्स के लिए एक ही पिन का उपयोग कर सकते हैं?",
    "DtaA का पूर्ण रूप?",
    "मैंने पैसे भेजे हैं लेकिन लेनदेन विफल हो गया है और मेरा खाता डेबिट हो गया है। मुझे क्या करना चाहिए?",
    "ऑनलाइन किए गए लेन-देन के प्रकार",
    "ओटीपी",
    "एनईएफटी / आरटीजीएस लेनदेन सीमा",
    "ग्राहक में वॉक के लिए लेन-देन की सीमा क्या है",
    "क्या UPI लेन-देन में ग्राहक के अनुरोध के अनुसार लेनदेन की सीमा बढ़ सकती है?",
    "UPI लेनदेन की सीमा?"
]

answers = [
    "Mr.Swamy Vinay",
    "Debit card can be blocked as below Through SMS:SMS syntax for blocking ATM/Debit Card: CARDBLOCK<SPACE>XXXX (XXXXLast four digits of A/c No.) to 56161",
    "Exclusive Savings Bank Pass Book designed for Minor accounts only should be issued with Photo affixed on it.",
    "Cash can be deposited for a day, up to Rs.2 lacs where the account is linked to PAN and Rs.49950/- where the account is not linked to PAN.",
    "No charges lieved on customer for depositing cash in Cash recycler/ Deposit Machine.",
    "Visit the Branch where the BNA/CR is linked for Clarification.",
    "Please mail the transaction details to email.",
    "I can help you with that! The transaction may have failed due to a system error.Your transaction ID is your reference ID, which you can take up with us in our toll free number XXXXXXXXXX.",
    "Please contact our toll free number XXXXXXXXXX",
    "Sometimes many users will be trying for the toll free number/customer care number at the same time due to which number becomes busy/Not reachable.In such cases we request you to please try to connect after few minutes.",
    "There is no limit on number of transactions.",
    "Aadhaar card is accepted as a proof of both identity and address.",
    "It depends upon the connectivity with server.",
    "Branch business hours-where the center is running.",
    "For Aadhaar biometric/ Demograhic  modification/Updation Rs. 50/- (including GST).",
    "I can help you with that!.You can update your mobile number through: a)Branch b)ATM.Please Note: If you are having Corporate Internet Banking Mobile Number can be updated by visiting your home branch only.",
    "YOU NEED To APPROACH NEAR BY BANK BRANCH.",
    "Address updation in Aadhaar is possible online - for more details please visit:-  www.uidai.gov.in   *The registered mobile number is essential to avail this service.",
    "Please contact :XXXXXXXXXX or go to Nearest Bank.",
    "No, introduction is not required.",
    "You can still open a bank account known as Small Account by submitting your recent photograph and putting your signature or thumb impression in the presence of the bank official subject to certain restrictions in operation of account.",
    "Rs.200/- will be levied, if quarterly average balance is not maintained.",
    "Any individual having a smartphone and bank account is eligible to use UPI. That being said, you need your mobile number registered with the bank and a debit card linked to that account. You can download the app from playstore or appstore.",
    "A UPI ID or VPA (Virtual Payment Address) is a unique identifier which you can use to send and receive money on UPI.Think of it as an unique ID which you can use to transfer money.",
    "User can use the same PIN created for their bank accounts across all UPI apps.",
    "DTAA is Double Tax Avoidance Agreement.",
    "I can help you with that! The transaction may have failed due to a system error.Your transaction ID is your reference ID,which you can take up with us in our toll free number 1800 425 1515.",
    "I can help you with that!Below mentioned type of transactions can be made through Internet Banking  :- Retail/Individual users can do the Fund Transfer or Payment to : 1.) Own Account,2.) Other Andhra Bank account ,3.) Neft/RTGS /IMPS,4.)Own PPF account,5.) Other Andhra Bank PPF account ,6.) Tax payment. Corporate/Non Individual users can do Fund Transfer or Payment to :1.)Own Account,2.)Other Andhra Bank account ,3.) Neft/RTGS/IMPS,4.)Bulk Neft,5.)Tax payment.",
    "Yes, this facility is available in Internet Banking for retail users. They can do transactions upto Rs.50,000/-  with only OTP.",
    "Transaction limit for NEFT/RTGS is 1 Crore per transaction",
    "Remittance of funds by way of DD,mail/telegraphic transfer above Rs.50,000 is by way of debit of customer account or against cheques and not against cash payments",
    "This limit is fixed for all customers and will not be increased as per customers request.",
    "User cannot make more than 10 transactions in a day and per Bank limit 1Lakhs and per day limit is 2Lakhs.",
    "మిస్టర్ స్వామి వినయ్",
    "డెబిట్ కార్డును ఈ క్రింది విధంగా బ్లాక్ చేయవచ్చు ఎస్ఎంఎస్ ద్వారా: ఎటిఎం / డెబిట్ కార్డును నిరోధించడానికి ఎస్ఎంఎస్ సింటాక్స్: కార్డ్బ్లాక్ <స్పేస్> XXXX (XXXX చివరి నాలుగు అంకెలు A / c నం) నుండి 56161",
    "మైనర్ ఖాతాల కోసం రూపొందించిన ఎక్స్‌క్లూజివ్ సేవింగ్స్ బ్యాంక్ పాస్ బుక్ దానిపై అతికించిన ఫోటోతో మాత్రమే జారీ చేయాలి.",
    "ఒక రోజు నగదును రూ .2 లక్షల వరకు జమ చేయవచ్చు, ఇక్కడ ఖాతా పాన్‌తో అనుసంధానించబడి, ఖాతా పాన్‌తో లింక్ చేయబడని రూ .49950 / -.",
    "నగదు రీసైక్లర్ / డిపాజిట్ మెషీన్లో నగదు జమ చేసినందుకు కస్టమర్పై ఎటువంటి ఛార్జీలు లేవు.",
    "స్పష్టీకరణ కోసం BNA / CR అనుసంధానించబడిన బ్రాంచ్‌ను సందర్శించండి.",
    "దయచేసి లావాదేవీ వివరాలను ఇమెయిల్‌కు మెయిల్ చేయండి.",
    "నేను మీకు సహాయం చేయగలను! సిస్టమ్ లోపం కారణంగా లావాదేవీ విఫలమై ఉండవచ్చు.మీ లావాదేవీ ID మీ రిఫరెన్స్ ఐడి, మీరు మా టోల్ ఫ్రీ నంబర్ XXXXXXXXXX లో మాతో తీసుకోవచ్చు.",
    "దయచేసి మా టోల్ ఫ్రీ నంబర్ XXXXXXXXXX ని సంప్రదించండి",
    "కొన్నిసార్లు చాలా మంది వినియోగదారులు టోల్ ఫ్రీ నంబర్ / కస్టమర్ కేర్ నంబర్ కోసం ఒకే సమయంలో ప్రయత్నిస్తున్నారు, దీనివల్ల ఏ సంఖ్య బిజీగా ఉంటుంది / చేరుకోలేరు. ఇలాంటి సందర్భాల్లో మేము మిమ్మల్ని అభ్యర్థిస్తున్నాము దయచేసి కొన్ని నిమిషాల తర్వాత కనెక్ట్ చేయడానికి ప్రయత్నించండి.",
    "లావాదేవీల సంఖ్యకు పరిమితి లేదు.",
    "గుర్తింపు మరియు చిరునామా రెండింటికి రుజువుగా ఆధార్ కార్డు అంగీకరించబడుతుంది.",
    "ఇది సర్వర్‌తో కనెక్టివిటీపై ఆధారపడి ఉంటుంది.",
    "బ్రాంచ్ వ్యాపార గంటలు-కేంద్రం నడుస్తున్న చోట.",
    "ఆధార్ బయోమెట్రిక్ / డెమోగ్రాఫిక్ సవరణ / నవీకరణ కోసం రూ. 50 / - (జీఎస్టీతో సహా).",
    "నేను మీకు సహాయం చేయగలను! .మీరు దీని ద్వారా మీ మొబైల్ నంబర్‌ను అప్‌డేట్ చేసుకోవచ్చు: ఎ) బ్రాంచ్ బి) ఎటిఎం. దయచేసి గమనిక: మీకు కార్పొరేట్ ఇంటర్నెట్ బ్యాంకింగ్ ఉంటే మొబైల్ నంబర్‌ను సందర్శించడం ద్వారా నవీకరించవచ్చు. ఇంటి శాఖ మాత్రమే.",
    "మీరు బ్యాంక్ బ్రాంచ్ ద్వారా సమీపించాల్సిన అవసరం ఉంది.",
    "ఆధార్‌లో చిరునామా నవీకరణ ఆన్‌లైన్‌లో సాధ్యమే - మరిన్ని వివరాల కోసం దయచేసి సందర్శించండి: - www.uidai.gov.in * ఈ సేవను పొందడానికి రిజిస్టర్డ్ మొబైల్ నంబర్ అవసరం.",
    "దయచేసి సంప్రదించండి: XXXXXXXXXXX లేదా సమీప బ్యాంకుకు వెళ్లండి.",
    "లేదు, పరిచయం అవసరం లేదు.",
    "మీ ఇటీవలి ఛాయాచిత్రాన్ని సమర్పించడం ద్వారా మరియు బ్యాంక్ అధికారి సమక్షంలో మీ సంతకం లేదా బొటనవేలు ముద్రను కొన్ని పరిమితులకు లోబడి ఉంచడం ద్వారా మీరు ఇప్పటికీ చిన్న ఖాతా అని పిలువబడే బ్యాంకు ఖాతాను తెరవవచ్చు.",
    "రూ .200 / - వసూలు చేయబడుతుంది.",
    "స్మార్ట్‌ఫోన్ మరియు బ్యాంక్ ఖాతా ఉన్న ఏ వ్యక్తి అయినా యుపిఐని ఉపయోగించడానికి అర్హులు. చెప్పబడుతున్నది, మీకు బ్యాంకులో నమోదు చేయబడిన మీ మొబైల్ నంబర్ మరియు ఆ ఖాతాకు లింక్ చేయబడిన డెబిట్ కార్డ్ అవసరం. మీరు ప్లేస్టోర్ లేదా యాప్‌స్టోర్ నుండి అనువర్తనాన్ని డౌన్‌లోడ్ చేసుకోవచ్చు.",
    "ఒక UPI ID లేదా VPA (వర్చువల్ చెల్లింపు చిరునామా) అనేది ఒక ప్రత్యేకమైన ఐడెంటిఫైయర్, ఇది మీరు UPI లో డబ్బు పంపించడానికి మరియు స్వీకరించడానికి ఉపయోగించవచ్చు. డబ్బును బదిలీ చేయడానికి మీరు ఉపయోగించగల ఒక ప్రత్యేకమైన ID గా ఆలోచించండి.",
    "వినియోగదారుడు అన్ని యుపిఐ అనువర్తనాల్లో వారి బ్యాంక్ ఖాతాల కోసం సృష్టించిన అదే పిన్ను ఉపయోగించవచ్చు.",
    "DTAA అనేది డబుల్ టాక్స్ ఎగవేత ఒప్పందం.",
    "నేను మీకు సహాయం చేయగలను! సిస్టమ్ లోపం కారణంగా లావాదేవీ విఫలమై ఉండవచ్చు.మీ లావాదేవీ ID మీ రిఫరెన్స్ ఐడి, మీరు మా టోల్ ఫ్రీ నంబర్ 1800 425 1515 లో మాతో తీసుకోవచ్చు.",
    "నేను మీకు సహాయం చేయగలను! క్రింద పేర్కొన్న రకమైన లావాదేవీలను ఇంటర్నెట్ బ్యాంకింగ్ ద్వారా చేయవచ్చు: - రిటైల్ / వ్యక్తిగత వినియోగదారులు ఫండ్ బదిలీ లేదా చెల్లింపు చేయవచ్చు: 1.) సొంత ఖాతా, 2.) ఇతర ఆంధ్ర బ్యాంక్ ఖాతా, 3.) నెఫ్ట్ / ఆర్టిజిఎస్ / ఐఎంపిఎస్, 4.) సొంత పిపిఎఫ్ ఖాతా, 5.) ఇతర ఆంధ్ర బ్యాంక్ పిపిఎఫ్ ఖాతా, 6.) పన్ను చెల్లింపు. కార్పొరేట్ / నాన్-పర్సనల్ యూజర్లు ఫండ్ ట్రాన్స్ఫర్ లేదా చెల్లింపు చేయవచ్చు: 1.) సొంత ఖాతా, 2.) ఇతర ఆంధ్ర బ్యాంక్ ఖాతా, 3.) నెఫ్ట్ / ఆర్టిజిఎస్ / ఐఎంపిఎస్, 4.) బల్క్ నెఫ్ట్, 5.) పన్ను చెల్లింపు.",
    "అవును, రిటైల్ వినియోగదారుల కోసం ఇంటర్నెట్ బ్యాంకింగ్‌లో ఈ సౌకర్యం అందుబాటులో ఉంది. వారు OTP తో మాత్రమే రూ .50,000 / - వరకు లావాదేవీలు చేయవచ్చు.",
    "NEFT / RTGS కోసం లావాదేవీ పరిమితి ప్రతి లావాదేవీకి 1 కోట్లు",
    "రూ .50,000 పైన డిడి, మెయిల్ / టెలిగ్రాఫిక్ బదిలీ ద్వారా నిధుల చెల్లింపు కస్టమర్ ఖాతా డెబిట్ ద్వారా లేదా చెక్కులకు వ్యతిరేకంగా మరియు నగదు చెల్లింపులకు వ్యతిరేకంగా కాదు",
    "ఈ పరిమితి వినియోగదారులందరికీ నిర్ణయించబడింది మరియు వినియోగదారుల అభ్యర్థన ప్రకారం పెంచబడదు.",
    "వినియోగదారు ఒక రోజులో 10 కంటే ఎక్కువ లావాదేవీలు చేయలేరు మరియు బ్యాంక్ పరిమితికి 1 లక్షలు మరియు రోజు పరిమితి 2 లక్షలు.",
    "श्री स्वामी विनय",
    "डेबिट कार्ड को एसएमएस के माध्यम से नीचे ब्लॉक किया जा सकता है: एटीएम / डेबिट कार्ड को ब्लॉक करने के लिए एसएमएस सिंटैक्स: कार्डब्लॉक <SPACE> XXXX (XXXXLast चार अंकों के ए / सी नंबर) से 56161",
    "मामूली खातों के लिए डिज़ाइन किया गया विशेष बचत बैंक पास बुक केवल उस पर चिपकाए गए फोटो के साथ जारी किया जाना चाहिए।",
    "एक दिन के लिए कैश जमा किया जा सकता है, जहां खाता पैन से जुड़ा हुआ है और रु .49950 / - जहां खाता पैन से लिंक नहीं है।",
    "कैश रिसाइक्लर / डिपॉजिट मशीन में कैश जमा करने के लिए ग्राहक पर कोई शुल्क नहीं लगाया गया।",
    "ब्रांच पर जाएं जहां BNA / CR क्लैरिफिकेशन के लिए लिंक किया गया है।",
    "कृपया लेनदेन का विवरण ईमेल पर मेल करें।",
    "मैं आपकी मदद कर सकता हूं! सिस्टम त्रुटि के कारण लेनदेन विफल हो सकता है। आपकी ट्रांजेक्शन आईडी आपकी संदर्भ आईडी है, जिसे आप हमारे टोल फ्री नंबर XXXXXXXXXX में हमारे साथ ले जा सकते हैं।",
    "कृपया हमारे टोल फ्री नंबर XXXXXXXXXX पर संपर्क करें",
    "कभी-कभी कई उपयोगकर्ता एक ही समय में टोल फ्री नंबर / कस्टमर केयर नंबर के लिए कोशिश कर रहे होंगे, जिसके कारण नंबर व्यस्त हो जाता है / नहीं पहुंच पाता है। ऐसे मामलों में हम आपसे अनुरोध करते हैं कृपया कुछ मिनट बाद कनेक्ट करने का प्रयास करें।",
    "लेनदेन की संख्या की कोई सीमा नहीं है।",
    "आधार कार्ड को पहचान और पते दोनों के प्रमाण के रूप में स्वीकार किया जाता है।",
    "यह सर्वर से कनेक्टिविटी पर निर्भर करता है।",
    "शाखा व्यापार घंटे-जहां केंद्र चल रहा है।",
    "आधार बायोमेट्रिक / डेमोग्राहिक संशोधन / अद्यतन के लिए रु। 50 / - (जीएसटी सहित)।",
    "मैं इसमें आपकी मदद कर सकता हूं! आप अपने मोबाइल नंबर को अपडेट कर सकते हैं: a) ब्रांच b) ATM.Please नोट: यदि आप कॉर्पोरेट इंटरनेट बैंकिंग कर रहे हैं तो मोबाइल नंबर को अपडेट किया जा सकता है। केवल घर की शाखा।",
    "आप बैंक शाखा से संपर्क करना चाहते हैं।",
    "आधार में एड्रेस अपडेशन ऑनलाइन संभव है - अधिक जानकारी के लिए कृपया देखें: - www.uidai.gov.in * इस सेवा का लाभ उठाने के लिए पंजीकृत मोबाइल नंबर आवश्यक है।",
    "कृपया संपर्क करें: XXXXXXXXXX या निकटतम बैंक में जाएं।",
    "नहीं, परिचय की आवश्यकता नहीं है।",
    "आप अभी भी एक बैंक खाता खोल सकते हैं जिसे लघु खाता के रूप में जाना जाता है, अपनी हालिया तस्वीर जमा करके और बैंक अधिकारी की उपस्थिति में अपने हस्ताक्षर या अंगूठे का निशान लगाकर कुछ प्रतिबंधों के अधीन। खाते का संचालन।",
    "Rs.200 / - लगाया जाएगा, अगर त्रैमासिक औसत संतुलन बनाए नहीं रखा जाता है।",
    "स्मार्टफोन और बैंक खाते वाले कोई भी व्यक्ति UPI का उपयोग करने के लिए योग्य है। कहा जा रहा है, आपको बैंक के साथ पंजीकृत अपना मोबाइल नंबर और उस खाते से जुड़ा एक डेबिट कार्ड चाहिए। आप ऐप को प्लेस्टोर या ऐपस्टोर से डाउनलोड कर सकते हैं।",
    "एक यूपीआई आईडी या वीपीए (वर्चुअल पेमेंट एड्रेस) एक विशिष्ट पहचानकर्ता है जिसका उपयोग आप यूपीआई पर पैसे भेजने और प्राप्त करने के लिए कर सकते हैं। इसे एक अद्वितीय आईडी के रूप में उपयोग करें जिसे आप पैसे ट्रांसफर करने के लिए उपयोग कर सकते हैं।",
    "उपयोगकर्ता अपने बैंक खातों के लिए बनाए गए एक ही पिन का उपयोग सभी UPI ऐप्स में कर सकते हैं।",
    "DTAA डबल टैक्स अवॉइडेंस एग्रीमेंट है।",
    "मैं आपकी मदद कर सकता हूं! सिस्टम त्रुटि के कारण लेनदेन विफल हो सकता है। आपकी ट्रांजेक्शन आईडी आपकी संदर्भ आईडी है, जिसे आप हमारे टोल फ्री नंबर 1800 425 1515 में हमारे साथ ले जा सकते हैं।",
    "मैं इसमें आपकी मदद कर सकता हूं! नीचे उल्लिखित प्रकार के लेनदेन इंटरनेट बैंकिंग के माध्यम से किए जा सकते हैं: - खुदरा / व्यक्तिगत उपयोगकर्ता फंड ट्रांसफर या भुगतान करने के लिए कर सकते हैं: 1.) स्वयं खाता, 2।) अन्य आंध्र बैंक खाता, 3।) नेफ्ट / RTGS /IMPS,4.)Own PPF खाता, 5।) अन्य आंध्रा बैंक PPF खाता, 6।) कर भुगतान। कॉर्पोरेट / गैर-व्यक्तिगत उपयोगकर्ता फंड ट्रांसफर या भुगतान कर सकते हैं: 1।) स्वयं खाता, 2।) अन्य आंध्रा बैंक खाता, 3।) नेफ्ट / आरटीजीएस / आईएमपीएस, 4।) बल्क नेफ्ट, 5।) कर भुगतान।",
    "के साथ नेफ्ट लेन-देन की सीमा। हां, यह सुविधा खुदरा उपयोगकर्ताओं के लिए इंटरनेट बैंकिंग में उपलब्ध है। वे केवल ओटीपी के साथ रु। 50,000 / - तक के लेनदेन कर सकते हैं।",
    "एनईएफटी / आरटीजीएस के लिए लेन-देन की सीमा 1 करोड़ प्रति लेनदेन है",
    "डीडी के माध्यम से धनराशि का प्रेषण, रु। 50,000 से ऊपर का मेल / टेलीग्राफिक ट्रांसफर ग्राहक के खाते के डेबिट के माध्यम से या चेक के माध्यम से होता है न कि नकद भुगतान के खिलाफ",
    "यह सीमा सभी ग्राहकों के लिए निर्धारित है और ग्राहकों के अनुरोध के अनुसार नहीं बढ़ाई जाएगी।",
    "उपयोगकर्ता एक दिन में 10 से अधिक लेनदेन नहीं कर सकते हैं और प्रति बैंक सीमा 1Lakhs और प्रति दिन की सीमा 2 लाख है।"
]


WORD = re.compile(r"\w+")

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def checkQuery(query):
    ans = "Please contact us"
    max = 0
    for idx,question in enumerate(corpus):
        text1 = query.translate(str.maketrans('','',string.punctuation))
        text2 = question.translate(str.maketrans('','',string.punctuation))
        v1 = Counter()
        v2 = Counter()
        for i in text1.split():
            v1[i] += 1
        for i in text2.split():
            v2[i] += 1
        cosine = get_cosine(v1,v2)
        if cosine>0.4 and cosine>max:
            max = cosine
            ans = answers[idx]
    return ans

app = Flask(__name__)

@app.route('/',methods=['POST'])
def getSentence():
    givenString = request.get_json()
    ans = checkQuery(givenString["string"])
    return jsonify({"ans":ans})

app.run(port=5000)
