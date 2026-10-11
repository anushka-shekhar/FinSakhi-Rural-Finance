"""
FinSakhi - Seed Data Helper
Populates initial sample data for schemes, awareness categories, default admin, and demo users.
Subject Mapping: DBMS & Data Integrity
"""

from werkzeug.security import generate_password_hash

def seed_fallback_data(conn):
    cursor = conn.cursor()
    
    # 1. Default Admin (admin / admin123)
    admin_hash = generate_password_hash('admin123')
    cursor.execute("""
    INSERT INTO admin_users (username, password_hash, full_name, email, role)
    VALUES (?, ?, ?, ?, ?)
    """, ('admin', admin_hash, 'FinSakhi Lead Administrator', 'admin@finsakhi.gov.in', 'admin'))

    # 2. Demo Users (user123)
    user_hash = generate_password_hash('user123')
    cursor.execute("""
    INSERT INTO users (full_name, mobile_number, password_hash, village, business_type)
    VALUES (?, ?, ?, ?, ?)
    """, ('Sunita Ramesh Patil', '9876543210', user_hash, 'Khed, Pune District', 'Dairy & Milk Products'))
    
    cursor.execute("""
    INSERT INTO users (full_name, mobile_number, password_hash, village, business_type)
    VALUES (?, ?, ?, ?, ?)
    """, ('Rameshwar Kumar Verma', '9811223344', user_hash, 'Bara Banki, Uttar Pradesh', 'Kirana & General Store'))

    # 3. Government Schemes
    schemes_data = [
        (
            'Pradhan Mantri MUDRA Yojana (PMMY) - Shishu Category',
            'PMMY-SHISHU',
            'Micro Business Loan',
            'Provides collateral-free micro-credit loans up to Rs. 50,000 for tiny business units, fruit/vegetable vendors, artisans, and village shopkeepers to purchase equipment or working capital.',
            'छोटे व्यवसायियों, फल-सब्जी विक्रेताओं, कारीगरों और किराना दुकानदारों को उपकरण या कार्यशील पूंजी खरीदने के लिए 50,000 रुपये तक का संपार्श्विक-मुक्त (बिना गारंटी) ऋण प्रदान करता है।',
            'लहान व्यावसायिक, फळे/भाजीपाला विक्रेते, कारागीर आणि किराणा दुकानदारांना साहित्य किंवा भांडवलासाठी 50,000 रुपयांपर्यंत विनातारण कर्ज उपलब्ध करून देते.',
            'All, Small Grocery / Kirana, Agriculture & Dairy, Handicrafts & Tailoring, Food Stall, Service & Repairs',
            'All India',
            0.0,
            10000.0,
            50000.0,
            0.0,
            'Aadhaar Card, Voter ID / Driving License, Bank Account Passbook (last 6 months), Business Address Proof, Passport size photograph.',
            'Visit any public sector bank, regional rural bank (RRB), or apply online via UdyamiMitra portal.',
            'https://www.mudra.org.in'
        ),
        (
            'Pradhan Mantri MUDRA Yojana (PMMY) - Kishor Category',
            'PMMY-KISHOR',
            'Small Business Growth Loan',
            'Offers collateral-free loans from Rs. 50,000 to Rs. 5,00,000 for growing micro-enterprises, small manufacturing units, agro-processing, and village service centers.',
            'बढ़ते सूक्ष्म उद्यमों, छोटी विनिर्माण इकाइयों, कृषि प्रसंस्करण और ग्रामीण सेवा केंद्रों के लिए 50,000 से 5 लाख रुपये तक का गारंटी-मुक्त ऋण प्रदान करता है।',
            'वाढणाऱ्या सूक्ष्म उद्योगांसाठी, लहान उत्पादन घटकांसाठी आणि ग्रामीण सेवा केंद्रांसाठी 50,000 ते 5 लाख रुपयांपर्यंतचे विनातारण कर्ज.',
            'All, Small Grocery / Kirana, Agriculture & Dairy, Handicrafts & Tailoring, Food Stall, Poultry & Livestock',
            'All India',
            800000.0,
            50000.0,
            500000.0,
            0.0,
            'Aadhaar Card, PAN Card, Business registration / Udyam certificate, Last 6 months bank statement, Quotation of machinery/goods to be purchased.',
            'Apply through your nearest commercial bank, cooperative bank, or UdyamiMitra portal with equipment quotation.',
            'https://www.mudra.org.in'
        ),
        (
            'PM Street Vendor AtmaNirbhar Nidhi (PM SVANidhi)',
            'PM-SVANIDHI',
            'Working Capital Micro-Credit',
            'Special micro-credit facility providing affordable working capital loan starting at Rs. 10,000 with 7% interest subsidy on timely repayment, digital transaction cashback, and graduated limits up to Rs. 50,000.',
            'सड़क किनारे रेहड़ी-पटरी लगाने वाले, खोमचे वाले और छोटे विक्रेताओं के लिए 10,000 रुपये का प्रारंभिक कार्यशील पूंजी ऋण, 7% ब्याज सब्सिडी और डिजिटल लेनदेन कैशबैक के साथ।',
            'पथविक्रेते आणि लहान हातगाडी धारकांसाठी 10,000 रुपयांचे खेळत्या भांडवलाचे कर्ज, वेळेवर परतफेडीवर 7% व्याज अनुदान आणि डिजिटल कॅशबॅक सुविधा.',
            'Food Stall, Small Grocery / Kirana, Handicrafts & Tailoring, Service & Repairs',
            'All India',
            300000.0,
            5000.0,
            50000.0,
            7.0,
            'Vending Certificate / Identity Card issued by ULB/Town Vending Committee, Aadhaar Card, Bank Account linked to mobile.',
            'Apply online at pmsvanidhi.mohua.gov.in or through Common Service Centers (CSC) and Municipal Urban Local Body office.',
            'https://pmsvanidhi.mohua.gov.in'
        ),
        (
            'Prime Minister Employment Generation Programme (PMEGP)',
            'PMEGP-KVIC',
            'Enterprise Setup Subsidy',
            'Credit-linked subsidy program providing 15% to 35% margin money subsidy for setting up new micro-enterprises in manufacturing (up to Rs. 50 Lakhs) and service sectors (up to Rs. 20 Lakhs).',
            'विनिर्माण (50 लाख रुपये तक) और सेवा क्षेत्रों (20 लाख रुपये तक) में नए सूक्ष्म उद्यम स्थापित करने के लिए 15% से 35% की मार्जिन मनी सब्सिडी प्रदान करने वाला कार्यक्रम।',
            'उत्पादन (50 लाखांपर्यंत) आणि सेवा क्षेत्रात (20 लाखांपर्यंत) नवीन सूक्ष्म उद्योग सुरू करण्यासाठी 15% ते 35% सबसिडी देणारी पत-संलग्न योजना.',
            'Handicrafts & Tailoring, Food Stall, Agriculture & Dairy, Poultry & Livestock, Service & Repairs',
            'All India',
            0.0,
            100000.0,
            2500000.0,
            25.0,
            'Project Report / Business Plan, Aadhaar Card, Caste Certificate (if SC/ST/OBC), Rural area certificate, Highest education mark sheet, PAN Card.',
            'Apply online through KVIC PMEGP e-portal (kviconline.gov.in/pmegpeportal) and submit physical copies to the District Industries Centre (DIC).',
            'https://www.kviconline.gov.in'
        ),
        (
            'Stand-Up India Scheme for Women and SC/ST Entrepreneurs',
            'STANDUP-INDIA',
            'Greenfield Enterprise Loan',
            'Facilitates bank loans between Rs. 10 Lakhs and Rs. 1 Crore to at least one SC/ST borrower and one woman borrower per bank branch for setting up a greenfield enterprise in manufacturing, services, or trading.',
            'विनिर्माण, सेवा या व्यापार में नया उद्यम स्थापित करने के लिए प्रति बैंक शाखा में कम से कम एक एससी/एसटी और एक महिला उद्यमी को 10 लाख से 1 करोड़ रुपये तक का ऋण।',
            'उत्पादन, सेवा किंवा व्यापार क्षेत्रात नवीन उद्योग सुरू करण्यासाठी महिला आणि अनुसूचित जाती/जमाती उद्योजकांसाठी 10 लाख ते 1 कोटी रुपयांपर्यंत बँक कर्ज.',
            'All, Agriculture & Dairy, Handicrafts & Tailoring, Small Grocery / Kirana, Service & Repairs',
            'All India',
            0.0,
            1000000.0,
            10000000.0,
            15.0,
            'Proof of identity (Aadhaar/PAN), SC/ST certificate or proof of woman entrepreneurship, Business Project Report, Projected Balance Sheets, Pollution clearance if required.',
            'Apply online on standupmitra.in portal or directly contact Lead District Manager (LDM) or any scheduled commercial bank.',
            'https://www.standupmitra.in'
        ),
        (
            'Kisan Credit Card (KCC) Animal Husbandry & Fisheries',
            'KCC-DAIRY',
            'Agri & Dairy Working Capital',
            'Provides concessional short-term working capital credit at effective 4% interest rate (with 3% prompt repayment incentive) up to Rs. 2 Lakhs for dairy farmers, goat farming, and poultry rearing.',
            'दुग्ध उत्पादक, बकरी पालन और पोल्ट्री पालकों के लिए प्रभावी 4% रियायती ब्याज दर पर 2 लाख रुपये तक का अल्पकालिक कार्यशील पूंजी ऋण।',
            'दुग्ध व्यवसाय, शेळीपालन आणि कुक्कुटपालनासाठी केवळ 4% सवलतीच्या व्याजदराने 2 लाख रुपयांपर्यंतचे अल्पमुदत खेळते भांडवल कर्ज.',
            'Agriculture & Dairy, Poultry & Livestock',
            'All India',
            0.0,
            20000.0,
            200000.0,
            3.0,
            'Land Records / Village Sarpanch verification, Aadhaar Card, PAN Card, Dairy cooperative milk pouring card or animal count certificate.',
            'Submit KCC application to your local primary agricultural cooperative society (PACS) or nationalized rural bank.',
            'https://www.myscheme.gov.in'
        ),
        (
            'Annasaheb Patil Arthik Vikas Mahamandal Scheme',
            'APAVM-MH',
            'State Youth Self-Employment',
            'State government interest refund scheme for youth entrepreneurs in Maharashtra. Banks provide loans up to Rs. 15 Lakhs and the corporation refunds up to 12% interest for 5 years upon regular repayment.',
            'महाराष्ट्र के युवा उद्यमियों के लिए ब्याज प्रतिपूर्ति योजना। बैंक 15 लाख तक ऋण देते हैं और निगम नियमित पुनर्भुगतान पर 12% तक ब्याज सीधे खाते में वापस करता है।',
            'महाराष्ट्रातील तरुण उद्योजकांसाठी व्याज परतावा योजना. बँका 15 लाखांपर्यंत कर्ज देतात आणि महामंडळ नियमित हप्ते भरल्यास 12% पर्यंत व्याज बँक खात्यात परत करते.',
            'All, Small Grocery / Kirana, Agriculture & Dairy, Handicrafts & Tailoring, Service & Repairs',
            'Maharashtra',
            800000.0,
            100000.0,
            1500000.0,
            12.0,
            'Domicile Certificate of Maharashtra, Aadhaar Card, PAN Card, Project Appraisal Report, Bank sanction letter, Caste/Income certificate.',
            'Register on mahaswayam.gov.in portal, obtain Letter of Intent (LOI), and submit to bank for sanction.',
            'https://mahaswayam.gov.in'
        )
    ]
    cursor.executemany("""
    INSERT INTO schemes (
        scheme_name, scheme_code, category,
        description_en, description_hi, description_mr,
        eligible_business_types, state_applicability,
        max_annual_income, min_loan_amount, max_loan_amount,
        subsidy_percentage, required_documents, how_to_apply, official_portal
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, schemes_data)

    # 4. Awareness Articles
    content_data = [
        (
            'upi-payments',
            'UPI and Digital Payments',
            'यूपीआई और डिजिटल भुगतान',
            'यूपीआय आणि डिजिटल व्यवहार',
            'UPI (Unified Payments Interface) allows you to send and receive business money instantly using your mobile phone 24x7 without carrying cash. It works through simple QR codes or mobile numbers linked to your bank account.',
            'यूपीआई (UPI) आपको अपने मोबाइल फोन का उपयोग करके नकदी ले जाने के बिना तुरंत 24x7 व्यावसायिक पैसे भेजने और प्राप्त करने की अनुमति देता है। यह क्यूआर कोड या बैंक से जुड़े मोबाइल नंबर से काम करता है।',
            'यूपीआय (UPI) मुळे आपण कोणत्याही वेळी रोख रक्कम न बाळगता मोबाईल फोनवरून व्यवसायाचे पैसे त्वरित पाठवू किंवा स्वीकारू शकता. हे बँक खात्याशी जोडलेल्या मोबाईल नंबर किंवा क्यूआर कोडद्वारे चालते.',
            'A village grocery store owner displays a printed QR code. Customers scan and pay directly into the merchant account, eliminating loose change disputes and counterfeit note risks.',
            'गाँव के एक किराना स्टोर मालिक ने अपनी दुकान पर क्यूआर कोड लगाया है। ग्राहक स्कैन करके सीधे पैसे भेजते हैं, जिससे छुट्टे पैसों की झंझट और नकली नोटों का जोखिम खत्म हो गया है।',
            'गावातील किराणा दुकानदार दुकानात क्यूआर कोड लावतात. ग्राहक थेट बँक खात्यात पैसे पाठवतात, ज्यामुळे सुट्ट्या पैशांची अडचण आणि बनावट नोटांची भीती राहत नाही.',
            'Remember: You NEVER need to enter your UPI PIN to RECEIVE money. Entering your PIN always DEDUCTS money from your bank account.',
            'याद रखें: पैसे प्राप्त करने के लिए आपको कभी भी अपना यूपीआई पिन दर्ज करने की आवश्यकता नहीं होती है। पिन दर्ज करने से हमेशा आपके खाते से पैसे कटते हैं।',
            'लक्षात ठेवा: पैसे मिळवण्यासाठी (स्वीकारण्यासाठी) कधीही यूपीआय पिन टाकण्याची गरज नसते. पिन टाकल्यास नेहमी तुमच्या खात्यातून पैसे वजा होतात.',
            1
        ),
        (
            'online-banking',
            'Safe Online & Mobile Banking',
            'सुरक्षित ऑनलाइन और मोबाइल बैंकिंग',
            'सुरक्षित ऑनलाइन आणि मोबाईल बँकिंग',
            'Mobile and Internet Banking enables rural business owners to check daily balances, download passbook statements, transfer supplier payments via NEFT/IMPS, and monitor government subsidies from home.',
            'मोबाइल और इंटरनेट बैंकिंग ग्रामीण व्यवसायियों को घर बैठे दैनिक शेष राशि की जांच करने, पासबुक डाउनलोड करने, आपूर्तिकर्ता को पैसे भेजने और सरकारी सब्सिडी की निगरानी करने में मदद करती है।',
            'मोबाईल आणि नेट बँकिंगमुळे ग्रामीण उद्योजक घरबसल्या शिल्लक रक्कम तपासू शकतात, पासबुक विवरण पाहू शकतात आणि पुरवठादारांना घरूनच खात्यात पैसे पाठवू शकतात.',
            'A tailor transfers cloth purchase payments directly to the city wholesale distributor through mobile banking instead of travelling 30 km with physical currency.',
            'एक दर्जी 30 किलोमीटर नकदी लेकर जाने के बजाय मोबाइल बैंकिंग के माध्यम से शहर के थोक विक्रेता को सीधे कपड़े का भुगतान भेजता है।',
            'एका शिंपी बांधवाने रोख पैसे घेऊन शहरात जाण्याऐवजी मोबाईल बँकिंगद्वारे थेट घाऊक विक्रेत्याच्या खात्यात कापडाचे पैसे जमा केले.',
            'Never share your net banking login credentials, password, or security questions with anyone, even if they claim to be a bank manager.',
            'अपनी नेट बैंकिंग लॉगिन जानकारी, पासवर्ड या सुरक्षा प्रश्न किसी के साथ साझा न करें, भले ही फोन करने वाला बैंक मैनेजर होने का दावा करे।',
            'तुमचा नेट बँकिंग पासवर्ड किंवा बँक खात्याचा तपशील कोणाशीही शेअर करू नका, अगदी बँकेचा मॅनेजर बोलतोय असा फोन आला तरीही नाही.',
            2
        ),
        (
            'business-loans',
            'Understanding Business Loans & Credit',
            'व्यावसायिक ऋण और ब्याज दरें',
            'व्यावसायिक कर्ज आणि व्याजदर',
            'A business loan provides capital to expand inventory, purchase machines, or modernize shops. Formal bank loans offer low interest rates (7% to 12% annually) compared to informal moneylenders who charge 36% to 60% per year.',
            'व्यवसाय ऋण आपकी इन्वेंट्री बढ़ाने, मशीन खरीदने या दुकान के आधुनिकीकरण के लिए पूंजी देता है। बैंक ऋण कम ब्याज दर (7% से 12% वार्षिक) पर मिलता है, जबकि साहूकार 36% से 60% तक भारी ब्याज लेते हैं।',
            'व्यवसाय कर्ज नवीन यंत्रसामग्री, कच्चा माल किंवा दुकानाचा विस्तार करण्यासाठी उपयुक्त ठरते. बँकेचे कर्ज वार्षिक 7% ते 12% व्याजदराने मिळते, तर सावकारी कर्ज 36% ते 60% इतके महाग असते.',
            'Investing Rs. 40,000 borrowed under MUDRA Shishu to buy a modern stitching machine doubled the tailor shop monthly output with manageable monthly EMI of Rs. 1,400.',
            'मुद्रा शिशु योजना के तहत 40,000 रुपये का ऋण लेकर आधुनिक सिलाई मशीन खरीदने से टेलर की मासिक आय दोगुनी हो गई, और मासिक किस्त मात्र 1,400 रुपये बनी।',
            'मुद्रा योजनेतून 40,000 रुपयांचे कर्ज घेऊन आधुनिक शिलाई यंत्र घेतल्यामुळे शिलाई काम दुप्पट झाले आणि मासिक हप्ता फक्त 1,400 रुपये बसला.',
            'Always borrow only what your business profits can repay. Ensure EMIs do not exceed 30% of your net monthly earnings.',
            'हमेशा उतना ही कर्ज लें जिसे आपका व्यवसाय आसानी से चुका सके। ईएमआई आपकी शुद्ध मासिक आय के 30% से अधिक नहीं होनी चाहिए।',
            'नेहमी व्यवसायाच्या फायद्यातून फेडता येईल इतकेच कर्ज घ्या. कर्जाचा मासिक हप्ता तुमच्या नफ्याच्या 30% पेक्षा जास्त नसावा.',
            3
        ),
        (
            'insurance',
            'Business & Rural Insurance Basics',
            'बीमा और सुरक्षा योजनाएं',
            'विमा आणि व्यावसायिक सुरक्षा',
            'Insurance acts as a safety shield against unexpected disasters like shop fire, livestock sickness, accident, or crop failure. Low-cost government schemes cost as little as Rs. 20 to Rs. 436 per year.',
            'बीमा अप्रत्याशित आपदाओं जैसे दुकान में आग, मवेशियों की बीमारी, दुर्घटना या फसल खराब होने के खिलाफ सुरक्षा ढाल के रूप में कार्य करता है। सरकारी योजनाएं मात्र 20 से 436 रुपये प्रति वर्ष में उपलब्ध हैं।',
            'विमा हा अनपेक्षित संकटांपासून (जसे की दुकानाला आग, जनावरांचे आजारपण, अपघात) संरक्षण देणारी ढाल आहे. शासकीय विमा योजना वर्षाला अवघ्या 20 ते 436 रुपयांत उपलब्ध आहेत.',
            'A dairy entrepreneur insured 3 cows under Pashu Bima Yojana. When one animal fell sick and died, the insurance company paid Rs. 45,000, preventing business collapse.',
            'एक डेयरी उद्यमी ने पशु बीमा योजना के तहत 3 गायों का बीमा कराया था। एक गाय की मृत्यु होने पर बीमा कंपनी ने 45,000 रुपये दिए, जिससे उसका व्यवसाय बंद होने से बच गया।',
            'एका दुग्ध व्यावसायिकाने पशु विमा उतरवला होता. एका गाईचा मृत्यू झाल्यावर विमा कंपनीकडून 45,000 रुपये भरपाई मिळाली, ज्यामुळे त्यांचे मोठे नुकसान टळले.',
            'Keep your insurance policy document, receipts, and nominee details safe and inform your family about them.',
            'अपने बीमा पॉलिसी दस्तावेज, रसीदें और नॉमिनी विवरण सुरक्षित रखें और अपने परिवार को इनके बारे में अवश्य बताएं।',
            'तुमची विमा पॉलिसी, पावत्या आणि वारसाचे नाव (Nominee) सुरक्षित ठेवा आणि कुटुंबीयांना याची माहिती द्या.',
            4
        ),
        (
            'savings-investment',
            'Savings and Safe Investments',
            'बचत और सुरक्षित निवेश के मूल सिद्धांत',
            'बचत आणि सुरक्षित गुंतवणुकीचे मूलभूत नियम',
            'Saving small amounts regularly in formal bank accounts, Post Office Recurring Deposits (RD), or Self-Help Groups (SHGs) helps build an emergency fund and future wealth without risking capital.',
            'औपचारिक बैंक खातों, डाकघर आवर्ती जमा (RD) या स्वयं सहायता समूहों (SHG) में नियमित रूप से छोटी राशि जमा करने से आपातकालीन निधि और भविष्य की सुरक्षा बनती है।',
            'बँक खाते, पोस्ट ऑफिस आरडी (RD) किंवा बचत गटामध्ये दरमहा छोटी रक्कम साठवल्याने आणीबाणीच्या काळात आधार मिळतो आणि भांडवल सुरक्षित राहते.',
            'Saving Rs. 1,000 every month in a Post Office RD creates a guaranteed reserve of over Rs. 65,000 in 5 years with central government safety.',
            'डाकघर आरडी में हर महीने 1,000 रुपये जमा करने से 5 साल में केंद्र सरकार की सुरक्षा के साथ 65,000 रुपये से अधिक का गारंटीड फंड तैयार होता है।',
            'पोस्ट ऑफिस आरडी मध्ये दरमहा 1,000 रुपये जमा केल्यास 5 वर्षांत सरकारी सुरक्षेसह 65,000 रुपयांपेक्षा जास्त रक्कम जमा होते.',
            'Beware of private chit funds or unregistered agents promising to double your money in 1 or 2 years. They are illegal scams.',
            '1 या 2 साल में पैसे दोगुना करने का वादा करने वाले निजी चिट फंड या अनधिकृत एजेंटों से सावधान रहें। वे गैरकानूनी धोखाधड़ी हैं।',
            'पैसा 1 किंवा 2 वर्षांत दुप्पट करण्याचे आमिष दाखवणाऱ्या खाजगी भिशी किंवा अनधिकृत कंपन्यांपासून सावध राहा. ती फसवणूक असते.',
            5
        ),
        (
            'financial-planning',
            'Financial Planning for Small Business',
            'छोटे व्यवसाय के लिए वित्तीय योजना',
            'लहान व्यवसायाचे आर्थिक नियोजन',
            'Financial planning means separating your household expenses from business money, recording daily income and costs in a simple register, and planning for seasonal business variations.',
            'वित्तीय योजना का अर्थ है अपने घरेलू खर्चों को व्यापार के पैसे से अलग रखना, एक साधारण बही-खाते में दैनिक आय और व्यय दर्ज करना, और मंदी के महीनों के लिए योजना बनाना।',
            'आर्थिक नियोजनाचा अर्थ म्हणजे घरगुती खर्च आणि व्यवसायाचे पैसे वेगळे ठेवणे, रोजच्या जमा-खर्चाची साध्या वहीत नोंद ठेवणे आणि भविष्यातील खर्चाचे नियोजन करणे.',
            'A food stall owner maintaining two separate pouches (one for daily raw material expenses and one for house grocery) always has cash ready to restock stock without borrowing.',
            'एक भोजनालय संचालक जो दो अलग-अलग बटुए रखता है (एक दुकान के कच्चे माल के लिए और एक घरेलू खर्च के लिए), उसे कभी भी कच्चा माल खरीदने के लिए उधार नहीं लेना पड़ता।',
            'खाद्यपदार्थ विक्रेत्याने दुकानाचा खर्च आणि घराचा खर्च वेगवेगळ्या खात्यात ठेवल्यामुळे त्याला साहित्य भरण्यासाठी कोणाकडेही हात पसरावे लागत नाहीत.',
            'Maintain a daily handwritten or digital cash diary. Review total earnings and pending supplier bills every Sunday.',
            'एक दैनिक नकद डायरी बनाए रखें। हर रविवार को कुल कमाई और बाकी उधारी की समीक्षा अवश्य करें।',
            'दररोज जमा-खर्चाची वही लिहा. प्रत्येक रविवारी आठवड्याची एकूण कमाई आणि देणी यांचा ताळेबंद तपासा.',
            6
        )
    ]
    cursor.executemany("""
    INSERT INTO financial_content (
        category_slug,
        title_en, title_hi, title_mr,
        explanation_en, explanation_hi, explanation_mr,
        example_en, example_hi, example_mr,
        safety_tips_en, safety_tips_hi, safety_tips_mr,
        display_order
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, content_data)

    # 5. Feedback Demo Entries
    feedback_data = [
        (1, 'Sunita Ramesh Patil', '9876543210', 'Appreciation', 5, 'FinSakhi helped me understand MUDRA Shishu loans in Marathi. The business calculator is very simple to use for my dairy accounts!', 'Reviewed'),
        (2, 'Rameshwar Kumar Verma', '9811223344', 'Suggestion', 5, 'The digital fraud warning about UPI PIN deduction saved me from an online QR code scam. Please keep adding more regional examples.', 'Reviewed')
    ]
    cursor.executemany("""
    INSERT INTO feedback (user_id, user_name, mobile_number, category, rating, message, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, feedback_data)
