import json
import nltk
from nltk.corpus import wordnet

nltk.download("wordnet", quiet=True)

# ---------------- HELPERS ---------------- #

def synonyms(word):
    syns = set([word])
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            syns.add(lemma.name().replace("_", " "))
    return list(syns)[:3]

TEMPLATES = [
    "tell me about {}",
    "what is {}",
    "information about {}",
    "details of {}",
    "how does {} work",
    "can you explain {}",
    "{} in chandigarh university",
    "{} at cu",
    "i want to know about {}",
    "guide me about {}",
    "queries related to {}",
    "anything on {}",
    "give me info on {}",
    "do you know about {}"
]

def build_patterns(phrases):
    patterns = set()
    for p in phrases:
        patterns.add(p)
        for t in TEMPLATES:
            patterns.add(t.format(p))
    return list(patterns)

# ---------------- GENERAL CHAT ---------------- #

INTENTS = [
    {
        "tag": "greeting",
        "patterns": [
            "hi", "hello", "hey", "good morning",
            "good evening", "hi there", "hello there", "sup", "what's up",
            "greetings", "namaste"
        ],
        "responses": [
            "Hello! 👋 How can I assist you with Chandigarh University today?",
            "Hi there! I'm your CU virtual assistant. Ask me anything about academics, admissions, campus life, and more.",
            "Hey! Need help navigating life at Chandigarh University? Just ask!"
        ]
    },
    {
        "tag": "thanks",
        "patterns": ["thanks", "thank you", "thanks a lot", "appreciate it", "great help", "thanks for the info"],
        "responses": [
            "You're very welcome! 😊 Let me know if you need anything else.",
            "Happy to help! Have a great time at CU.",
            "Anytime! Go CU!"
        ]
    },
    {
        "tag": "bot_identity",
        "patterns": ["who are you", "what are you", "what is your name", "who made you", "are you human or bot"],
        "responses": [
            "I am the highly intelligent virtual assistant for Chandigarh University (CU). I'm here to answer your queries!",
            "I'm the CU Chatbot. I know all about placements, hostels, fests, and courses here."
        ]
    }
]

# ---------------- MEANINGFUL CU INTENTS (MASSIVE EXPANSION) ---------------- #

