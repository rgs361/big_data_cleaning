import json
import os

# Taxonomy Groups
# 1. Arts & Culture
# 2. Business & Career
# 3. Community & Environment
# 4. Family & Education
# 5. Food & Drink
# 6. Games & Hobbies
# 7. Health & Wellness
# 8. Music & Performance
# 9. Science & Technology
# 10. Social & Networking
# 11. Sports & Fitness
# 12. Spirituality & Religion
# 13. Travel & Outdoor
# 14. Other / Miscellaneous

CATEGORY_MAPPING = {
    # Arts & Culture
    "Art": "Arts & Culture", "Art Exhibit": "Arts & Culture", "Art Galleries": "Arts & Culture", 
    "Art History": "Arts & Culture", "Art Museums": "Arts & Culture", "Artists": "Arts & Culture", 
    "Artists & Art Lovers": "Arts & Culture", "Arts & Entertainment": "Arts & Culture", 
    "Digital Art": "Arts & Culture", "Drawing": "Arts & Culture", "Figure Drawing": "Arts & Culture", 
    "Fine Art Photography": "Arts & Culture", "Fine Arts": "Arts & Culture", "Mixed Media Art": "Arts & Culture", 
    "Museum": "Arts & Culture", "Museums & Galleries": "Arts & Culture", "Painting": "Arts & Culture", 
    "Performing Arts": "Arts & Culture", "Photography": "Arts & Culture", "Photo Editing": "Arts & Culture",
    "Photo Walks": "Arts & Culture", "Photography Classes & Workshops": "Arts & Culture", "Portrait Photography": "Arts & Culture",
    "Street Photography": "Arts & Culture", "Travel Photography": "Arts & Culture", "Sculpture": "Arts & Culture",
    "Sketching": "Arts & Culture", "Theater": "Arts & Culture", "Plays": "Arts & Culture", "Playwriting": "Arts & Culture",
    "Film": "Arts & Culture", "Film Festivals": "Arts & Culture", "Film Industry": "Arts & Culture", 
    "Film and Video Production": "Arts & Culture", "Filmmaking": "Arts & Culture", "Foreign Films": "Arts & Culture", 
    "Foreign Horror Films": "Arts & Culture", "Indie Film": "Arts & Culture", "Movies & Discussions": "Arts & Culture", 
    "Movies in Movie Theaters": "Arts & Culture", "Watching Movies": "Arts & Culture", "Bad Movies": "Arts & Culture",
    "Classic Films": "Arts & Culture", "Cult Films": "Arts & Culture", "Documentary": "Arts & Culture",
    "Dramatic Arts Theatre": "Arts & Culture", "Independent Filmmaking": "Arts & Culture", "Local Filmmakers": "Arts & Culture",
    "Musicals & Movies": "Arts & Culture", "Screenwriting": "Arts & Culture", "Scriptwriting": "Arts & Culture",
    "Short Stories": "Arts & Culture", "Storytelling": "Arts & Culture", "Visual Facilitation": "Arts & Culture",
    "Watercolor Painting": "Arts & Culture", "Acrylic Painting": "Arts & Culture", "Designers": "Arts & Culture",
    "Design Thinking": "Arts & Culture", "Graphic Facilitation": "Arts & Culture", "Graphic Recording": "Arts & Culture",
    "Interaction Design": "Arts & Culture", "Interactive Design": "Arts & Culture", "Product Design": "Arts & Culture",
    "UI/UX Design": "Arts & Culture", "UX Design": "Arts & Culture", "User Experience": "Arts & Culture",
    "User Research": "Arts & Culture", "Web Design": "Arts & Culture", "Architecture": "Arts & Culture",
    "Fashion Industry": "Arts & Culture", "Literature": "Arts & Culture", "Poetry": "Arts & Culture",
    "Shakespeare": "Arts & Culture", "Writing": "Arts & Culture", "Creative Writing": "Arts & Culture",
    "Essay Writing": "Arts & Culture", "Fiction Writing": "Arts & Culture", "Horror Writing": "Arts & Culture",
    "Non-Fiction Writing": "Arts & Culture", "Novel Writing": "Arts & Culture", "Writers": "Arts & Culture",
    "Writing Workshops": "Arts & Culture", "Writer's Block": "Arts & Culture", "Aspiring Writers": "Arts & Culture",
    "Authors": "Arts & Culture", "Book Club": "Arts & Culture", "Book Lovers": "Arts & Culture", 
    "Book Publishing": "Arts & Culture", "Book Swap": "Arts & Culture", "Book Writing": "Arts & Culture",
    "Books and Drinks": "Arts & Culture", "Books and Movies Discussions": "Arts & Culture", "Classic Books": "Arts & Culture",
    "Comics & Novels": "Arts & Culture", "English Books & Literature": "Arts & Culture", "Fantasy Books": "Arts & Culture",
    "Fiction": "Arts & Culture", "Fiction and Non-Fiction Reading": "Arts & Culture", "Harry Potter": "Arts & Culture",
    "Harry Potter Books": "Arts & Culture", "Horror Fiction": "Arts & Culture", "Indie Comics & Graphic Novels": "Arts & Culture",
    "Jane Austen": "Arts & Culture", "Novel Reading": "Arts & Culture", "Play Reading": "Arts & Culture",
    "Reading": "Arts & Culture", "Romance Novels": "Arts & Culture", "Science Fiction": "Arts & Culture",
    "Sci-Fi/Fantasy": "Arts & Culture", "Women's Book Club": "Arts & Culture", "Men's Book Club": "Arts & Culture",

    # Business & Career
    "Business": "Business & Career", "Business Agility": "Business & Career", "Business Analytics": "Business & Career",
    "Business Intelligence": "Business & Career", "Business Intelligence & Data Warehousing": "Business & Career",
    "Business Intelligence Tools": "Business & Career", "Business Management": "Business & Career",
    "Business Operations": "Business & Career", "Business Presentations": "Business & Career",
    "Business Referral Networking": "Business & Career", "Business Strategy": "Business & Career",
    "Career Coaching": "Business & Career", "Career Network": "Business & Career", "Coworking": "Business & Career",
    "Digital Marketing": "Business & Career", "Entrepreneur Networking": "Business & Career", "Entrepreneurship": "Business & Career",
    "Executive Coaching": "Business & Career", "Financial Engineering": "Business & Career", "Financial Freedom": "Business & Career",
    "Financial Independence": "Business & Career", "Forex Trading": "Business & Career", "Futures Trading": "Business & Career",
    "HR Professionals": "Business & Career", "High-Tech Ventures": "Business & Career", "Investing": "Business & Career",
    "Job Search": "Business & Career", "Landlords & Property Managers": "Business & Career", "Leadership": "Business & Career",
    "Leadership Development": "Business & Career", "Lean Management": "Business & Career", "Lean Project Management": "Business & Career",
    "Lean Startup": "Business & Career", "Making Money": "Business & Career", "Marketing": "Business & Career",
    "Marketing Strategy": "Business & Career", "Mentoring": "Business & Career", "Motivation & Success": "Business & Career",
    "Networking Happy Hour": "Business & Career", "New Career": "Business & Career", "Office 365": "Business & Career",
    "Online Marketing": "Business & Career", "Passive Income": "Business & Career", "Personal Finance": "Business & Career",
    "Presentations": "Business & Career", "Product Management": "Business & Career", "Professional Development": "Business & Career",
    "Professional Networking": "Business & Career", "Professional Women": "Business & Career", "Project Management": "Business & Career",
    "Real Estate": "Business & Career", "Real Estate Agents": "Business & Career", "Real Estate Investing": "Business & Career",
    "Real Estate Investors": "Business & Career", "Recruiting & Hiring": "Business & Career", "Resume, Cover Letters, Interview Help": "Business & Career",
    "Sales": "Business & Career", "Small Business": "Business & Career", "Small Business Marketing Strategy": "Business & Career",
    "Small Business Online Marketing": "Business & Career", "Social Media Marketing": "Business & Career",
    "Startup Businesses": "Business & Career", "Stock Trading": "Business & Career", "Stocks and Options": "Business & Career",
    "Strategy": "Business & Career", "Talent Acquisition": "Business & Career", "Trading": "Business & Career",
    "Trading Education": "Business & Career", "Venture Capital": "Business & Career", "Women Entrepreneurs": "Business & Career",
    "Women's Business Networking": "Business & Career", "Workforce Development": "Business & Career",
    "Agile Coaching": "Business & Career", "Agile Leadership": "Business & Career", "Agile Project Management": "Business & Career",
    "Agile and Scrum": "Business & Career", "Angel Investing": "Business & Career", "Beginner Real Estate Investing": "Business & Career",
    "Blogging for Business": "Business & Career", "Day Traders": "Business & Career", "Day Trading": "Business & Career",
    "Fix and Flip Real Estate": "Business & Career", "Hard Money Lending": "Business & Career", "Interview Skills": "Business & Career",
    "Scrum": "Business & Career", "Side Hustle": "Business & Career", "Starting an Online Business": "Business & Career",
    "Women in Blockchain": "Business & Career", "Women in Technology": "Business & Career",

    # Community & Environment
    "Animal Rights & Welfare": "Community & Environment", "Charitable Giving": "Community & Environment",
    "Charity": "Community & Environment", "Charity Events": "Community & Environment", "Clean-Up": "Community & Environment",
    "Community": "Community & Environment", "Community Building": "Community & Environment", "Conservation": "Community & Environment",
    "Donations": "Community & Environment", "Earth": "Community & Environment", "Global Warming": "Community & Environment",
    "It's My Park": "Community & Environment", "Local Wildlife": "Community & Environment", "Natural Environment": "Community & Environment",
    "Nature": "Community & Environment", "Nonprofit": "Community & Environment", "Open Street Partner Event": "Community & Environment",
    "Plaza Event": "Community & Environment", "Plaza Partner Event": "Community & Environment", "Social Impact": "Community & Environment",
    "Social Innovation": "Community & Environment", "Social Justice": "Community & Environment", "Sustainability": "Community & Environment",
    "Urban Park Rangers": "Community & Environment", "Vegetarian and Vegan Activism": "Community & Environment",
    "Volunteer": "Community & Environment", "Volunteering": "Community & Environment", "Volunteering and Charity Events": "Community & Environment",
    "Civic": "Community & Environment", "Politics": "Community & Environment", "Activism": "Community & Environment",
    "Nonviolence": "Community & Environment", "Street Event": "Community & Environment", "Production Event": "Community & Environment",
    "Special Event": "Community & Environment", "Parade": "Community & Environment", "Block Party": "Community & Environment",
    "Sidewalk Sale": "Community & Environment",

    # Family & Education
    "Education": "Family & Education", "Education & Technology": "Family & Education", "Families of Children who have ADD/ADHD": "Family & Education",
    "Family": "Family & Education", "Family Friendly": "Family & Education", "History": "Family & Education",
    "Historical Museum": "Family & Education", "Historical Tours": "Family & Education", "Local History & Culture": "Family & Education",
    "Natural History": "Family & Education", "Parents of Children with ADHD": "Family & Education", "Single Parents": "Family & Education",
    "Special Education": "Family & Education", "Stay-at-Home Moms": "Family & Education", "Working Dads": "Family & Education",
    "Working Moms": "Family & Education", "Divorced Parents": "Family & Education", "Language & Culture": "Family & Education",
    "Language Exchange": "Family & Education", "Language Learning": "Family & Education", "Learn Spanish": "Family & Education",
    "Bilingual Spanish/English": "Family & Education", "Brazilian Portuguese": "Family & Education", "Chinese Language": "Family & Education",
    "English": "Family & Education", "English as a Second Language": "Family & Education", "French": "Family & Education",
    "French Conversation": "Family & Education", "French Speakers": "Family & Education", "German": "Family & Education",
    "Hebrew": "Family & Education", "Italian": "Family & Education", "Japanese Food": "Family & Education", # Categorizing language/culture
    "Polyglot": "Family & Education", "Portuguese": "Family & Education", "Practice Spanish": "Family & Education",
    "Russian": "Family & Education", "Spanish": "Family & Education", "Spanish & English Language Exchange": "Family & Education",
    "Spanish Speakers": "Family & Education", "Lectures": "Family & Education", "Library": "Family & Education",
    "Scholarly Research Outside Academia": "Family & Education", "Science": "Family & Education", "Astronomy": "Family & Education",
    "Biology": "Family & Education", "Chemistry": "Family & Education", "Geology": "Family & Education", "Physics": "Family & Education",
    "Space Science": "Family & Education", "Cosmology": "Family & Education", "Archaeology": "Family & Education",
    "Biotechnology": "Family & Education", "Life Sciences": "Family & Education", "Neuroscience": "Family & Education",
    "Pharmaceutical Sciences": "Family & Education", "Research": "Family & Education", "Teaching": "Family & Education",
    "Tutoring": "Family & Education", "Workshops": "Family & Education", "Workshop Facilitation": "Family & Education",

    # Food & Drink
    "Beer": "Food & Drink", "Bars & Pubs": "Food & Drink", "Breakfast & Brunch": "Food & Drink",
    "Brunch, Lunch, Picnics": "Food & Drink", "Cafe Lovers": "Food & Drink", "Cocktails & Happy Hour": "Food & Drink",
    "Coffee": "Food & Drink", "Coffee & Books": "Food & Drink", "Coffee and Tea Socials": "Food & Drink",
    "Cooking": "Food & Drink", "Dining Out": "Food & Drink", "Dinner and a Movie": "Food & Drink",
    "Drinking": "Food & Drink", "Eating & Drinking": "Food & Drink", "Ethnic Food": "Food & Drink",
    "Exploring New Restaurants": "Food & Drink", "Farmers Market": "Food & Drink", "Food": "Food & Drink",
    "Foodie": "Food & Drink", "French Food": "Food & Drink", "Happy Hour": "Food & Drink", "Healthy Cooking": "Food & Drink",
    "Healthy Eating": "Food & Drink", "Italian Culture": "Food & Drink", # Often food related
    "Local Food": "Food & Drink", "Lunch": "Food & Drink", "Plant-Based Diet": "Food & Drink", "Raw Food": "Food & Drink",
    "Sushi": "Food & Drink", "Tea": "Food & Drink", "Vegan": "Food & Drink", "Vegetarian": "Food & Drink",
    "Wine": "Food & Drink", "Wine Lovers": "Food & Drink", "Wine Tasting": "Food & Drink", "Wine While Knitting": "Food & Drink",
    "Wine and Food Pairing": "Food & Drink", "Social Drinking": "Food & Drink",

    # Games & Hobbies
    "3D Gaming": "Games & Hobbies", "3D Printing": "Games & Hobbies", "Arduino": "Games & Hobbies",
    "Arts & Crafts": "Games & Hobbies", "Backgammon": "Games & Hobbies", "Backgammon Tournaments": "Games & Hobbies",
    "Bingo": "Games & Hobbies", "Board Games": "Games & Hobbies", "Card Games": "Games & Hobbies",
    "Card Making & Stamping": "Games & Hobbies", "Chess": "Games & Hobbies", "Comic Books": "Games & Hobbies",
    "Cooperative Board Games": "Games & Hobbies", "Crafts": "Games & Hobbies", "Crochet": "Games & Hobbies",
    "Cross Stitch": "Games & Hobbies", "DIY (Do It Yourself)": "Games & Hobbies", "DIY Technology": "Games & Hobbies",
    "Dungeons & Dragons": "Games & Hobbies", "Electronics": "Games & Hobbies", "Embroidery": "Games & Hobbies",
    "European Board Games": "Games & Hobbies", "Game Design": "Games & Hobbies", "Game Night": "Games & Hobbies",
    "Game Programming": "Games & Hobbies", "Games": "Games & Hobbies", "Gaming": "Games & Hobbies",
    "Geek Culture": "Games & Hobbies", "Handmade Crafts": "Games & Hobbies", "Horror Geeks": "Games & Hobbies",
    "Independent Game Development": "Games & Hobbies", "Indie Games": "Games & Hobbies", "Jewelry Making": "Games & Hobbies",
    "Knitter's Social": "Games & Hobbies", "Knitting": "Games & Hobbies", "Laser Cutting": "Games & Hobbies",
    "Makers": "Games & Hobbies", "Makerspaces": "Games & Hobbies", "Metalworking": "Games & Hobbies",
    "Microcontrollers": "Games & Hobbies", "Needlework": "Games & Hobbies", "Paper Crafts": "Games & Hobbies",
    "Retro Video Gaming": "Games & Hobbies", "Robotics": "Games & Hobbies", "Roleplaying Games (RPGs)": "Games & Hobbies",
    "Sewing": "Games & Hobbies", "Spades": "Games & Hobbies", "Strategy Board Games": "Games & Hobbies",
    "Strategy Games": "Games & Hobbies", "Tabletop Board Games": "Games & Hobbies", "Tabletop Role Playing and Board Games": "Games & Hobbies",
    "Trivia": "Games & Hobbies", "Video Game Design": "Games & Hobbies", "Video Game Development": "Games & Hobbies",
    "Video Games": "Games & Hobbies", "War Games": "Games & Hobbies", "Woodworking": "Games & Hobbies",
    "Yarn": "Games & Hobbies", "Bird Identification": "Games & Hobbies", "Bird Watching": "Games & Hobbies",
    "Birding": "Games & Hobbies", "Birds": "Games & Hobbies", "Gardening": "Games & Hobbies",

    # Health & Wellness
    "ADD/ADHD": "Health & Wellness", "ADHD": "Health & Wellness", "ADHD Parents with ADHD Children": "Health & Wellness",
    "Adult ADD/ADHD": "Health & Wellness", "Alternative Medicine": "Health & Wellness", "Anxiety": "Health & Wellness",
    "Behavioral Psychology": "Health & Wellness", "Breathing Meditation": "Health & Wellness", "Buddhist Meditation": "Health & Wellness",
    "Confidence": "Health & Wellness", "Confidence and Self-Esteem": "Health & Wellness", "Depression": "Health & Wellness",
    "Emotional Healing": "Health & Wellness", "Emotional Intelligence": "Health & Wellness", "Energy Healing": "Health & Wellness",
    "Grief Support": "Health & Wellness", "Group Coaching": "Health & Wellness", "Guided Meditation": "Health & Wellness",
    "Healing": "Health & Wellness", "Healing Breathwork": "Health & Wellness", "Health Fair": "Health & Wellness",
    "Healthcare Reform": "Health & Wellness", "Healthy Family and Healthy Environment": "Health & Wellness",
    "Healthy Living": "Health & Wellness", "Holistic Health": "Health & Wellness", "Hypnosis and Hypnotherapy": "Health & Wellness",
    "Life Coaching": "Health & Wellness", "Life Mastery": "Health & Wellness", "Life Transformation": "Health & Wellness",
    "Meditation": "Health & Wellness", "Men's Mental Health": "Health & Wellness", "Mental Health Professionals": "Health & Wellness",
    "Mental and Emotional Wellnes": "Health & Wellness", "Mind Body Wellness": "Health & Wellness", "Mindful Living": "Health & Wellness",
    "Mindfulness": "Health & Wellness", "Mindfulness Meditation": "Health & Wellness", "Mindfulness Training": "Health & Wellness",
    "Mindfulness in Nature": "Health & Wellness", "Mindfulness-based Stress Reduction": "Health & Wellness",
    "Narcissism Awareness": "Health & Wellness", "Negative Emotions": "Health & Wellness", "Overcome Fears": "Health & Wellness",
    "Personal Development": "Health & Wellness", "Personal Growth": "Health & Wellness", "Personal Improvement": "Health & Wellness",
    "Physical & Mental Wellness": "Health & Wellness", "Positive Thinking": "Health & Wellness", "Psychedelic Assisted Therapy": "Health & Wellness",
    "Psychedelic Integration": "Health & Wellness", "Psychology": "Health & Wellness", "Reduce Stress": "Health & Wellness",
    "Reiki": "Health & Wellness", "Self Exploration": "Health & Wellness", "Self Expression": "Health & Wellness",
    "Self Knowledge & Self Awareness": "Health & Wellness", "Self-Awareness": "Health & Wellness", "Self-Care": "Health & Wellness",
    "Self-Empowerment": "Health & Wellness", "Self-Help & Self-Improvement": "Health & Wellness", "Self-Love & Self-Acceptance": "Health & Wellness",
    "Social Anxiety": "Health & Wellness", "Stress Management": "Health & Wellness", "Stress Relief": "Health & Wellness",
    "Success Mindset": "Health & Wellness", "Support": "Health & Wellness", "Support Group": "Health & Wellness",
    "Toxic Relationships": "Health & Wellness", "Wellness": "Health & Wellness", "Wellness Coaching": "Health & Wellness",
    "Women's Health and Wellness": "Health & Wellness", "Achieving Goals": "Health & Wellness", "Getting Organized": "Health & Wellness",
    "Memory Training": "Health & Wellness",

    # Music & Performance
    "80's Dancing": "Music & Performance", "80's Music": "Music & Performance", "A Cappella": "Music & Performance",
    "Ableton Live": "Music & Performance", "Adult Amateur Pianists": "Music & Performance", "Banjo Player": "Music & Performance",
    "Barbershop Chorus": "Music & Performance", "Baroque Music": "Music & Performance", "Beginner Piano": "Music & Performance",
    "Blues": "Music & Performance", "Chamber Music": "Music & Performance", "Christmas Caroling & Music": "Music & Performance",
    "Classical Music": "Music & Performance", "Classical Piano": "Music & Performance", "Comedy Club": "Music & Performance",
    "Comedy Show": "Music & Performance", "Concerts": "Music & Performance", "Dance": "Music & Performance",
    "Dance Parties": "Music & Performance", "Dancing": "Music & Performance", "Early Music": "Music & Performance",
    "Electric Guitar": "Music & Performance", "Electronic Dance Music": "Music & Performance", "Electronic Music": "Music & Performance",
    "Electronic Music Production": "Music & Performance", "Fiddle": "Music & Performance", "Grateful Dead": "Music & Performance",
    "Group Singing": "Music & Performance", "Guitar": "Music & Performance", "Improv": "Music & Performance",
    "Improv Comedy": "Music & Performance", "Jam Band": "Music & Performance", "Jam Sessions": "Music & Performance",
    "Jazz": "Music & Performance", "Jazz Jams": "Music & Performance", "Jazz Musicians": "Music & Performance",
    "Jazz Piano": "Music & Performance", "Jazz Standards": "Music & Performance", "Karaoke": "Music & Performance",
    "Keyboardist": "Music & Performance", "Latin Dance": "Music & Performance", "Listening To Music": "Music & Performance",
    "Live Music": "Music & Performance", "Music": "Music & Performance", "Music Industry": "Music & Performance",
    "Music Production": "Music & Performance", "Musicians": "Music & Performance", "Partner Dancing": "Music & Performance",
    "Piano": "Music & Performance", "Piano Lessons": "Music & Performance", "Piano Performances": "Music & Performance",
    "Salsa Lessons": "Music & Performance", "Singing": "Music & Performance", "Social Dancing": "Music & Performance",
    "Soul Music": "Music & Performance", "Stand-up Comedy": "Music & Performance", "Vinyl Records": "Music & Performance",
    "Acting": "Music & Performance", "Beginners Acting Training": "Music & Performance", "Drama": "Music & Performance",
    "Drama and Comedy Stories": "Music & Performance",

    # Science & Technology
    ".NET": "Science & Technology", "3D Artists": "Science & Technology", "AI Algorithms": "Science & Technology",
    "AI and Society": "Science & Technology", "AI/ML": "Science & Technology", "API": "Science & Technology",
    "Adobe Lightroom": "Science & Technology", "Android": "Science & Technology", "Angular": "Science & Technology",
    "Apache Spark": "Science & Technology", "Application Security": "Science & Technology", "Artificial Intelligence": "Science & Technology",
    "Artificial Intelligence Applications": "Science & Technology", "Augmented Reality": "Science & Technology",
    "Automation": "Science & Technology", "Bayesian Statistics": "Science & Technology", "Big Data": "Science & Technology",
    "Biostatistics": "Science & Technology", "Bitcoin": "Science & Technology", "Blockchain": "Science & Technology",
    "C#": "Science & Technology", "CG Animation": "Science & Technology", "CISO": "Science & Technology",
    "CNC": "Science & Technology", "Cloud Computing": "Science & Technology", "Cloud Security": "Science & Technology",
    "Computer Programming": "Science & Technology", "Computer Security": "Science & Technology", "Conversational AI": "Science & Technology",
    "Cryptocurrency": "Science & Technology", "Cryptography": "Science & Technology", "Cybersecurity": "Science & Technology",
    "Dart Language": "Science & Technology", "Data Analytics": "Science & Technology", "Data Center and Operations Automation": "Science & Technology",
    "Data Engineering": "Science & Technology", "Data Integration": "Science & Technology", "Data Management": "Science & Technology",
    "Data Mining": "Science & Technology", "Data Science": "Science & Technology", "Data Science using Python": "Science & Technology",
    "Data Visualization": "Science & Technology", "Database Administrators": "Science & Technology", "Database Applications": "Science & Technology",
    "Database Development": "Science & Technology", "Database Professionals": "Science & Technology", "Decentralized Systems & Applications": "Science & Technology",
    "Deep Learning": "Science & Technology", "DevOps": "Science & Technology", "DevOps Automation": "Science & Technology",
    "Disruptive innovation": "Science & Technology", "E-Learning": "Science & Technology", "ETL": "Science & Technology",
    "Emerging Technology": "Science & Technology", "Ethereum": "Science & Technology", "Flutter": "Science & Technology",
    "Github": "Science & Technology", "Google": "Science & Technology", "Google Cloud": "Science & Technology",
    "Hacking": "Science & Technology", "Human-Computer Interaction": "Science & Technology", "IT Professionals": "Science & Technology",
    "Immersive Tech": "Science & Technology", "Information Architecture": "Science & Technology", "Information Security": "Science & Technology",
    "Information Technology": "Science & Technology", "Infrastructure as Code": "Science & Technology", "Internet Professionals": "Science & Technology",
    "Internet Startups": "Science & Technology", "Internet of Things (IOT)": "Science & Technology", "JavaScript": "Science & Technology",
    "Learn to Code": "Science & Technology", "Linux": "Science & Technology", "Machine Learning": "Science & Technology",
    "Mesh Networks": "Science & Technology", "Microsoft": "Science & Technology", "Microsoft Azure": "Science & Technology",
    "Microsoft Excel": "Science & Technology", "Mobile Development": "Science & Technology", "Mobile Technology": "Science & Technology",
    "Network Security": "Science & Technology", "New Technology": "Science & Technology", "NoSQL": "Science & Technology",
    "OWASP": "Science & Technology", "Oculus Rift": "Science & Technology", "Open Source": "Science & Technology",
    "Oracle": "Science & Technology", "PaaS (Platform as a Service)": "Science & Technology", "Performance Monitoring": "Science & Technology",
    "Photoshop": "Science & Technology", "PostgreSQL": "Science & Technology", "Power BI": "Science & Technology",
    "Predictive Analytics": "Science & Technology", "Programming in R": "Science & Technology", "Puppet Software": "Science & Technology",
    "Python": "Science & Technology", "Python Web Development": "Science & Technology", "R Project for Statistical Computing": "Science & Technology",
    "R-Ladies": "Science & Technology", "Rust": "Science & Technology", "Rustlang": "Science & Technology",
    "SQL Azure": "Science & Technology", "Security Analysis": "Science & Technology", "Serverless Architecture": "Science & Technology",
    "Site Reliability Engineering (SRE)": "Science & Technology", "Software Development": "Science & Technology",
    "Software Engineering": "Science & Technology", "Software Security": "Science & Technology", "Swift Language": "Science & Technology",
    "System Administration": "Science & Technology", "Tech Talks": "Science & Technology", "Technical Analysis": "Science & Technology",
    "Technical Writers": "Science & Technology", "Technology": "Science & Technology", "Technology Professionals": "Science & Technology",
    "Technology Startups": "Science & Technology", "Unreal Engine": "Science & Technology", "Usability": "Science & Technology",
    "Video Editing": "Science & Technology", "Virtual Reality (VR)": "Science & Technology", "Virtual Worlds": "Science & Technology",
    "Virtual/Online Events": "Science & Technology", "Visual Studio": "Science & Technology", "Visualization": "Science & Technology",
    "Web Application": "Science & Technology", "Web Application Security": "Science & Technology", "Web Development": "Science & Technology",
    "Web Security": "Science & Technology", "Web Technology": "Science & Technology", "White Hat Hacking": "Science & Technology",
    "Wi-Fi": "Science & Technology", "Women Programmers": "Science & Technology", "Youtube": "Science & Technology",
    "iOS": "Science & Technology", "iOS Development": "Science & Technology",

    # Social & Networking
    "20's-30's": "Social & Networking", "20's-40's": "Social & Networking", "Asian Americans": "Social & Networking",
    "Asian Culture": "Social & Networking", "Asian Professionals": "Social & Networking", "Asian Singles": "Social & Networking",
    "Asians": "Social & Networking", "Baby Boomers": "Social & Networking", "Black Culture": "Social & Networking",
    "Brazilian Culture": "Social & Networking", "Build Better Relationships": "Social & Networking", "Communication": "Social & Networking",
    "Communication Skills": "Social & Networking", "Connection": "Social & Networking", "Conversation": "Social & Networking",
    "Cultural Activities": "Social & Networking", "Culture": "Social & Networking", "Culture Exchange": "Social & Networking",
    "Dating Advice": "Social & Networking", "Dating Again": "Social & Networking", "Dating Coaching": "Social & Networking",
    "Dating Over 40": "Social & Networking", "Dating Women": "Social & Networking", "Dating and Relationships": "Social & Networking",
    "Daytime Women's Social": "Social & Networking", "Desi Singles": "Social & Networking", "Divorced": "Social & Networking",
    "Divorced Women": "Social & Networking", "Entrepreneur Dating": "Social & Networking", "European Culture": "Social & Networking",
    "Expat": "Social & Networking", "Expat Brazilian": "Social & Networking", "Expat French": "Social & Networking",
    "Expat Italian": "Social & Networking", "Expat Portuguese": "Social & Networking", "Filipino Culture": "Social & Networking",
    "Flirting": "Social & Networking", "Francophiles": "Social & Networking", "Francophone Culture": "Social & Networking",
    "Free Events": "Social & Networking", "Free in New York City": "Social & Networking", "Friendship for the Lonely": "Social & Networking",
    "Friendships": "Social & Networking", "Fun Times": "Social & Networking", "Fun and Laughter": "Social & Networking",
    "Gay": "Social & Networking", "Gay Dating": "Social & Networking", "Gay Friends": "Social & Networking",
    "Gay Men": "Social & Networking", "Gay Professionals": "Social & Networking", "Gay Singles": "Social & Networking",
    "Gay Social Networking": "Social & Networking", "Gay and Lesbian Friends": "Social & Networking", "Generation X": "Social & Networking",
    "Girlfriends": "Social & Networking", "Girls Having Fun": "Social & Networking", "Girls' Night Out": "Social & Networking",
    "Hanging Out": "Social & Networking", "Happiness": "Social & Networking", "Holiday Parties": "Social & Networking",
    "Holidays": "Social & Networking", "Improving Relationships": "Social & Networking", "Indian Singles": "Social & Networking",
    "International Friends": "Social & Networking", "International and Exchange Students": "Social & Networking",
    "Introverted": "Social & Networking", "Introverts Meeting Friends": "Social & Networking", "LGBT": "Social & Networking",
    "LGBT Social": "Social & Networking", "LGBT+": "Social & Networking", "Latino Culture": "Social & Networking",
    "Lesbian": "Social & Networking", "Lesbian Dating": "Social & Networking", "Lesbian Friends": "Social & Networking",
    "Life Discussions": "Social & Networking", "Like Minded People": "Social & Networking", "Live Your Best Life": "Social & Networking",
    "Local Activities": "Social & Networking", "Locals & New in Town": "Social & Networking", "Loneliness": "Social & Networking",
    "Love & Happiness": "Social & Networking", "Make New Friends": "Social & Networking", "Matchmaking Service": "Social & Networking",
    "Men's Social": "Social & Networking", "Mix and Mingle": "Social & Networking", "New In Town": "Social & Networking",
    "Newly Divorced": "Social & Networking", "Nightlife": "Social & Networking", "Over 45": "Social & Networking",
    "Over 50": "Social & Networking", "Parties & Socializing": "Social & Networking", "Portuguese Culture": "Social & Networking",
    "Queer Socializing": "Social & Networking", "Relationship Building": "Social & Networking", "Relationship Coaching": "Social & Networking",
    "Seniors": "Social & Networking", "Shyness": "Social & Networking", "Single Professionals": "Social & Networking",
    "Single and Dating Again": "Social & Networking", "Singles": "Social & Networking", "Singles 20's-30's": "Social & Networking",
    "Singles 20's-40's": "Social & Networking", "Singles 30's-40's": "Social & Networking", "Singles 30's-50's": "Social & Networking",
    "Singles 40's-50's": "Social & Networking", "Singles Over 40": "Social & Networking", "Singles Over 50": "Social & Networking",
    "Social": "Social & Networking", "Social Networking": "Social & Networking", "Socializing": "Social & Networking",
    "Soul Connection": "Social & Networking", "Spanish Culture": "Social & Networking", "Successful Relationships": "Social & Networking",
    "Thought-Provoking Conversations": "Social & Networking", "Turkish Culture": "Social & Networking", "Ukraine": "Social & Networking",
    "West Africa": "Social & Networking", "Winter Holidays": "Social & Networking", "Women 20's-30's": "Social & Networking",
    "Women Friends": "Social & Networking", "Women Over 40": "Social & Networking", "Women Over 50": "Social & Networking",
    "Women's Empowerment": "Social & Networking", "Women's Networking": "Social & Networking", "Women's Social": "Social & Networking",
    "Young Professional Singles": "Social & Networking", "Young Professionals": "Social & Networking",

    # Sports & Fitness
    "Athletic Race / Tour": "Sports & Fitness", "Badminton": "Sports & Fitness", "Basketball": "Sports & Fitness",
    "Beginners Running": "Sports & Fitness", "Bicycling": "Sports & Fitness", "Bowling": "Sports & Fitness",
    "Co-ed Soccer": "Sports & Fitness", "Coached Badminton": "Sports & Fitness", "Cross-Country Skiing": "Sports & Fitness",
    "Cycling": "Sports & Fitness", "Dodgeball": "Sports & Fitness", "Doubles Badminton": "Sports & Fitness",
    "European Football": "Sports & Fitness", "Exercise": "Sports & Fitness", "Exercise and Fun": "Sports & Fitness",
    "Experienced Soccer Players": "Sports & Fitness", "Figure Skating": "Sports & Fitness", "Fitness": "Sports & Fitness",
    "Free Running": "Sports & Fitness", "Fun Run": "Sports & Fitness", "Futbol": "Sports & Fitness",
    "Gay Mens Fitness": "Sports & Fitness", "Gentle Yoga": "Sports & Fitness", "Group Fitness Training": "Sports & Fitness",
    "Hockey": "Sports & Fitness", "Ice Climbing": "Sports & Fitness", "Ice Hockey": "Sports & Fitness",
    "Ice Skating": "Sports & Fitness", "Indoor Basketball": "Sports & Fitness", "Inline Skating": "Sports & Fitness",
    "Jogging Friends": "Sports & Fitness", "Kayaking": "Sports & Fitness", "Men's Basketball": "Sports & Fitness",
    "Men's Pickup Basketball": "Sports & Fitness", "Mens Soccer": "Sports & Fitness", "Outdoor Fitness": "Sports & Fitness",
    "Outdoor Rollerblading": "Sports & Fitness", "Outdoor Soccer": "Sports & Fitness", "Pickup Badminton": "Sports & Fitness",
    "Pickup Basketball": "Sports & Fitness", "Pickup Soccer": "Sports & Fitness", "Pilates": "Sports & Fitness",
    "Ping Pong": "Sports & Fitness", "Ping Pong for Singles": "Sports & Fitness", "Recreation Center Programming": "Sports & Fitness",
    "Recreational Soccer": "Sports & Fitness", "Recreational Sports": "Sports & Fitness", "Road Cycling": "Sports & Fitness",
    "Road Running": "Sports & Fitness", "Rock Climbing": "Sports & Fitness", "Roller Blading": "Sports & Fitness",
    "Roller Hockey": "Sports & Fitness", "Roller Skating": "Sports & Fitness", "Running": "Sports & Fitness",
    "Running Partners & Groups": "Sports & Fitness", "Running/Jogging": "Sports & Fitness", "Saturday Badminton": "Sports & Fitness",
    "Skating": "Sports & Fitness", "Skiing": "Sports & Fitness", "Snowboarding": "Sports & Fitness",
    "Snowsports": "Sports & Fitness", "Soccer": "Sports & Fitness", "Sport - Adult": "Sports & Fitness",
    "Sport - Youth": "Sports & Fitness", "Sports and Recreation": "Sports & Fitness", "Sports and Socials": "Sports & Fitness",
    "Sunday Badminton": "Sports & Fitness", "Table Tennis": "Sports & Fitness", "Volleyball Social": "Sports & Fitness",
    "Walking for Fitness": "Sports & Fitness", "Womens Soccer": "Sports & Fitness", "Yoga": "Sports & Fitness",
    "Yoga & Meditation": "Sports & Fitness",

    # Spirituality & Religion
    "Agnostic": "Spirituality & Religion", "Ancient Philosophy": "Spirituality & Religion", "Astrology": "Spirituality & Religion",
    "Atheist": "Spirituality & Religion", "Buddhism": "Spirituality & Religion", "Consciousness": "Spirituality & Religion",
    "Dreaming Consciously": "Spirituality & Religion", "Eckankar": "Spirituality & Religion", "Engaged Buddhism": "Spirituality & Religion",
    "Ethics": "Spirituality & Religion", "Free Thinker": "Spirituality & Religion", "Humanism": "Spirituality & Religion",
    "Inner Peace": "Spirituality & Religion", "Intuition": "Spirituality & Religion", "Lucid Dreaming": "Spirituality & Religion",
    "Metaphysics": "Spirituality & Religion", "Morality and Ethics": "Spirituality & Religion", "Myers-Briggs Type Indicator": "Spirituality & Religion",
    "Past Lives": "Spirituality & Religion", "Personality Theory": "Spirituality & Religion", "Personality Type": "Spirituality & Religion",
    "Philosophy": "Spirituality & Religion", "Pranayama": "Spirituality & Religion", "Psychic": "Spirituality & Religion",
    "Psychic & Spiritual Matters": "Spirituality & Religion", "Psychic Development & Readings": "Spirituality & Religion",
    "Rationality and Reasoning": "Spirituality & Religion", "Religious Event": "Spirituality & Religion",
    "Science and Spirituality": "Spirituality & Religion", "Secularism": "Spirituality & Religion", "Skeptics": "Spirituality & Religion",
    "Spiritual Awakening": "Spirituality & Religion", "Spiritual Growth": "Spirituality & Religion", "Spiritual Healing": "Spirituality & Religion",
    "Spiritualism": "Spirituality & Religion", "Spirituality": "Spirituality & Religion", "Stoicism": "Spirituality & Religion",
    "Tarot": "Spirituality & Religion",

    # Travel & Outdoor
    "Adventure": "Travel & Outdoor", "Adventure Travel": "Travel & Outdoor", "Backpacking": "Travel & Outdoor",
    "Beach": "Travel & Outdoor", "Camping": "Travel & Outdoor", "City Walks": "Travel & Outdoor",
    "Daytrips to the Mountains": "Travel & Outdoor", "Exploring": "Travel & Outdoor", "Exploring the City": "Travel & Outdoor",
    "Hiking": "Travel & Outdoor", "Hill Walking": "Travel & Outdoor", "Himalayas": "Travel & Outdoor",
    "Historic Locations": "Travel & Outdoor", "Nature Photography": "Travel & Outdoor", "Nature Walks": "Travel & Outdoor",
    "Outdoors": "Travel & Outdoor", "Picnics": "Travel & Outdoor", "Sightseeing": "Travel & Outdoor",
    "Tours": "Travel & Outdoor", "Travel": "Travel & Outdoor", "Urban Exploration": "Travel & Outdoor",
    "Urban Foraging": "Travel & Outdoor", "Walking": "Travel & Outdoor", "Walking Tours": "Travel & Outdoor",
    "Walking with Friends": "Travel & Outdoor", "Weekend Adventures": "Travel & Outdoor", "Wilderness Hiking": "Travel & Outdoor",
    "Women Who Travel": "Travel & Outdoor",

    # Other / Miscellaneous
    "Category not found": "Other / Miscellaneous", "Miscellaneous": "Other / Miscellaneous", "N/A": "Other / Miscellaneous",
    "Astoria": "Other / Miscellaneous", "Brooklyn": "Other / Miscellaneous", "Bucks County": "Other / Miscellaneous",
    "DMV": "Other / Miscellaneous", "Long Island City": "Other / Miscellaneous", "Manhattan": "Other / Miscellaneous",
    "NYC": "Other / Miscellaneous", "New York City": "Other / Miscellaneous", "Queens": "Other / Miscellaneous",
    "Washington DC": "Other / Miscellaneous", "Remote Workers": "Other / Miscellaneous", "Facilitation": "Other / Miscellaneous",
    "Group Facilitation": "Other / Miscellaneous", "Meeting Facilitation": "Other / Miscellaneous", "Organizing": "Other / Miscellaneous",
    "Public Speaker Training": "Other / Miscellaneous", "Public Speaking": "Other / Miscellaneous", "Toastmasters": "Other / Miscellaneous",
    "Impromptu Speaking": "Other / Miscellaneous", "Fear of Public Speaking": "Other / Miscellaneous",
    "Critical Thinking": "Other / Miscellaneous", "Intellectual Curiosity": "Other / Miscellaneous", "Intellectual Discussions": "Other / Miscellaneous",
    "Learning": "Other / Miscellaneous", "Creativity": "Other / Miscellaneous", "Creative Circle": "Other / Miscellaneous",
    "Art Journaling": "Other / Miscellaneous", "Journaling": "Other / Miscellaneous", "Critique Group": "Other / Miscellaneous",
    "Modeling": "Other / Miscellaneous", "Group Photo Shoots": "Other / Miscellaneous", "Human-Centered Design": "Other / Miscellaneous",
    "Design Research": "Other / Miscellaneous", "Sociology": "Other / Miscellaneous", "African Culture": "Other / Miscellaneous",
    "Intentional Communities": "Other / Miscellaneous", "Mathematics": "Other / Miscellaneous", "Evolution": "Other / Miscellaneous",
    "Anthropology": "Other / Miscellaneous", "Politics": "Other / Miscellaneous", "Government": "Other / Miscellaneous",
    "Law": "Other / Miscellaneous", "Legal": "Other / Miscellaneous", "Crime": "Other / Miscellaneous",
    "True Crime": "Other / Miscellaneous", "Mystery": "Other / Miscellaneous", "Scary Movies": "Other / Miscellaneous",
    "Horror Films": "Other / Miscellaneous", "Lawn closure": "Other / Miscellaneous", "Closure": "Other / Miscellaneous"
}

