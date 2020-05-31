from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        self.assertTrue(any(section.text == 'Summary' for section in headings))
        self.assertTrue(any(section.text == 'Skills' for section in headings))
        self.assertTrue(any(section.text == 'Education' for section in headings))
        self.assertTrue(any(section.text == 'Experience' for section in headings))
        self.assertTrue(any(section.text == 'Interests' for section in headings))

    def test_skill(self):
        # Login to edit
        self.login()
        self.browser.get('http://localhost:8000/cv')

        # Click button for new education
        new_button = self.browser.find_element_by_id("new-skill")
        new_button.click()

        # Display new education form
        self.base_html_loads()

        # Notice all applicable fields
        title = self.browser.find_element_by_id("id_title")
        skill_type = self.browser.find_element_by_id("id_skill_type")

        # Fill in the form

        # Notice correct data displayed

        # find the specific item

        # Toggle collapse

        # Check item has all data

        # Check close collapse

        # Delete item
        self.fail("finish test!")


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
        title.send_keys("Test Education Title")
        location.send_keys("Test Location")
        start_date.send_keys("Test Start Date")
        end_date.send_keys("Test End Date")
        brief.send_keys("Test Brief")
        detail.send_keys("Test Detail")
        save.click()

        # Notice correct data displayed
        education_section = self.browser.find_element_by_id("education-section")
        items = education_section.find_elements_by_class_name("card")
        self.assertTrue(any('Test Education Title' in item.text for item in items))

        # find the specific item
        for item in items:
            if 'Test Education Title' in item.text:
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
        self.assertTrue('Test Location' in header.text)
        self.assertTrue('Test Start Date' in header.text)
        self.assertTrue('Test End Date' in header.text)
        self.assertTrue('Test Brief' in header.text)
        self.assertTrue('Test Detail' in body.text)

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
        self.assertFalse(any('Test Education Title' in item.text for item in items))


        self.browser.get('http://localhost:8000/accounts/logout')

        # In Terminal use the command `python manage.py test functional-tests` to run these