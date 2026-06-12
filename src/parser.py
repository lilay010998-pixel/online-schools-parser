# Parser module for extracting school information
import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, List
from config import USER_AGENT, TIMEOUT, MAX_RETRIES

logger = logging.getLogger(__name__)

class SchoolParser:
    """Parse online school information from websites and APIs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT
        })
        self.schools_data = []
    
    def parse_school(self, url: str) -> Dict:
        """
        Parse school information from URL
        
        Args:
            url: School website URL
            
        Returns:
            Dictionary with school data
        """
        try:
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic info
            school_data = {
                'url': url,
                'name': self._extract_name(soup, url),
                'description': self._extract_description(soup),
                'contacts': self._extract_contacts(soup),
                'social_media': self._extract_social_media(soup),
                'courses': self._extract_courses(soup),
            }
            
            logger.info(f"✅ Добавлена: {school_data['name']}")
            return school_data
            
        except Exception as e:
            logger.error(f"❌ Error parsing {url}: {str(e)}")
            return None
    
    def _extract_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract school name from page"""
        # Try to find title
        title = soup.find('title')
        if title:
            return title.get_text().strip().split('|')[0].strip()
        
        # Extract from URL if title not found
        return url.replace('https://', '').replace('http://', '').split('/')[0].replace('www.', '').title()
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract school description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']
        
        # Try to find first paragraph
        p = soup.find('p')
        if p:
            return p.get_text().strip()[:200]
        
        return "Online education platform"
    
    def _extract_contacts(self, soup: BeautifulSoup) -> Dict:
        """Extract contact information"""
        contacts = {
            'email': None,
            'phone': None,
            'address': None
        }
        
        # Find email
        for link in soup.find_all('a', href=True):
            if 'mailto:' in link['href']:
                contacts['email'] = link['href'].replace('mailto:', '')
                break
        
        # Find phone
        text = soup.get_text()
        import re
        phone_match = re.search(r'\+7\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}', text)
        if phone_match:
            contacts['phone'] = phone_match.group()
        
        return contacts
    
    def _extract_social_media(self, soup: BeautifulSoup) -> Dict:
        """Extract social media links"""
        socials = {
            'vk': None,
            'instagram': None,
            'telegram': None,
            'youtube': None
        }
        
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            if 'vk.com' in href or 'vkontakte.ru' in href:
                socials['vk'] = link['href']
            elif 'instagram.com' in href:
                socials['instagram'] = link['href']
            elif 'telegram' in href:
                socials['telegram'] = link['href']
            elif 'youtube.com' in href:
                socials['youtube'] = link['href']
        
        return socials
    
    def _extract_courses(self, soup: BeautifulSoup) -> List[str]:
        """Extract course information"""
        courses = []
        
        # Look for common course-related keywords
        text = soup.get_text().lower()
        keywords = ['programming', 'design', 'marketing', 'business', 'data', 'ai', 'web', 'mobile']
        
        for keyword in keywords:
            if keyword in text:
                courses.append(keyword.title())
        
        return courses[:5]  # Return top 5 courses
    
    def parse_multiple(self, urls: List[str]) -> List[Dict]:
        """Parse multiple schools"""
        logger.info(f"🚀 Запуск парсера онлайн-школ...")
        
        for url in urls:
            try:
                data = self.parse_school(url)
                if data:
                    self.schools_data.append(data)
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
        
        logger.info(f"✅ Обработано: {len(self.schools_data)} школ")
        return self.schools_data