CU_INTENT_BANK = {
    "attendance_rule": {
        "phrases": ["attendance policy", "75% attendance", "minimum attendance", "attendance requirement", "consequences of low attendance", "short attendance", "attendance rules", "What is the 75% attendance rule?"],
        "responses": [
            "Chandigarh University strictly enforces a minimum 75% attendance rule. Falling below this may lead to debarring from final semester exams.",
            "You need at least 75% attendance in each subject to appear for end-term examinations. Medical leaves must be approved promptly.",
            "Keep your attendance above 75%! If you fall short, you might face heavy penalties, extra assignments, or be detained from exams."
        ]
    },
    "attendance_medical": {
        "phrases": ["medical certificate", "medical leave", "sick leave attendance", "hospitalized attendance"],
        "responses": [
            "For medical leaves, submit a valid medical certificate from a registered practitioner to your HOD within a week of joining back.",
            "Medical certificates can provide some relaxation, but total attendance (including medical) usually shouldn't fall below a strict threshold (e.g. 65%). Check specific department norms."
        ]
    },
    "cuims_login": {
        "phrases": ["cuims", "cuims login", "forgot cuims password", "uims portal", "student portal", "cuchd portal"],
        "responses": [
            "CUIMS (Chandigarh University Information Management System) is your primary student portal for attendance, timetables, fee payment, and results.",
            "You can log into CUIMS via uims.cuchd.in. Use your UID as the username. If you forgot your password, use the 'Forgot Password' link to reset via your registered email/phone."
        ]
    },
    "blackboard_lms": {
        "phrases": ["blackboard", "lms", "assignments portal", "where to submit assignments", "online classes portal"],
        "responses": [
            "Blackboard Learn is the official Learning Management System (LMS) at CU. Faculty upload notes, take quizzes, and collect assignments here.",
            "You can access Blackboard via cuchd.blackboard.com using your CU email credentials."
        ]
    },
    "mess_food": {
        "phrases": ["mess food", "hostel food", "mess quality", "veg food", "non veg food", "food options", "hostel menu"],
        "responses": [
            "Chandigarh University has large dining halls serving 4 meals a day (Breakfast, Lunch, Snacks, Dinner). The menu rotates weekly.",
            "The mess provides primarily vegetarian food with special non-veg options available on specific days. Quality is strictly monitored.",
            "Hostel residents get fixed meals. If you're a day scholar or just want variety, you can visit the food courts on campus."
        ]
    },
    "hostel_timing": {
        "phrases": ["hostel timing", "in time", "out time", "curfew", "hostel rules", "late entry", "What are the hostel in-times?"],
        "responses": [
            "Hostel timings (in-time) vary specifically by gender and block. Generally, boys' hostels might have later timings than girls' hostels for security reasons. Over time, norms are actively modernized.",
            "Late entry into hostels requires prior intimation via the hostel warden or a gate pass. Repeated late entries might incur fines or inform parents."
        ]
    },
    "hostel_booking": {
        "phrases": ["hostel booking", "ac room", "non ac room", "hostel fees", "hostel availability"],
        "responses": [
            "You can book a hostel room through CUIMS during admission or right before the new academic year. Options range from 1-seater to 5-seater with AC/Non-AC variants.",
            "Hostel seats are allotted on a first-come, first-serve basis. Fees range significantly depending on whether you choose AC, attached washrooms, or standard occupancy."
        ]
    },
    "cu_fest_tcu": {
        "phrases": ["cu fest", "tcu", "tech fest", "cultural fest", "celebrity visits", "youth fest", "Tell me about CU Fest"],
        "responses": [
            "Chandigarh University is famous for its massive fests! 'CU Fest' and 'Tech Invent' bring major celebrities, tech competitions, and DJ nights.",
            "TCU (The Chandigarh University) events happen year-round. We often have Bollywood stars coming for movie promotions at the ground.",
            "Participating in fests is a great way to earn extracurricular credits and have fun!"
        ]
    },
    "medical_facility": {
        "phrases": ["medical facility", "health care", "hospital", "doctor on campus", "ambulance", "sick on campus"],
        "responses": [
            "CU has a dedicated dispensary and medical officers on campus 24x7. Free primary healthcare is provided to students.",
            "In case of emergencies, university ambulances provide quick transit to nearby superspecialty hospitals in Mohali/Kharar."
        ]
    },
    "id_card": {
        "phrases": ["student id card", "lost id card", "duplicate id card", "id card issue", "uid missing", "where to get id card", "How to apply for a duplicate ID card?"],
        "responses": [
            "Your ID card (Smart Card) is mandatory. Without it, you cannot enter the campus or borrow library books. It also works as a smart wallet at some campus outlets.",
            "If lost, you must lodge an FIR (or DDR), pay a fine (usually Rs. 500) via CUIMS, and apply for a duplicate card at the DSW office."
        ]
    },
    "library_timings": {
        "phrases": ["library timings", "library hours", "when is library open", "central library"],
        "responses": [
            "The A.P.J. Abdul Kalam Central Library stays open from 8:00 AM to 8:00 PM on working days, but timings are extended till midnight or 24x7 during end-semester exams.",
            "To issue books, you must have your physical ID card. You can borrow up to 4 books for 14 days."
        ]
    },
    "placement_training": {
        "phrases": ["placement training", "aptitude training", "interview preparation", "cpp", "tpp", "dcp"],
        "responses": [
            "CU provides Department of Career Planning (DCP) classes, known as TPP (Training and Placement Program). It covers quantitative aptitude, logical reasoning, and soft skills.",
            "From the 4th semester onwards, TPP classes are crucial for cracking placement tests. Missing them can lead to lower internal placement scores."
        ]
    },
    "placement_stats": {
        "phrases": ["highest package", "average package", "placement record", "companies visiting", "placement stats", "Tell me about CSE placements"],
        "responses": [
            "Chandigarh University holds records for placing massive numbers of students in a single academic year with over 900+ multi-national companies visiting.",
            "For CSE specifically, top recruiters include Microsoft, Google, Amazon, and IBM. The highest packages often exceed 50+ LPA. The average package hovers around 7-9 LPA.",
            "Top recruiters include Microsoft, Google, Amazon, IBM, Deloitte, and Cognizant."
        ]
    },
    "anti_ragging": {
        "phrases": ["ragging", "anti ragging", "ragging rules", "ragging complaint", "bullying helpline"],
        "responses": [
            "Chandigarh University has a ZERO TOLERANCE policy for ragging. Anyone found guilty will be expelled immediately and handed over to the police.",
            "If you face any issues, immediately contact the UGC Anti-Ragging Helpline, your Warden, or the DSW (Dean Students Welfare)."
        ]
    },
    "transport_bus": {
        "phrases": ["transportation", "bus facility", "bus pass", "bus routes", "university bus"],
        "responses": [
            "CU offers an extensive bus transport network covering Chandigarh, Mohali, Panchkula, Ambala, Patiala, and far-off local regions.",
            "Bus fees vary by route distance. You must carry your valid bus pass to board; random checks are frequent.",
            "You can apply for the bus facility via the specific transport portal linked in CUIMS."
        ]
    },
    "parking": {
        "phrases": ["parking", "car parking", "bike parking", "vehicle entry", "student parking"],
        "responses": [
            "Dedicated multi-level or open parking spaces are available for day scholars. Proper university vehicle stickers are mandatory for regular entry.",
            "Hostellers are generally discouraged from keeping private four-wheelers unless authorized by DSW."
        ]
    },
    "sports_facility": {
        "phrases": ["sports facility", "gym", "swimming pool", "cricket ground", "football", "sports quota"],
        "responses": [
            "CU boasts extensive sports facilities, including indoor stadiums, a fully equipped gym, basketball courts, and large cricket/football grounds.",
            "For hostellers, sports gears can be issued. CU also aggressively recruits and supports students under the sports quota with scholarships."
        ]
    },
    "scholarships": {
        "phrases": ["scholarships", "cucet", "fee concession", "sports scholarship", "defense scholarship"],
        "responses": [
            "CUCET (Chandigarh University Common Entrance Test) offers substantial scholarships based on merit up to 100%.",
            "There are specific scholarships for Defense personnel wards, Sports quota, single girl child, and post-matric SC/ST schemes. Make sure to renew it yearly by maintaining the required CGPA!"
        ]
    },
    "wifi": {
        "phrases": ["campus wifi", "internet", "wifi password", "cu-wifi"],
        "responses": [
            "The entire campus is Wi-Fi enabled. You log in using your UID and the initial portal password. Data usage limits may apply in hostels to curb misuse."
        ]
    },
    "clubs_societies": {
        "phrases": ["clubs", "societies", "student organizations", "ieee", "acm", "drama club", "dance club", "nss", "ncc"],
        "responses": [
            "CU has over 100 clubs ranging from IEEE, ACM, technical clubs, to specialized drama, fine arts, and photography clubs.",
            "Joining clubs, NSS, or NCC gives you extracurricular points which look great on your resume and help in personality development."
        ]
    },
    "exam_structure": {
        "phrases": ["exam pattern", "mst", "mid semester", "end semester", "est", "passing marks", "grading system"],
        "responses": [
            "A typical semester has two mid-terms (MST 1 & 2) and one End Semester Test (EST). Continuous assessment includes assignments, quizzes, and attendance weightage.",
            "Passing marks are typically 40% overall. CU follows a relative grading system (A+, A, B+, etc.) based on the class average."
        ]
    },
    "reappear": {
        "phrases": ["reappear", "backlog", "failed in subject", "supply exam"],
        "responses": [
            "If you fail a subject, you will get an 'F' or 'E' grade. You must fill a reappear form via CUIMS and pay the reappear fee to give the exam in a subsequent semester.",
            "Clear your reappears ASAP! Having pending backlogs limits you from sitting in campus placements."
        ]
    },
    "cucet": {
         "phrases": ["cucet exam", "entrance exam", "admission test", "cucet syllabus"],
         "responses": [
             "CUCET is the Chandigarh University Common Entrance Test. It determines both your admission eligibility and scholarship band.",
             "The test is fully online and proctored. Syllabus is based on your previous qualification (e.g., 10+2 science syllabus for B.Tech aspirants)."
         ]
    },
    "laundry": {
        "phrases": ["laundry service", "washing clothes", "dhobi", "ironing"],
        "responses": [
            "Hostels provide outsourced laundry services. A fixed number of clothes are washed and ironed per month (e.g., typically 40-50 clothes/person depending on your plan).",
            "Be sure to label or mark your clothes properly to avoid mix-ups at the laundry!"
        ]
    },
    "distance_education": {
        "phrases": ["distance education", "cuidol", "online degree", "odl"],
        "responses": [
            "CU offers online and distance learning degrees through CUIDOL (Chandigarh University Institute of Distance & Online Learning), approved by UGC-DEB.",
            "It is highly ranked and very popular for working professionals who want to complete MBA, MCA, or BBA programs remotely."
        ]
    },
    "international_tieups": {
       "phrases": ["study abroad", "international programs", "semester exchange", "foreign university tieups", "global immersion"],
       "responses": [
           "CU has tie-ups with 300+ international universities across USA, UK, Canada, and Australia.",
           "You can opt for semester-exchange programs, summer internships abroad, or 2+2/3+1 articulation programs that grant dual degrees."
       ]
   },
    "food_courts": {
       "phrases": ["food court", "canteens", "tuck shop", "cafe", "dominos", "subway"],
       "responses": [
           "Beyond host messes, CU has large food courts with popular outlets like Domino's, Subway, CCD, La Pino'z, and numerous local eateries.",
           "The most popular hangout spots are the main food court near the engineering blocks and scattered tuck shops."
       ]
   },
   "banks_atms": {
       "phrases": ["atm", "bank on campus", "sbi", "withdraw money"],
       "responses": [
           "Yes, CU campus houses a full-fledged SBI branch with multiple ATMs scattered around academic blocks and hostels for easy cash access."
       ]
   },
    "alumni": {
        "phrases": ["alumni network", "passouts", "alumni portal", "alumni association"],
        "responses": [
            "CU's Alumni network is vast and active globally. The university frequently hosts alumni meets and interaction sessions for mentorship.",
            "Graduates can register on the CU Alumni Portal to stay connected, find jobs, and access university privileges."
        ]
    },
    "dress_code": {
       "phrases": ["dress code", "uniform", "what to wear", "clothes allowed", "shorts allowed"],
       "responses": [
           "CU is quite liberal with casual wear; there is no strict uniform for most programs unless you belong to Hotel Management, Airlines, or specific professional courses.",
           "However, proper formal or smart casual wear is expected for university labs, TPP sessions, and placement drives. Extremely informal wear (like shorts) is generally discouraged in academic blocks."
       ]
   }
}

