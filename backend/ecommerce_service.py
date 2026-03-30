import httpx
from typing import List, Dict, Optional
from urllib.parse import quote_plus
import asyncio


class EcommerceSearcher:
    """Search for products on various e-commerce platforms"""
    
    def __init__(self):
        self.timeout = httpx.Timeout(10.0)
    
    async def search_amazon(
        self,
        query: str,
        limit: int = 5,
    ) -> List[Dict]:
        """
        Search Amazon for products.
        Note: This uses the public search page. For production, use Amazon Product Advertising API.
        """
        try:
            # Build search URL
            encoded_query = quote_plus(query)
            url = f"https://www.amazon.in/s?k={encoded_query}"
            
            # Headers to mimic browser
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers, follow_redirects=True)
                
                # For now, return search links
                # In production, parse HTML or use official API
                return [{
                    "title": f"Search results for '{query}' on Amazon",
                    "url": url,
                    "source": "amazon",
                    "price": None,
                    "image": None,
                }]
                
        except Exception as e:
            print(f"Amazon search error: {e}")
            return []
    
    async def search_flipkart(
        self,
        query: str,
        limit: int = 5,
    ) -> List[Dict]:
        """Search Flipkart for products"""
        try:
            encoded_query = quote_plus(query)
            url = f"https://www.flipkart.com/search?q={encoded_query}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers, follow_redirects=True)
                
                return [{
                    "title": f"Search results for '{query}' on Flipkart",
                    "url": url,
                    "source": "flipkart",
                    "price": None,
                    "image": None,
                }]
                
        except Exception as e:
            print(f"Flipkart search error: {e}")
            return []
    
    async def search_myntra(
        self,
        query: str,
        limit: int = 5,
    ) -> List[Dict]:
        """Search Myntra for fashion products"""
        try:
            encoded_query = quote_plus(query)
            url = f"https://www.myntra.com/{encoded_query.replace('+', '-')}?rawQuery={encoded_query}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers, follow_redirects=True)
                
                return [{
                    "title": f"Search results for '{query}' on Myntra",
                    "url": url,
                    "source": "myntra",
                    "price": None,
                    "image": None,
                }]
                
        except Exception as e:
            print(f"Myntra search error: {e}")
            return []
    
    async def search_all(
        self,
        query: str,
        limit_per_source: int = 3,
    ) -> Dict[str, List[Dict]]:
        """Search all platforms concurrently"""
        results = await asyncio.gather(
            self.search_amazon(query, limit_per_source),
            self.search_flipkart(query, limit_per_source),
            self.search_myntra(query, limit_per_source),
            return_exceptions=True,
        )
        
        return {
            "amazon": results[0] if not isinstance(results[0], Exception) else [],
            "flipkart": results[1] if not isinstance(results[1], Exception) else [],
            "myntra": results[2] if not isinstance(results[2], Exception) else [],
        }
    
    def generate_affiliate_links(
        self,
        outfit_name: str,
        colors: List[str],
    ) -> Dict[str, str]:
        """Generate affiliate search links for an outfit"""
        # Build search query
        color_str = " ".join(colors[:2]) if colors else ""
        query = f"{color_str} {outfit_name}".strip()
        
        encoded = quote_plus(query)
        
        return {
            "amazon": f"https://www.amazon.in/s?k={encoded}",
            "flipkart": f"https://www.flipkart.com/search?q={encoded}",
            "myntra": f"https://www.myntra.com/{encoded.replace('+', '-')}",
        }


# Singleton instance
_searcher = None


def get_ecommerce_searcher() -> EcommerceSearcher:
    global _searcher
    if _searcher is None:
        _searcher = EcommerceSearcher()
    return _searcher
