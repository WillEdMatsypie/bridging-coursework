from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

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


        # In Terminal use the command `python manage.py test functional-tests` to run these