# Generate CU intents with vast variation
for tag, data in CU_INTENT_BANK.items():
    INTENTS.append({
        "tag": tag,
        "patterns": build_patterns(data["phrases"]),
        "responses": data["responses"]
    })

# ---------------- COURSE-SPECIFIC (DEEP EXPANSION) ---------------- #

DEPARTMENTS = {
    "computing": [
        "Computer Science Engineering (CSE)",
        "Artificial Intelligence & Machine Learning (AIML)",
        "Data Science",
        "Cloud Computing",
        "Cyber Security",
        "Internet of Things (IoT)",
        "Software Engineering",
        "BCA", "MCA"
    ],
    "engineering_core": [
        "Mechanical Engineering",
        "Civil Engineering",
        "Electrical Engineering",
        "Electronics & Communication Engineering (ECE)",
        "Mechatronics",
        "Automobile Engineering",
        "Aerospace Engineering"
    ],
    "business_management": [
        "BBA", "BBA Fintech", "BBA Business Analytics",
        "MBA", "MBA HR", "MBA Finance", "MBA Marketing",
        "MBA International Business", "B.Com", "M.Com"
    ],
    "health_pharma": [
        "Pharmacy (B.Pharm)", "D.Pharm",
        "Physiotherapy (BPT)", "Optometry",
        "Nursing", "Medical Lab Technology (BMLT)",
        "Nutrition & Dietetics"
    ],
    "law_humanities": [
        "BA LLB", "BBA LLB", "B.Com LLB", "LLM",
        "Psychology", "Journalism & Mass Communication",
        "Animation & Multimedia", "Fashion Design", "Fine Arts", "Film Studies"
    ]
}

