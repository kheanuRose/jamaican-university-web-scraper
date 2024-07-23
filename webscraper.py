import requests
from bs4 import BeautifulSoup
import csv
from pymongo import MongoClient
from datetime import datetime

UCC_URL = "https://ucc.edu.jm/programmes/undergraduate"

# UTech URLs
UTECH_BASE_URL = "https://www.utech.edu.jm"
UTECH_ENDPOINTS = {
    "COHS": "/academics/colleges-faculties/cohs/mod-guide",
    "COBAM": "/academics/colleges-faculties/cobam/courses-of-study",
    "FELS": "/academics/colleges-faculties/fels/mod-guide",
    "FENC": "/academics/colleges-faculties/fenc/mod-guide",
    "FOL": "/academics/colleges-faculties/fol/mod-guide",
    "FOSS": "/academics/colleges-faculties/foss/mod-guide",
    "FOBE": "/academics/colleges-faculties/fobe/mod-guide",
    "JOINT": "/academics/colleges-faculties/joint/mod-guide"
}

THEMICO_URL = "https://themico.edu.jm/academics/undergraduate-programmes/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['college', 'faculty', 'programme', 'awarding_institution', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def save_to_mongodb(data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['jamaican_colleges']
    
    # Create or get collections for each college
    ucc_collection = db['ucc']
    utech_collection = db['utech']
    mico_collection = db['mico']
    
    # Separate data by college
    ucc_data = [program for program in data if program['college'] == 'UCC']
    utech_data = [program for program in data if program['college'] == 'UTech']
    mico_data = [program for program in data if program['college'] == 'The Mico University College']
    
    # Insert data into respective collections
    if ucc_data:
        ucc_collection.insert_many(ucc_data)
    if utech_data:
        utech_collection.insert_many(utech_data)
    if mico_data:
        mico_collection.insert_many(mico_data)
    
    client.close()

def scrape_ucc_table(table, table_name):
    programs = []
    if table:
        program_rows = table.find_all('tr')
        for row in program_rows:
            columns = row.find_all('td')
            if len(columns) >= 2:
                title = columns[0].text.strip()
                institution = columns[1].text.strip()
                link = columns[0].find('a')['href'] if columns[0].find('a') else "N/A"
                programs.append({
                    'college': 'UCC',
                    'faculty': table_name,
                    'programme': title,
                    'awarding_institution': institution,
                    'link': link
                })
    return programs

