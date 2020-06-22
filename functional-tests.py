from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import unittest

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get('http://localhost:8000/accounts/login')
        self.browser.find_element_by_id('id_username').send_keys('admin')
        self.browser.find_element_by_id('id_password').send_keys('testPass123')
        login_button = self.browser.find_element_by_id("login-button")
        login_button.click()
    
    def login_page_show(self, url):
        self.browser.get(url)
        try:
            self.browser.find_element_by_id('id_username')
            self.browser.find_element_by_id('id_password')
            self.browser.find_element_by_id("login-button")
        except NoSuchElementException:
            return False
        return True

    def base_html_loads(self):
        # Sees Page Title and sees nav-bar
        self.assertIn('Zenith', self.browser.title)
        header_text = self.browser.find_element_by_class_name('navbar-brand').text
        self.assertIn('Zenith', header_text)

        # Notice Nav-bar links to Blog and then CV
        navbar = self.browser.find_elements_by_class_name('nav-link')
        self.assertTrue(any(link.text == 'Blog' and 'blog' in link.get_attribute("href") for link in navbar))
        self.assertTrue(any(link.text == 'CV' and 'cv' in link.get_attribute("href") for link in navbar))

    def test_view_home_page(self):
        self.browser.get('http://localhost:8000')

        # Check Title & Nav-bar
        self.base_html_loads()
        
        # See Title of page 
        title_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Zenith', title_text)

        # Check out social links
        socials = self.browser.find_elements_by_class_name('social-btn')
        self.assertTrue(any('https://twitter.com/Willedmats' == link.get_attribute("href") and 'twitter' in link.get_attribute("class") for link in socials))
        self.assertTrue(any('https://www.instagram.com/willedmatsypie/' == link.get_attribute("href") and 'instagram' in link.get_attribute("class") for link in socials))
        self.assertTrue(any('https://open.spotify.com/user/willedmatsypie?si=FWpbPgjoTW2XyX0FGkP7fw' == link.get_attribute("href") and 'spotify' in link.get_attribute("class") for link in socials))
        self.assertTrue(any('https://www.linkedin.com/in/william-matson-589409171/' == link.get_attribute("href") and 'linkedin' in link.get_attribute("class") for link in socials))
        self.assertTrue(any('https://github.com/WillEdMatsypie' == link.get_attribute("href") and 'github' in link.get_attribute("class") for link in socials))

        # Can see buttons for accessing CV and Blog
        page_btns = self.browser.find_elements_by_class_name('btn-outline-dark')
        self.assertTrue(any(btn.text == 'My Blog' and 'blog' in btn.get_attribute("href") for btn in page_btns))
        self.assertTrue(any(btn.text == 'Interactive CV' and 'cv' in btn.get_attribute("href") for btn in page_btns))

    def test_view_cv_page(self):
        self.browser.get('http://localhost:8000/cv')

        # Check Title & Nav-bar
        self.base_html_loads()

        # See Name at start of CV
        title_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('William Matson', title_text)

        # See section headings in CV
        headings = self.browser.find_elements_by_class_name('section-header')
        self.assertTrue(any(section.text == 'Statement' for section in headings))
        self.assertTrue(any(section.text == 'Skills' for section in headings))
        self.assertTrue(any(section.text == 'Education' for section in headings))
        self.assertTrue(any(section.text == 'Experience' for section in headings))
        self.assertTrue(any(section.text == 'Interests' for section in headings))

    def test_skill(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new skill
        new_button = self.browser.find_element_by_id("new-skill")
        new_button.click()

        # Display new skill form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        skill_type = Select(self.browser.find_element_by_id('id_skill_type'))
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Skill Tech 1")
        skill_type.select_by_visible_text("TECHNICAL")
        save.click()

        # Add a skill which is other
        new_button = self.browser.find_element_by_id("new-skill")
        new_button.click()
        self.base_html_loads()

        title = self.browser.find_element_by_id("id_title")
        skill_type = Select(self.browser.find_element_by_id('id_skill_type'))
        save = self.browser.find_element_by_class_name("save")

        title.send_keys("Skill Other 1")
        skill_type.select_by_visible_text("OTHER")
        save.click()

        # Notice the tables
        tech_table = self.browser.find_element_by_id("tech-skill-table")
        other_table = self.browser.find_element_by_id("other-skill-table")

        # Check table header
        table_head = tech_table.find_element_by_tag_name('h3').text
        self.assertIn('Technical Skills', table_head)

        # Check item is displayed and other item is not
        items = tech_table.find_elements_by_class_name("skill-item")
        self.assertTrue(any(item.text == 'Skill Tech 1' for item in items))
        self.assertFalse(any(item.text == 'Skill Other 1' for item in items))
        
        # find the specific item
        for item in items:
            if 'Skill Tech 1' in item.text:
                tech_skill = item

        # Repeat for other table
        table_head = other_table.find_element_by_tag_name('h3').text
        self.assertIn('Other Skills', table_head)

        items = other_table.find_elements_by_class_name("skill-item")
        self.assertTrue(any(item.text == 'Skill Other 1' for item in items))
        self.assertFalse(any(item.text == 'Skill Tech 1' for item in items))

        # Delete tech item
        delete_btn = tech_skill.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)
        tech_table = self.browser.find_element_by_id("tech-skill-table")
        items = tech_table.find_elements_by_class_name("skill-item")
        self.assertFalse(any(item.text == 'Skill Tech 1' for item in items))


        # Delete other item
        other_table = self.browser.find_element_by_id("other-skill-table")

        items = other_table.find_elements_by_class_name("skill-item")
        for item in items:
            if 'Skill Other 1' in item.text:
                other_skill = item

        delete_btn = other_skill.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)

        other_table = self.browser.find_element_by_id("other-skill-table")

        items = other_table.find_elements_by_class_name("skill-item")
        self.assertFalse(any(item.text == 'Skill Other 1' for item in items))

        self.browser.get('http://localhost:8000/accounts/logout')
    
    def test_skill_edit(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new skill
        new_button = self.browser.find_element_by_id("new-skill")
        new_button.click()

        # Display new skill form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        skill_type = Select(self.browser.find_element_by_id('id_skill_type'))
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Skill Tech 2")
        skill_type.select_by_visible_text("TECHNICAL")
        save.click()

        # Notice the table
        tech_table = self.browser.find_element_by_id("tech-skill-table")

        # Check item is displayed
        items = tech_table.find_elements_by_class_name("skill-item")
        self.assertTrue(any(item.text == 'Skill Tech 2' for item in items))

        # find the specific item
        for item in items:
            if 'Skill Tech 2' in item.text:
                tech_skill = item
        
        # See edit button
        edit_btn = tech_skill.find_element_by_class_name("edit_btn")
        edit_btn.click()

        # Display edit skill form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        skill_type = Select(self.browser.find_element_by_id('id_skill_type'))
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys(" Other")
        skill_type.select_by_visible_text("OTHER")
        save.click()

        # Notice the tables
        tech_table = self.browser.find_element_by_id("tech-skill-table")
        other_table = self.browser.find_element_by_id("other-skill-table")

        # Check item is displayed and is not in tech table
        items = tech_table.find_elements_by_class_name("skill-item")
        items2 = other_table.find_elements_by_class_name("skill-item")
        self.assertFalse(any(item.text == 'Skill Tech 2' for item in items))
        self.assertFalse(any(item.text == 'Skill Tech 2 Other' for item in items))
        self.assertFalse(any(item.text == 'Skill Tech 2' for item in items2))
        self.assertTrue(any(item.text == 'Skill Tech 2 Other' for item in items2))

        # Delete item
        for item in items2:
            if 'Skill Tech 2 Other' in item.text:
                other_skill = item

        delete_btn = other_skill.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)

        other_table = self.browser.find_element_by_id("other-skill-table")

        items = other_table.find_elements_by_class_name("skill-item")
        self.assertFalse(any(item.text == 'Skill Tech 2 Other' for item in items))

        self.browser.get('http://localhost:8000/accounts/logout')


    def test_education(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new education
        new_button = self.browser.find_element_by_id("new-education")
        new_button.click()

        # Display new education form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        location = self.browser.find_element_by_id("id_location")
        start_date = self.browser.find_element_by_id("id_start_date")
        end_date = self.browser.find_element_by_id("id_end_date")
        brief = self.browser.find_element_by_id("id_brief_text")
        detail = self.browser.find_element_by_id("id_detailed_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Education Title 1")
        location.send_keys("Test Location 1")
        start_date.send_keys("Test Start Date 1")
        end_date.send_keys("Test End Date 1")
        brief.send_keys("Test Brief 1")
        detail.send_keys("Test Detail 1")
        save.click()

        # Notice correct data displayed
        education_section = self.browser.find_element_by_id("education-section")
        items = education_section.find_elements_by_class_name("card")
        self.assertTrue(any('Test Education Title 1' in item.text for item in items))

        # find the specific item
        for item in items:
            if 'Test Education Title 1' in item.text:
                header = item.find_element_by_class_name("card-header")
                body = item.find_element_by_class_name("collapse")

        # Toggle collapse
        self.assertTrue('collapsed' in header.get_attribute("class"))
        self.assertTrue('show' not in body.get_attribute("class"))
        header.click()
        time.sleep(1)
        self.assertTrue('collapsed' not in header.get_attribute("class"))
        self.assertTrue('show' in body.get_attribute("class"))

        # Check item has all data
        self.assertTrue('Test Location 1' in header.text)
        self.assertTrue('Test Start Date 1' in header.text)
        self.assertTrue('Test End Date 1' in header.text)
        self.assertTrue('Test Brief 1' in header.text)
        self.assertTrue('Test Detail 1' in body.text)

        # Check close collapse
        header.click()
        time.sleep(1)
        self.assertTrue('collapsed' in header.get_attribute("class"))
        self.assertTrue('show' not in body.get_attribute("class"))

        # Delete item
        header.click()
        time.sleep(1)
        delete_btn = item.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)
        education_section = self.browser.find_element_by_id("education-section")
        items = education_section.find_elements_by_class_name("card")
        self.assertFalse(any('Test Education Title 1' in item.text for item in items))


        self.browser.get('http://localhost:8000/accounts/logout')

    def test_education_edit(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new education
        new_button = self.browser.find_element_by_id("new-education")
        new_button.click()

        # Display new education form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        location = self.browser.find_element_by_id("id_location")
        start_date = self.browser.find_element_by_id("id_start_date")
        end_date = self.browser.find_element_by_id("id_end_date")
        brief = self.browser.find_element_by_id("id_brief_text")
        detail = self.browser.find_element_by_id("id_detailed_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Education Title 2")
        location.send_keys("Test Location 2")
        start_date.send_keys("Test Start Date 2")
        end_date.send_keys("Test End Date 2")
        brief.send_keys("Test Brief 2")
        detail.send_keys("Test Detail 2")
        save.click()

        # Notice correct data displayed
        education_section = self.browser.find_element_by_id("education-section")
        items = education_section.find_elements_by_class_name("card")
        self.assertTrue(any('Test Education Title 2' in item.text for item in items))

        # find the specific item
        for item in items:
            if 'Test Education Title 2' in item.text:
                header = item.find_element_by_class_name("card-header")
                body = item.find_element_by_class_name("collapse")
        
        # See edit button
        header.click()
        time.sleep(1)
        edit_btn = body.find_element_by_class_name("edit_btn")
        edit_btn.click()

        # Display edit skill form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        location = self.browser.find_element_by_id("id_location")
        start_date = self.browser.find_element_by_id("id_start_date")
        end_date = self.browser.find_element_by_id("id_end_date")
        brief = self.browser.find_element_by_id("id_brief_text")
        detail = self.browser.find_element_by_id("id_detailed_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.clear()
        title.send_keys("Test Education Title EDIT")
        end_date.send_keys(" Edit")
        detail.send_keys(" EDITED TEXT")
        save.click()

                # Notice correct data displayed
        education_section = self.browser.find_element_by_id("education-section")
        items = education_section.find_elements_by_class_name("card")
        self.assertFalse(any('Test Education Title 2' in item.text for item in items))
        self.assertTrue(any('Test Education Title EDIT' in item.text for item in items))

        # find the specific item
        for item in items:
            if 'Test Education Title EDIT' in item.text:
                header = item.find_element_by_class_name("card-header")
                body = item.find_element_by_class_name("collapse")

        # Toggle collapse
        header.click()
        time.sleep(1)

        # Check item has all data
        self.assertTrue('Test Location 2' in header.text)
        self.assertTrue('Test Start Date 2' in header.text)
        self.assertTrue('Test End Date 2 Edit' in header.text)
        self.assertTrue('Test Brief 2' in header.text)
        self.assertTrue('Test Detail 2 EDITED TEXT' in body.text)

        # Delete item
        delete_btn = item.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)
        education_section = self.browser.find_element_by_id("education-section")
        items = education_section.find_elements_by_class_name("card")
        self.assertFalse(any('Test Education Title EDIT' in item.text for item in items))

        self.browser.get('http://localhost:8000/accounts/logout')

    def test_experience(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new experience
        new_button = self.browser.find_element_by_id("new-experience")
        new_button.click()

        # Display new experience form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        date = self.browser.find_element_by_id("id_date")
        detail = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Experience Title 1")
        subtitle.send_keys("Test Subtitle 1")
        date.send_keys("Test Date 1")
        detail.send_keys("Test Detail 1")
        save.click()

        # Notice correct data displayed
        experience_section = self.browser.find_element_by_id("experience-section")
        items = experience_section.find_elements_by_class_name("card")
        self.assertTrue(any('Test Experience Title 1' in item.text for item in items))

        # find the specific item
        for item in items:
            if 'Test Experience Title 1' in item.text:
                header = item.find_element_by_class_name("card-header")
                body = item.find_element_by_class_name("collapse")

        # Toggle collapse
        self.assertTrue('collapsed' in header.get_attribute("class"))
        self.assertTrue('show' not in body.get_attribute("class"))
        header.click()
        time.sleep(1)
        self.assertTrue('collapsed' not in header.get_attribute("class"))
        self.assertTrue('show' in body.get_attribute("class"))

        # Check item has all data
        self.assertTrue('Test Subtitle 1' in header.text)
        self.assertTrue('Test Date 1' in header.text)
        self.assertTrue('Test Detail 1' in body.text)

        # Check close collapse
        header.click()
        time.sleep(1)
        self.assertTrue('collapsed' in header.get_attribute("class"))
        self.assertTrue('show' not in body.get_attribute("class"))

        # Delete item
        header.click()
        time.sleep(1)
        delete_btn = item.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)
        experience_section = self.browser.find_element_by_id("experience-section")
        items = experience_section.find_elements_by_class_name("card")
        self.assertFalse(any('Test Experience Title 1' in item.text for item in items))


        self.browser.get('http://localhost:8000/accounts/logout')
    
    def test_experience_edit(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new experience
        new_button = self.browser.find_element_by_id("new-experience")
        new_button.click()

        # Display new experience form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        date = self.browser.find_element_by_id("id_date")
        detail = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Experience Title 2")
        subtitle.send_keys("Test Subtitle 2")
        date.send_keys("Test Date 2")
        detail.send_keys("Test Detail 2")
        save.click()

        # Notice correct data displayed
        experience_section = self.browser.find_element_by_id("experience-section")
        items = experience_section.find_elements_by_class_name("card")
        self.assertTrue(any('Test Experience Title 2' in item.text for item in items))

        # find the specific item
        for item in items:
            if 'Test Experience Title 2' in item.text:
                header = item.find_element_by_class_name("card-header")
                body = item.find_element_by_class_name("collapse")
        
        # See edit button
        header.click()
        time.sleep(1)
        edit_btn = body.find_element_by_class_name("edit_btn")
        edit_btn.click()

        # Display edit experience form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        date = self.browser.find_element_by_id("id_date")
        detail = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.clear()
        title.send_keys("Test Experience Title EDIT")
        detail.send_keys(" EDITED")
        save.click()

        # Notice correct data displayed
        experience_section = self.browser.find_element_by_id("experience-section")
        items = experience_section.find_elements_by_class_name("card")
        self.assertFalse(any('Test Experience Title 2' in item.text for item in items))
        self.assertTrue(any('Test Experience Title EDIT' in item.text for item in items))

        # find the specific item
        for item in items:
            if 'Test Experience Title EDIT' in item.text:
                header = item.find_element_by_class_name("card-header")
                body = item.find_element_by_class_name("collapse")

        # Toggle collapse
        header.click()
        time.sleep(1)

        # Check edited content
        self.assertTrue('Test Subtitle 2' in header.text)
        self.assertTrue('Test Date 2' in header.text)
        self.assertTrue('Test Detail 2 EDITED' in body.text)

        # Delete item
        delete_btn = item.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)
        experience_section = self.browser.find_element_by_id("experience-section")
        items = experience_section.find_elements_by_class_name("card")
        self.assertFalse(any('Test Experience Title EDIT' in item.text for item in items))

        self.browser.get('http://localhost:8000/accounts/logout')
    
    def test_interests(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new interest
        new_button = self.browser.find_element_by_id("new-interest")
        new_button.click()

        # Display new interest form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Interest 1")
        save.click()

        # Notice the tables
        interest_table = self.browser.find_element_by_id("interest-table")

        # Check item is displayed and other item is not
        items = interest_table.find_elements_by_class_name("interest-item")
        self.assertTrue(any(item.text == 'Test Interest 1' for item in items))
        
        # find the specific item
        for item in items:
            if 'Test Interest 1' in item.text:
                interest = item

        # Delete interest
        delete_btn = interest.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)
        interest_table = self.browser.find_element_by_id("interest-table")
        items = interest_table.find_elements_by_class_name("interest-item")
        self.assertFalse(any(item.text == 'Test Interest' for item in items))

        self.browser.get('http://localhost:8000/accounts/logout')

    def test_interest_edit(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new interest
        new_button = self.browser.find_element_by_id("new-interest")
        new_button.click()

        # Display new interest form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Interest 2")
        save.click()

        # Notice the tables
        interest_table = self.browser.find_element_by_id("interest-table")

        # Check item is displayed
        items = interest_table.find_elements_by_class_name("interest-item")
        self.assertTrue(any(item.text == 'Test Interest 2' for item in items))
        
        # find the specific item
        for item in items:
            if 'Test Interest 2' in item.text:
                interest = item
        
        # See edit button
        edit_btn = interest.find_element_by_class_name("edit_btn")
        edit_btn.click()

        # Display edit skill form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.clear()
        title.send_keys("Test Interest EDIT")
        save.click()

        interest_table = self.browser.find_element_by_id("interest-table")

        # Check item is displayed and other item is not
        items = interest_table.find_elements_by_class_name("interest-item")
        self.assertFalse(any(item.text == 'Test Interest 2' for item in items))
        self.assertTrue(any(item.text == 'Test Interest EDIT' for item in items))
        
        # find the specific item
        for item in items:
            if 'Test Interest EDIT' in item.text:
                interest = item

        # Delete interest
        delete_btn = interest.find_element_by_class_name("delete_btn")
        delete_btn.click()
        time.sleep(1)
        interest_table = self.browser.find_element_by_id("interest-table")
        items = interest_table.find_elements_by_class_name("interest-item")
        self.assertFalse(any(item.text == 'Test Interest EDIT' for item in items))

        self.browser.get('http://localhost:8000/accounts/logout')

    def test_cv_authentication_urls(self):
        # Test to see if login page displays appropriately on trying to access these URLs
        self.assertFalse(self.login_page_show('http://localhost:8000/cv'))

        self.assertTrue(self.login_page_show('http://localhost:8000/cv/interest/new'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/experience/new'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/skill/new'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/education/new'))

        self.assertTrue(self.login_page_show('http://localhost:8000/cv/interest/0/edit'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/experience/0/edit'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/skill/0/edit'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/education/0/edit'))

        self.assertTrue(self.login_page_show('http://localhost:8000/cv/interest/0/remove'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/experience/0/remove'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/skill/0/remove'))
        self.assertTrue(self.login_page_show('http://localhost:8000/cv/education/0/remove'))
    
    def test_make_and_view_blog_post(self):
        self.login()

        self.browser.get('http://localhost:8000/blog/')

        # Check Title & Nav-bar
        self.base_html_loads()

        # See New Post Button
        new_post_btn = self.browser.find_element_by_id('new-post')
        new_post_btn.click()

        # Display new post form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        text = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Blog Post 1")
        subtitle.send_keys("Test Subtitle 1")
        text.send_keys("Test Post Text 1")
        save.click()

        # See Information is correct on Post Detail Page
        self.base_html_loads()
        title_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Test Blog Post 1', title_text)

        subtitle_text = self.browser.find_element_by_class_name('subtitle').text
        self.assertEqual('Test Subtitle 1', subtitle_text)

        all_text = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(post_text.text == 'Test Post Text 1' for post_text in all_text))
        
        # Views that post is NOT published
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Blog' in link.text:
                post_list_btn = link
        
        post_list_btn.click()
        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertFalse(any('Test Blog Post 1' in card.text for card in cards))

        # Views Post exists as a Draft
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Drafts' in link.text:
                draft_btn = link
        
        draft_btn.click()
        self.base_html_loads()

        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertTrue(any('Test Blog Post 1' in card.text for card in cards))
        for card in cards:
            if 'Test Blog Post 1' in card.text:
                title = card.find_element_by_class_name('card-title')
                link = title.find_element_by_tag_name('a')
                self.assertEqual(title.text, 'Test Blog Post 1')
                self.assertIn('created', card.find_element_by_class_name('date').text)
                self.assertEqual(card.find_element_by_class_name('subtitle').text, 'Test Subtitle 1')
        
        link.click()

        # See Information is correct on Post Detail Page
        self.base_html_loads()
        title_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Test Blog Post 1', title_text)

        subtitle_text = self.browser.find_element_by_class_name('subtitle').text
        self.assertEqual('Test Subtitle 1', subtitle_text)

        all_text = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(post_text.text == 'Test Post Text 1' for post_text in all_text))

        # Publish the Draft
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Publish' in button.text:
                button.click()
                break
        
        # See published post content
        title_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Test Blog Post 1', title_text)

        subtitle_text = self.browser.find_element_by_class_name('subtitle').text
        self.assertEqual('Test Subtitle 1', subtitle_text)

        all_text = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(post_text.text == 'Test Post Text 1' for post_text in all_text))

        pub_date = self.browser.find_element_by_class_name('date').text
        self.assertNotEqual(pub_date, "")

        # See Post is NOT a Draft
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Drafts' in link.text:
                draft_btn = link
        
        draft_btn.click()
        self.base_html_loads()

        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertFalse(any('Test Blog Post 1' in card.text for card in cards))
        
        # See Post is now Published
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Blog' in link.text:
                post_list_btn = link
        
        post_list_btn.click()
        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertTrue(any('Test Blog Post 1' in card.text for card in cards))
        for card in cards:
            if 'Test Blog Post 1' in card.text:
                title = card.find_element_by_class_name('card-title')
                link = title.find_element_by_tag_name('a')
                self.assertEqual(title.text, 'Test Blog Post 1')
                self.assertIn('published', card.find_element_by_class_name('date').text)
                self.assertEqual(card.find_element_by_class_name('subtitle').text, 'Test Subtitle 1')
        
        # Delete Post
        link.click()

        # See Information is correct on Post Detail Page
        self.base_html_loads()
        title_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Test Blog Post 1', title_text)

        subtitle_text = self.browser.find_element_by_class_name('subtitle').text
        self.assertEqual('Test Subtitle 1', subtitle_text)

        all_text = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(post_text.text == 'Test Post Text 1' for post_text in all_text))

        # Press Delete Button
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Delete' in button.text:
                button.click()
                break

        # Redirected to post list
        self.assertEqual(self.browser.current_url, 'http://localhost:8000/blog/')

        # Confirm post is deleted
        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertFalse(any('Test Blog Post 1' in card.text for card in cards))

        self.browser.get('http://localhost:8000/accounts/logout')
    

    def test_make_and_delete_draft(self):
        self.login()

        self.browser.get('http://localhost:8000/blog/drafts/')

        # Check Title & Nav-bar
        self.base_html_loads()

        # See New Post Button
        new_post_btn = self.browser.find_element_by_id('new-post')
        new_post_btn.click()

        # Display new post form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        text = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Blog Post 2")
        subtitle.send_keys("Test Subtitle 2")
        text.send_keys("Test Post Text 2")
        save.click()
        
        # Views Post exists as a Draft
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Drafts' in link.text:
                draft_btn = link
        
        draft_btn.click()
        self.base_html_loads()

        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertTrue(any('Test Blog Post 2' in card.text for card in cards))
        for card in cards:
            if 'Test Blog Post 2' in card.text:
                title = card.find_element_by_class_name('card-title')
                link = title.find_element_by_tag_name('a')
                self.assertEqual(title.text, 'Test Blog Post 2')
                self.assertIn('created', card.find_element_by_class_name('date').text)
                self.assertEqual(card.find_element_by_class_name('subtitle').text, 'Test Subtitle 2')

        # Delete Post
        link.click()

        # Press Delete Button
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Delete' in button.text:
                button.click()
                break

        # Redirected to post list
        self.assertEqual(self.browser.current_url, 'http://localhost:8000/blog/')

        # Confirm post is deleted
        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertFalse(any('Test Blog Post 2' in card.text for card in cards))

        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Drafts' in link.text:
                draft_btn = link
        
        draft_btn.click()
        self.base_html_loads()

        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertFalse(any('Test Blog Post 2' in card.text for card in cards))

        self.browser.get('http://localhost:8000/accounts/logout')

    def test_make_and_edit_posts(self):
        self.login()

        self.browser.get('http://localhost:8000/blog/')

        # Check Title & Nav-bar
        self.base_html_loads()

        # See New Post Button
        new_post_btn = self.browser.find_element_by_id('new-post')
        new_post_btn.click()

        # Display new post form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        text = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Blog Post 3")
        subtitle.send_keys("Test Subtitle 3")
        text.send_keys("Test Post Text 3")
        save.click()

        # Views Post content on Draft Page
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Drafts' in link.text:
                draft_btn = link
        
        draft_btn.click()
        self.base_html_loads()

        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertTrue(any('Test Blog Post 3' in card.text for card in cards))
        for card in cards:
            if 'Test Blog Post 3' in card.text:
                title = card.find_element_by_class_name('card-title')
                link = title.find_element_by_tag_name('a')
                self.assertEqual(title.text, 'Test Blog Post 3')
                self.assertIn('created', card.find_element_by_class_name('date').text)
                self.assertEqual(card.find_element_by_class_name('subtitle').text, 'Test Subtitle 3')
        
        # Open Post and see Edit Button
        link.click()
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Edit' in button.text:
                button.click()
                break
        
        # See Edit form
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        text = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys(" EDT")
        subtitle.send_keys(" EITED")
        text.send_keys(" HELLA EDITED")
        save.click()

        # Check edited post content
        title_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Test Blog Post 3 EDT', title_text)

        subtitle_text = self.browser.find_element_by_class_name('subtitle').text
        self.assertEqual('Test Subtitle 3 EITED', subtitle_text)

        all_text = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(post_text.text == 'Test Post Text 3 HELLA EDITED' for post_text in all_text))

        # Go to Drafts Page
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Drafts' in link.text:
                draft_btn = link
        
        draft_btn.click()
        self.base_html_loads()

        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertTrue(any('Test Blog Post 3 EDT' in card.text for card in cards))
        for card in cards:
            if 'Test Blog Post 3 EDT' in card.text:
                title = card.find_element_by_class_name('card-title')
                link = title.find_element_by_tag_name('a')
                self.assertEqual(title.text, 'Test Blog Post 3 EDT')
                self.assertIn('created', card.find_element_by_class_name('date').text)
                self.assertEqual(card.find_element_by_class_name('subtitle').text, 'Test Subtitle 3 EITED')
        
        # We are happy with the post so let's publish it
        link.click()
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Publish' in button.text:
                button.click()
                break
        
        # Oh no, there's some typos, let's edit that
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Edit' in button.text:
                button.click()
                break
        
        # See Edit form
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        text = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.clear()
        title.send_keys("Final Blog Post EDIT 3")
        subtitle.clear()
        subtitle.send_keys("Final Subtitle EDITED 3")
        text.clear()
        text.send_keys("Maybe there should be a real article here or something.")
        save.click()

        # Check Edited content
        title_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Final Blog Post EDIT 3', title_text)

        subtitle_text = self.browser.find_element_by_class_name('subtitle').text
        self.assertEqual('Final Subtitle EDITED 3', subtitle_text)

        all_text = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(post_text.text == 'Maybe there should be a real article here or something.' for post_text in all_text))

        # View post in post list
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Blog' in link.text:
                post_list_btn = link
        
        post_list_btn.click()
        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertTrue(any('Final Blog Post EDIT 3' in card.text for card in cards))
        for card in cards:
            if 'Final Blog Post EDIT 3' in card.text:
                title = card.find_element_by_class_name('card-title')
                link = title.find_element_by_tag_name('a')
                self.assertEqual(title.text, 'Final Blog Post EDIT 3')
                self.assertIn('published', card.find_element_by_class_name('date').text)
                self.assertEqual(card.find_element_by_class_name('subtitle').text, 'Final Subtitle EDITED 3')
        
        # Finally, delete the post
        link.click()
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Delete' in button.text:
                button.click()
                break
        
        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertFalse(any('Final Blog Post EDIT 3' in card.text for card in cards))

        self.browser.get('http://localhost:8000/accounts/logout')


    def check_number_of_comments(self, number):
        cards = self.browser.find_elements_by_class_name('card-body')
        self.assertTrue(any('Test Blog Post 4' in card.text for card in cards))
        for card in cards:
            if 'Test Blog Post 4' in card.text:
                title = card.find_element_by_class_name('card-title')
                link = title.find_element_by_tag_name('a')
                comments = card.find_element_by_class_name('card-comments')
                self.assertEqual(title.text, 'Test Blog Post 4')
                self.assertEqual(comments.text, 'Comments: ' + str(number))
        
        return link

    def test_blog_comments(self):
        self.login()

        self.browser.get('http://localhost:8000/blog/')

        # Create a Post
        new_post_btn = self.browser.find_element_by_id('new-post')
        new_post_btn.click()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        subtitle = self.browser.find_element_by_id("id_subtitle")
        text = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Fill in the form
        title.send_keys("Test Blog Post 4")
        subtitle.send_keys("Test Subtitle 4")
        text.send_keys("Test Post Text 4")
        save.click()

        # Add a comment to the post
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Add comment' in button.text:
                button.click()
                break
        
        # See form loads correctly
        self.base_html_loads()
        author = self.browser.find_element_by_id("id_author")
        text = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Enter data in all fields
        author.send_keys("Test Author 1")
        text.send_keys("Test Comment Text 1")
        save.click()

        # See comment is on post
        all_text = self.browser.find_elements_by_class_name('comment')
        self.assertTrue(any(comment_text.find_element_by_tag_name('strong').text == 'Test Author 1' and \
                        any(paragraph.text == 'Test Comment Text 1' for paragraph in comment_text.find_elements_by_tag_name('p')) for comment_text in all_text))

        # See number of comments on post draft is still 0 (Becuase the comment is unapproved)
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Drafts' in link.text:
                draft_btn = link

        draft_btn.click()

        link = self.check_number_of_comments(0)
        
        # Approve the Comment
        link.click()
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Approve' in button.text:
                button.click()
                break
        
        # See number of comments on draft is now 1
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Drafts' in link.text:
                draft_btn = link

        draft_btn.click()

        link = self.check_number_of_comments(1)
        
        # Publish the post
        link.click()
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Publish' in button.text:
                button.click()
                break
        
        # Add another comment
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Add comment' in button.text:
                button.click()
                break
        
        # See form loads correctly
        self.base_html_loads()
        author = self.browser.find_element_by_id("id_author")
        text = self.browser.find_element_by_id("id_text")
        save = self.browser.find_element_by_class_name("save")

        # Enter data in all fields
        author.send_keys("Test Author 2")
        text.send_keys("Test Comment Text 2")
        save.click()

        # See both comments on post
        all_text = self.browser.find_elements_by_class_name('comment')
        self.assertTrue(any(comment_text.find_element_by_tag_name('strong').text == 'Test Author 1' and \
                        any(paragraph.text == 'Test Comment Text 1' for paragraph in comment_text.find_elements_by_tag_name('p')) for comment_text in all_text))
        self.assertTrue(any(comment_text.find_element_by_tag_name('strong').text == 'Test Author 2' and \
                        any(paragraph.text == 'Test Comment Text 2' for paragraph in comment_text.find_elements_by_tag_name('p')) for comment_text in all_text))
        
        # See post list says 1 comment still (2nd comment not approved yet)
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Blog' in link.text:
                blog_btn = link

        blog_btn.click()

        link = self.check_number_of_comments(1)

        # Approve the comment and check the number goes up to 2
        link.click()
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Approve' in button.text:
                button.click()
                break
        
        # See number of comments on draft is now 1
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Blog' in link.text:
                blog_btn = link

        blog_btn.click()

        link = self.check_number_of_comments(2)
        
        # Delete the first comment 
        link.click()
        all_text = self.browser.find_elements_by_class_name('comment')
        for comment in all_text:
            if 'Test Comment Text 1' in comment.text:
                btn = comment.find_element_by_tag_name('a')
                btn.click()
                break

        time.sleep(1)

        all_text = self.browser.find_elements_by_class_name('comment')
        self.assertFalse(any(comment_text.find_element_by_tag_name('strong').text == 'Test Author 1' and \
                        any(paragraph.text == 'Test Comment Text 1' for paragraph in comment_text.find_elements_by_tag_name('p')) for comment_text in all_text))
        self.assertTrue(any(comment_text.find_element_by_tag_name('strong').text == 'Test Author 2' and \
                        any(paragraph.text == 'Test Comment Text 2' for paragraph in comment_text.find_elements_by_tag_name('p')) for comment_text in all_text))
        
        # Check number of comments has reduced to 1 in post list
        navbar = self.browser.find_elements_by_class_name('nav-link')
        for link in navbar:
            if 'Blog' in link.text:
                blog_btn = link

        blog_btn.click()

        link = self.check_number_of_comments(1)

        # Delete the post
        link.click()

        # Press Delete Button
        buttons = self.browser.find_elements_by_class_name('btn')
        for button in buttons:
            if 'Delete' in button.text:
                button.click()
                break
        
        self.browser.get('http://localhost:8000/accounts/logout')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
# In Terminal use the command `python manage.py test functional-tests` to run these