def get_parent_category(category_input):
    """
    Maps a category string or list of strings to a parent category.
    Returns a single string representing the parent category.
    """
    if not category_input:
        return "Other / Miscellaneous"

    # Handle list of categories (e.g. from Meetup)
    if isinstance(category_input, list):
        # Try to find the first valid mapping
        for cat in category_input:
            if cat in CATEGORY_MAPPING:
                return CATEGORY_MAPPING[cat]
        # If no mapping found, return Other
        return "Other / Miscellaneous"
    
    # Handle single string
    if isinstance(category_input, str):
        cat = category_input.strip()
        if cat in CATEGORY_MAPPING:
            return CATEGORY_MAPPING[cat]
        
        # Fallback for partial matches or unmapped
        # Check if it's a closure or park specific thing
        if "Closure" in cat or "closure" in cat:
            return "Other / Miscellaneous"
        
        return "Other / Miscellaneous"

    return "Other / Miscellaneous"

def process_files():
    input_dir = 'event_data_normalized'
    output_dir = 'event_data_with_parent_categories'
    
    files_config = [
        {
            'filename': 'eventbrite_events_normalized.json',
            'field': 'category'
        },
        {
            'filename': 'meetup_events_normalized.json',
            'field': 'Categories'
        },
        {
            'filename': 'nyc_park_events_normalized.json',
            'field': 'category'
        },
        {
            'filename': 'permitted_events_normalized.json',
            'field': 'category'
        }
    ]
    
    for config in files_config:
        input_path = os.path.join(input_dir, config['filename'])
        output_path = os.path.join(output_dir, config['filename'])
        
        if not os.path.exists(input_path):
            print(f"Warning: {input_path} not found.")
            continue
            
        print(f"Processing {config['filename']}...")
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            processed_data = []
            for item in data:
                # Get the category value
                cat_value = item.get(config['field'])
                
                # Determine parent category
                parent_cat = get_parent_category(cat_value)
                
                # Add new field
                item['parent_category'] = parent_cat
                processed_data.append(item)
                
            # Write to new file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=4)
                
            print(f"Successfully processed {len(processed_data)} events to {output_path}")
            
        except Exception as e:
            print(f"Error processing {config['filename']}: {e}")

if __name__ == "__main__":
    process_files()