def scrape_utech_programs():
    all_programs = []
    for program, endpoint in UTECH_ENDPOINTS.items():
        full_url = UTECH_BASE_URL + endpoint
        try:
            response = requests.get(full_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if program == "COHS":
                programs = scrape_cohs_programs(soup, full_url)
            elif program == "COBAM":
                programs = scrape_cobam_soba_programs(soup, full_url)
            elif program == "FELS":
                programs = scrape_fels_programs(soup, full_url)
            elif program == "FENC":
                programs = scrape_fenc_programs(soup, full_url)
            elif program == "FOL":
                programs = scrape_fol_programs(soup, full_url)
            elif program == "FOSS":
                programs = scrape_foss_programs(soup, full_url)
            elif program == "FOBE":
                programs = scrape_fobe_programs(soup, full_url)
            elif program == "JOINT":
                programs = scrape_joint_programs(soup, full_url)
            
            all_programs.extend(programs)
            
        except requests.RequestException as e:
            print(f"An error occurred while fetching the UTech {program} page: {e}")
    
    return all_programs

def scrape_cohs_programs(soup, url):
    programs = []
    content_div = soup.find('div', id='parent-fieldname-text-b9dc1e14ccf7482aa5b7ff6e7bbf1123')
    if content_div:
        schools = content_div.find_all(['p', 'strong'], string=lambda text: text and any(school in text.strip() for school in ['Caribbean School', 'School of']))
        
        for school in schools:
            current_element = school.find_next()
            while current_element and current_element.name != 'p' and 'School of' not in current_element.text:
                if current_element.name == 'ul':
                    program_items = current_element.find_all('li')
                    for program in program_items:
                        title = program.text.strip()
                        link = program.find('a')['href'] if program.find('a') else "N/A"
                        if link != "N/A":
                            link = UTECH_BASE_URL + link if not link.startswith('http') else link
                        programs.append({
                            'college': 'UTech',
                            'faculty': 'College of Health Sciences (COHS)',
                            'programme': title,
                            'awarding_institution': 'UTech',
                            'link': link
                        })
                current_element = current_element.find_next()
    return programs

def scrape_cobam_soba_programs(soup, url):
    programs = []
    soba_section = soup.find('h3', string=lambda text: text and "School of Business Administration (SOBA)" in text)
    if soba_section:
        ul_element = soba_section.find_next('ul')
        if ul_element:
            program_items = ul_element.find_all('li')
            for program in program_items:
                link = program.find('a')
                if link:
                    title = link.text.strip()
                    href = link.get('href', '')
                    full_href = UTECH_BASE_URL + href if not href.startswith('http') else href
                    programs.append({
                        'college': 'UTech',
                        'faculty': 'College of Business and Management (COBAM) - School of Business Administration (SOBA)',
                        'programme': title,
                        'awarding_institution': 'UTech',
                        'link': full_href
                    })
    return programs

def scrape_fels_programs(soup, url):
    programs = []
    content_div = soup.find('div', id='parent-fieldname-text-9cdf8186a39945f8ad56b6fe26f0aac8')
    if content_div:
        program_lists = content_div.find_all('ul')
        for program_list in program_lists:
            items = program_list.find_all('li')
            for item in items:
                title = item.text.strip()
                link = item.find('a')['href'] if item.find('a') else "N/A"
                if link != "N/A":
                    link = UTECH_BASE_URL + link if not link.startswith('http') else link
                programs.append({
                    'college': 'UTech',
                    'faculty': 'Faculty of Education and Liberal Studies (FELS)',
                    'programme': title,
                    'awarding_institution': 'UTech',
                    'link': link
                })
    return programs

def scrape_fenc_programs(soup, url):
    programs = []
    content_div = soup.find('div', id='parent-fieldname-text-20df11077c244ed588c7ccaacfde7723')
    if content_div:
        sections = content_div.find_all('h3')
        for section in sections:
            section_name = section.text.strip()
            ul_element = section.find_next('ul')
            if ul_element:
                program_items = ul_element.find_all('li')
                for program in program_items:
                    link = program.find('a')
                    if link:
                        title = link.text.strip()
                        href = link.get('href', '')
                        full_href = UTECH_BASE_URL + href if not href.startswith('http') else href
                        programs.append({
                            'college': 'UTech',
                            'faculty': f'Faculty of Engineering and Computing (FENC) - {section_name}',
                            'programme': title,
                            'awarding_institution': 'UTech',
                            'link': full_href
                        })
    return programs

def scrape_fol_programs(soup, url):
    programs = []
    content_div = soup.find('div', id='parent-fieldname-text-3fe23d5d6f514be7858810ba554a52eb')
    if content_div:
        program_link = content_div.find('a')
        if program_link:
            title = program_link.text.strip()
            link = program_link['href']
            link = UTECH_BASE_URL + link if not link.startswith('http') else link
            programs.append({
                'college': 'UTech',
                'faculty': 'Faculty of Law (FOL)',
                'programme': title,
                'awarding_institution': 'UTech',
                'link': link
            })
    return programs

def scrape_foss_programs(soup, url):
    programs = []
    content_div = soup.find('div', id='parent-fieldname-text-4bbc51f92183484bb2d3fc2fd02cdf1d')
    if content_div:
        sections = content_div.find_all('h3')
        for section in sections:
            section_name = section.text.strip()
            ul_element = section.find_next('ul')
            if ul_element:
                program_items = ul_element.find_all('li')
                for program in program_items:
                    link = program.find('a')
                    if link:
                        title = link.text.strip()
                        href = link.get('href', '')
                        full_href = UTECH_BASE_URL + href if not href.startswith('http') else href
                        programs.append({
                            'college': 'UTech',
                            'faculty': f'Faculty of Science and Sport (FOSS) - {section_name}',
                            'programme': title,
                            'awarding_institution': 'UTech',
                            'link': full_href
                        })
    return programs

def scrape_fobe_programs(soup, url):
    programs = []
    content_divs = soup.find_all('ul')
    if content_divs:
        for content_div in content_divs:
            program_items = content_div.find_all('li')
            for program in program_items:
                link = program.find('a')
                if link:
                    title = link.text.strip()
                    href = link.get('href', '')
                    full_href = UTECH_BASE_URL + href if not href.startswith('http') else href
                    # Filter to include only specific programs
                    if title in [
                        "MSc in Integrated Rural Development", 
                        "MSc. Sustainable Energy & Climate Change",
                        "MSc. Built Environment", 
                        "BEng. in Construction Engineering",
                        "BSc. in Land Surveying and Geographic and Information Sciences",
                        "BSc. in Quantity Surveying",
                        "BSc. in Urban & Regional Planning",
                        "BSc. in Mines and Quarry Management",
                        "BSc. Real Estate Management & Valuation",
                        "Associate Degree in Surveying and Geographic Information Technology",
                        "Post-Diploma Bachelor of Science in Construction Management",
                        "Diploma Construction Management",
                        "Diploma in Structural Engineering",
                        "BA. Architectural Studies"
                    ]:
                        programs.append({
                            'college': 'UTech',
                            'faculty': 'Faculty of the Built Environment (FOBE)',
                            'programme': title,
                            'awarding_institution': 'UTech',
                            'link': full_href
                        })
    return programs

def scrape_joint_programs(soup, url):
    programs = []
    content_div = soup.find('div', id='parent-fieldname-text-737869ead84f423d9c3bba17b01090c8')
    if content_div:
        sections = content_div.find_all('h3')
        for section in sections:
            section_name = section.text.strip()
            ul_element = section.find_next('ul')
            if ul_element:
                program_items = ul_element.find_all('li')
                for program in program_items:
                    link = program.find('a')
                    if link:
                        title = link.text.strip()
                        href = link.get('href', '')
                        full_href = UTECH_BASE_URL + href if not href.startswith('http') else href
                        programs.append({
                            'college': 'UTech',
                            'faculty': f'College of Oral Health Sciences and School of Public Health & Health Technology - {section_name}',
                            'programme': title,
                            'awarding_institution': 'UTech',
                            'link': full_href
                        })
    return programs

def scrape_themico_programs():
    programs = []
    try:
        response = requests.get(THEMICO_URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        faculties = [
            ("FACULTY OF EDUCATION", [
                "B.Ed. Primary Education",
                "B.Ed. Secondary specialising in Physical Education",
                "B.Ed. Early Childhood Education",
                "B.Ed. Special Education"
            ]),
            ("FACULTY OF SCIENCE AND TECHNOLOGY", [
                "B.Ed. Family and Consumer Science",
                "B.Ed. Geography and Environmental Studies",
                "B.Ed. Computer Science",
                "B.Ed. Mathematics",
                "B.Ed. Science",
                "B.Ed. Industrial Technology"
            ]),
            ("FACULTY OF HUMANITIES AND LIBERAL ARTS", [
                "B.Ed. in Business Studies",
                "B.Ed. in Music",
                "B.Ed. Language and Literacy",
                "B.Ed. History and Culture",
                "B.Ed. in Institutional Management and Leadership",
                "B.Sc. in Guidance and Counselling",
                "B.Ed. Visual Arts",
                "B.Ed. Social Studies",
                "B.Ed. Language and Literature"
            ])
        ]

        for faculty, program_titles in faculties:
            faculty_heading = soup.find('h2', class_='elementor-heading-title elementor-size-default', string=faculty)
            if faculty_heading:
                for title in program_titles:
                    programme = soup.find('h2', class_='eael-elements-flip-box-heading', string=title)
                    if programme:
                        programs.append({
                            'college': 'The Mico University College',
                            'faculty': faculty,
                            'programme': title,
                            'awarding_institution': 'The Mico University College',
                            'link': THEMICO_URL
                        })

    except requests.RequestException as e:
        print(f"An error occurred while fetching The Mico University College page: {e}")

    return programs

if __name__ == "__main__":
    try:
        all_data = []

        # Scrape UCC
        response = requests.get(UCC_URL, headers=headers)
        response.raise_for_status()

        ucc_soup = BeautifulSoup(response.content, 'html.parser')
        ucc_tables = ucc_soup.find_all('table', class_='views-table')

        if len(ucc_tables) >= 3:
            all_data.extend(scrape_ucc_table(ucc_tables[0], "School of Business, Administration and Management"))
            all_data.extend(scrape_ucc_table(ucc_tables[1], "School of Behavioral Sciences, Humanities and Law"))
            all_data.extend(scrape_ucc_table(ucc_tables[2], "School of Technology and Mathematics"))
        else:
            print("Couldn't find all expected tables on UCC page")

        # Scrape UTech
        all_data.extend(scrape_utech_programs())

        # Scrape The Mico University College
        all_data.extend(scrape_themico_programs())

        # Save data to CSV
        csv_filename = f"jamaican_colleges_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_to_csv(all_data, csv_filename)
        print(f"Data saved to {csv_filename}")

        # Save data to MongoDB
        save_to_mongodb(all_data)
        print("Data saved to MongoDB in separate collections for each college")

        print("Data has been successfully scraped and stored from UCC, UTech, and The Mico University College websites")

    except requests.RequestException as e:
        print(f"An error occurred while fetching a web page: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")