COURSE_TOPICS = [
    "fees", "eligibility", "placements",
    "syllabus", "duration", "scope", "curriculum", "intake", "subjects", "professors",
    "admission process", "merit criteria", "highest package"
]

for category, courses in DEPARTMENTS.items():
    for course in courses:
        patterns = []
        for topic in COURSE_TOPICS:
            for syn in synonyms(topic):
                base = f"{syn} of {course}"
                patterns.extend(build_patterns([
                    base,
                    f"{base} in chandigarh university",
                    f"{base} at cu",
                    f"is {course} good at cu",
                    f"what is the {syn} for {course}"
                ]))

        INTENTS.append({
            "tag": f"course_{course.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('&', 'and')}",
            "patterns": list(set(patterns)), # Use set to remove exact duplicates
            "responses": [
                f"{course} at Chandigarh University features an industry-vetted curriculum designed for maximum employability.",
                f"For {course}, CU provides specialized labs, expert faculty, and stellar placement opportunities among top MNCs.",
                f"You can find exact fee structures and eligibility for {course} on the official cuchd.in website or via CUCET.",
                f"Students of {course} often secure top-tier placements. The program ensures holistic academic and practical growth."
            ]
        })

# ---------------- FALLBACK ---------------- #

INTENTS.append({
    "tag": "fallback",
    "patterns": ["blablabla", "no match found testing fallback"],
    "responses": [
        "I'm not entirely sure about that. Could you rephrase your question?",
        "That's an interesting query! Currently, my knowledge is focused strongly on Chandigarh University academics, campuses, and logistics. Could you ask about that?",
        "Sorry, I couldn't understand that. Please ask something related to CU like placements, hostels, courses, or fees.",
        "Hmm, I didn't get that. Try asking 'What's the 75% attendance rule?' or 'Tell me about CSE placements'."
    ]
})

# ---------------- SAVE ---------------- #

with open("intents.json", "w", encoding="utf-8") as f:
    json.dump({"intents": INTENTS}, f, indent=2, ensure_ascii=False)

print("✅ intents.json generated massive expansion")
print(f"Total Intents: {len(INTENTS)}")
pattern_count = sum(len(i["patterns"]) for i in INTENTS)
print(f"Total Unique Patterns: {pattern_count}")
print("Run `python trainer_transformer.py` (if it exists) to regenerate embeddings, or start the app.py directly which does it on load.")
