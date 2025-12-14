"""
SEC EDGAR API Client for downloading and parsing 10-K reports
"""
import os
import re
import json
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from sec_edgar_downloader import Downloader


class SecEdgarClient:
    """
    Client for downloading and parsing SEC EDGAR 10-K reports
    """
    
    def __init__(self, user_agent: str = "finsight-ai@example.com"):
        self.user_agent = user_agent
        self.downloader = Downloader(user_agent, "data/raw")
        self.cache_dir = "data/raw"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_ticker_to_cik(self, ticker: str) -> Optional[str]:
        """
        Convert ticker symbol to CIK (Central Index Key)
        Uses SEC's company tickers JSON
        """
        cache_path = os.path.join(self.cache_dir, "ticker_cik_map.json")
        ticker_upper = ticker.upper()
        
        # Load or fetch ticker-CIK mapping
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    ticker_map = json.load(f)
                    cik = ticker_map.get(ticker_upper)
                    if cik:
                        return cik
                    # If not found, refresh cache
                    print(f"Ticker {ticker_upper} not in cache, refreshing...")
            except Exception as e:
                print(f"Warning: Could not load ticker-CIK cache: {e}")
        
        # Fetch from SEC (always refresh to get latest data)
        try:
            url = "https://www.sec.gov/files/company_tickers.json"
            response = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Convert to ticker -> CIK mapping
            ticker_map = {}
            for entry in data.values():
                if 'ticker' in entry and 'cik_str' in entry:
                    ticker_map[entry['ticker'].upper()] = str(entry['cik_str']).zfill(10)
            
            # Save cache
            try:
                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(ticker_map, f, indent=2)
                print(f"Updated ticker-CIK mapping cache with {len(ticker_map)} entries")
            except Exception as e:
                print(f"Warning: Could not save cache: {e}")
            
            cik = ticker_map.get(ticker_upper)
            if not cik:
                print(f"Warning: Ticker {ticker_upper} not found in SEC database")
            return cik
        except Exception as e:
            print(f"Warning: Could not fetch ticker-CIK mapping: {e}")
            # Try to use cached data even if refresh failed
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, 'r', encoding='utf-8') as f:
                        ticker_map = json.load(f)
                        return ticker_map.get(ticker_upper)
                except Exception:
                    pass
            return None
    
    def download_10k_direct(self, ticker: str) -> Optional[str]:
        """
        Download 10-K directly from SEC EDGAR API (alternative method)
        Returns: Path to downloaded file
        """
        cik = self.get_ticker_to_cik(ticker)
        if not cik:
            raise ValueError(f"Could not find CIK for ticker {ticker}. This ticker may not be registered with the SEC, or the ticker-CIK mapping needs to be refreshed.")
        
        # Remove leading zeros from CIK for API
        cik_clean = str(int(cik))
        print(f"Downloading 10-K for {ticker} (CIK: {cik_clean})...")
        
        try:
            # Get company filings from SEC API
            filings_url = f"https://data.sec.gov/submissions/CIK{cik_clean.zfill(10)}.json"
            headers = {
                "User-Agent": self.user_agent,
                "Accept": "application/json"
            }
            
            response = requests.get(filings_url, headers=headers, timeout=15)
            response.raise_for_status()
            company_data = response.json()
            
            # Find 10-K filings
            filings = company_data.get('filings', {}).get('recent', {})
            forms = filings.get('form', [])
            filing_dates = filings.get('filingDate', [])
            accession_numbers = filings.get('accessionNumber', [])
            
            # Find the most recent 10-K
            ten_k_indices = [i for i, form in enumerate(forms) if form == '10-K']
            if not ten_k_indices:
                # Check if there are any filings at all
                if not forms:
                    raise FileNotFoundError(f"No filings found for {ticker} (CIK: {cik_clean}). The company may not have filed any reports with the SEC.")
                # List available forms for debugging
                available_forms = set(forms[:20])  # First 20 forms
                raise FileNotFoundError(f"No 10-K filings found for {ticker} (CIK: {cik_clean}). Available forms: {', '.join(sorted(available_forms))}")
            
            # Get the most recent 10-K
            latest_index = ten_k_indices[0]
            accession = accession_numbers[latest_index].replace('-', '')
            filing_date = filing_dates[latest_index]
            
            # Construct the URL for the 10-K filing
            # Format: https://www.sec.gov/Archives/edgar/data/{CIK}/{accession}/filename
            # First, get the filing index to find the actual HTML file
            index_url = f"https://www.sec.gov/Archives/edgar/data/{cik_clean}/{accession}/index.json"
            index_response = requests.get(index_url, headers=headers, timeout=15)
            index_response.raise_for_status()
            index_data = index_response.json()
            
            # Try to find a .txt version first (plain text 10-K is ideal)
            txt_file = None
            for file_info in index_data.get('directory', {}).get('item', []):
                name = file_info.get('name', '')
                if name.endswith('.txt') and '10k' in name.lower():
                    txt_file = name
                    break
            
            # If .txt found, download it instead of HTML
            if txt_file:
                html_file = txt_file
            else:
                # Find the 10-K HTML file (prefer the main document, not small metadata files)
                html_files = []
                for file_info in index_data.get('directory', {}).get('item', []):
                    name = file_info.get('name', '')
                    size = file_info.get('size', 0)
                    desc = file_info.get('description', '') or ''
                    # Normalize
                    name_l = name.lower()
                    desc_l = desc.lower()

                    # Skip obvious metadata / index / XBRL files
                    if any(skip in name_l for skip in ['index', 'cover', 'summary', 'document_', 'c99999']):
                        continue
                    # Skip files that are XBRL/XML or IDEA generated (these are noisy)
                    if 'xbrl' in desc_l or 'idea' in desc_l or name_l.startswith('r') and re.match(r'^r\d+', name_l):
                        continue

                    if (name.endswith('.htm') or name.endswith('.html')):
                        # Only consider files > 50KB (small files are metadata)
                        try:
                            size_int = int(size)
                            if size_int >= 50000:
                                html_files.append((name, size_int))
                        except (ValueError, TypeError):
                            # If size is not an integer, still consider the file
                            html_files.append((name, 0))
                
                # Sort by size descending (larger files are usually main documents)
                html_files.sort(key=lambda x: x[1], reverse=True)
                
                # If no large files found, try any HTML/HTM file but avoid XBRL/IDEA files
                if not html_files:
                    for file_info in index_data.get('directory', {}).get('item', []):
                        name = file_info.get('name', '')
                        desc = file_info.get('description', '') or ''
                        name_l = name.lower()
                        desc_l = desc.lower()
                        if (name.endswith('.htm') or name.endswith('.html')) and 'index' not in name_l:
                            # Skip XBRL/IDEA generated files and files named like Rxx.htm
                            if 'xbrl' in desc_l or 'idea' in desc_l or re.match(r'^r\d+', name_l):
                                continue
                            html_files.append((name, file_info.get('size', 0)))
                
                html_file = html_files[0][0] if html_files else None
            
            if not html_file:
                raise FileNotFoundError(f"No HTML file found in 10-K filing for {ticker}")
            
            # Download the HTML file
            html_url = f"https://www.sec.gov/Archives/edgar/data/{cik_clean}/{accession}/{html_file}"
            html_response = requests.get(html_url, headers=headers, timeout=30)
            html_response.raise_for_status()
            
            # Save to cache
            save_dir = os.path.join(self.cache_dir, "sec-edgar-filings", ticker.upper(), "10-K", filing_date)
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, html_file)
            
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(html_response.text)
            
            return file_path
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to download 10-K from SEC API: {e}")
        except (KeyError, IndexError) as e:
            raise FileNotFoundError(f"Could not parse SEC filing data for {ticker}: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error downloading 10-K: {e}")
    
    def download_10k(self, ticker: str, num_filings: int = 1) -> Optional[str]:
        """
        Download the latest 10-K report for a ticker
        Tries direct API method first, then falls back to sec-edgar-downloader
        Returns: Path to downloaded file
        """
        cik = self.get_ticker_to_cik(ticker)
        if not cik:
            raise ValueError(f"Could not find CIK for ticker {ticker}")
        
        # Try direct API method first (more reliable)
        try:
            return self.download_10k_direct(ticker)
        except Exception as direct_error:
            print(f"Direct API download failed: {direct_error}, trying sec-edgar-downloader...")
        
        # Fallback to sec-edgar-downloader
        try:
            base_dir = os.path.join(self.cache_dir, "sec-edgar-filings")
            os.makedirs(base_dir, exist_ok=True)
            
            # Try with CIK (more reliable than ticker)
            try:
                self.downloader.get("10-K", cik, limit=1)
            except Exception:
                # Try with ticker
                try:
                    self.downloader.get("10-K", ticker, limit=1)
                except Exception as e:
                    raise RuntimeError(f"sec-edgar-downloader failed: {e}")
            
            # Wait for files to be written
            import time
            time.sleep(8)  # Increased wait time
            
            # Search for downloaded files
            possible_dirs = [
                os.path.join(base_dir, ticker.upper(), "10-K"),
                os.path.join(base_dir, ticker.lower(), "10-K"),
                os.path.join(base_dir, cik, "10-K"),
                os.path.join(base_dir, cik.zfill(10), "10-K"),
            ]
            
            target_dir = None
            for possible_dir in possible_dirs:
                if os.path.exists(possible_dir):
                    target_dir = possible_dir
                    break
            
            # Recursive search - improved to find any 10-K directory
            if not target_dir and os.path.exists(base_dir):
                # Search more thoroughly
                for root, dirs, files in os.walk(base_dir):
                    # Check if this directory contains 10-K
                    if '10-K' in root or '10K' in root:
                        # Check if there are subdirectories (filing dates)
                        subdirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
                        if subdirs:
                            target_dir = root
                            break
                
                # If still not found, try pattern matching
                if not target_dir:
                    for company_dir in Path(base_dir).iterdir():
                        if company_dir.is_dir():
                            # Check for 10-K in any subdirectory
                            for subdir in company_dir.rglob("10-K"):
                                if subdir.is_dir():
                                    subdirs = [d for d in subdir.iterdir() if d.is_dir()]
                                    if subdirs:
                                        target_dir = str(subdir)
                                        break
                            if target_dir:
                                break
            
            if not target_dir or not os.path.exists(target_dir):
                raise FileNotFoundError(f"No 10-K filings found for {ticker}")
            
            # Get the most recent filing
            filings = [f for f in Path(target_dir).iterdir() if f.is_dir()]
            if not filings:
                raise FileNotFoundError(f"No 10-K filing directories found")
            
            filings = sorted(filings, key=os.path.getmtime, reverse=True)
            latest_filing_dir = filings[0]
            
            # Find HTML file - improved search
            html_files = []
            
            # First, try direct files in the directory
            html_files = list(latest_filing_dir.glob("*.html"))
            if not html_files:
                html_files = list(latest_filing_dir.glob("*.htm"))
            
            # If not found, search recursively
            if not html_files:
                for html_file in latest_filing_dir.rglob("*.html"):
                    html_files.append(html_file)
                    break  # Take first found
                if not html_files:
                    for html_file in latest_filing_dir.rglob("*.htm"):
                        html_files.append(html_file)
                        break  # Take first found
            
            # If still not found, check subdirectories
            if not html_files:
                for subdir in latest_filing_dir.iterdir():
                    if subdir.is_dir():
                        html_files = list(subdir.glob("*.html"))
                        if not html_files:
                            html_files = list(subdir.glob("*.htm"))
                        if html_files:
                            break
                    elif subdir.suffix in ['.html', '.htm']:
                        html_files = [subdir]
                        break
            
            if html_files:
                # Filter out noisy XBRL/IDEA files (names like R36.htm) and prefer main documents
                def noisy(p):
                    try:
                        name = p.name.lower()
                        path_s = str(p).lower()
                        if re.match(r'^r\d+', name):
                            return True
                        if 'xbrl' in name or 'idea' in name or 'xbrl' in path_s:
                            return True
                        return False
                    except Exception:
                        return False

                filtered = [p for p in html_files if not noisy(p)]
                if filtered:
                    # Prefer files with 10-k in name if available
                    for p in filtered:
                        if '10-k' in p.name.lower() or '10k' in p.name.lower():
                            return str(p)
                    # Otherwise return the largest file by size
                    filtered_sorted = sorted(filtered, key=lambda p: p.stat().st_size if p.exists() else 0, reverse=True)
                    return str(filtered_sorted[0])

                # If all files are noisy, fall back to first one
                return str(html_files[0])
            
            raise FileNotFoundError(f"No HTML file found in {latest_filing_dir}")
            
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to download 10-K for {ticker}: {e}")
    
    def parse_10k_html(self, html_path: str) -> Dict[str, str]:
        """
        Parse 10-K HTML file and extract structured text
        Returns: Dictionary with sections (Item 1, Item 1A, etc.)
        """
        try:
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"Could not read HTML file: {e}")
        # Use BeautifulSoup to extract visible text and preserve some structure
        soup = BeautifulSoup(content, 'lxml')

        # Remove scripts, styles and comments
        for elem in soup(['script', 'style']):
            elem.decompose()
        for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.original_encoding))):
            pass

        # Get visible text with line breaks for heading detection
        text = '\n'.join([line.strip() for line in soup.get_text(separator='\n').splitlines() if line.strip()])

        # Stronger XBRL/IDEA noise removal up-front
        lines = []
        for line in text.split('\n'):
            low = line.lower()
            # Skip obvious XBRL/IDEA metadata lines or file listing lines
            if any(token in low for token in ['xbrl', 'idea:', 'document>', 'file:', '<text>', 'xml', 'schema', 'accession', 'sequence', 'filename', 'sec-']):
                continue
            # Skip lines that look like file names (e.g., r36.htm) or html doc markers
            if re.match(r'^[rR]\d+\.htm', low) or re.match(r'^[a-z0-9_\-]{1,20}\.(htm|html|xml|txt)$', low):
                continue
            # Skip very short lines or header noise
            if len(low) < 30 and low.isupper():
                continue
            lines.append(line)

        cleaned_text = '\n'.join(lines)

        # Attempt to split document by 'Item' headings (Item 1, Item 1A, etc.)
        sections: Dict[str, str] = {}

        # Find all item headings and their positions with improved pattern
        # Pattern matches: "Item 1. Business" or "ITEM 1. Business" or "Item 1. " followed by content
        item_pattern = r'\b[Ii]tem\s+(\d+[A-Za-z]?)[.\s]+([^\n]{10,})'
        item_matches = list(re.finditer(item_pattern, cleaned_text, flags=re.IGNORECASE))
        
        if item_matches and len(item_matches) > 0:
            # Extract content between Items
            for i, match in enumerate(item_matches):
                item_id = match.group(1).strip()  # e.g., "7A"
                item_title = match.group(2).strip()  # e.g., "Quantitative and Qualitative..."
                start_pos = match.start()
                
                # Find where next Item starts
                if i + 1 < len(item_matches):
                    end_pos = item_matches[i + 1].start()
                else:
                    end_pos = len(cleaned_text)
                
                # Extract content (from Item line through end of section)
                item_section = cleaned_text[start_pos:end_pos].strip()
                
                # Clean: normalize whitespace, remove excessive metadata
                item_section_clean = re.sub(r'\s+', ' ', item_section)[:80000]
                
                key = f'Item {item_id.upper()}'
                if item_section_clean and len(item_section_clean) > 50:  # Only keep if substantial content
                    sections[key] = item_section_clean

        # If we didn't find clear items, try regex-based extraction for common items
        if not sections:
            section_patterns = {
                'Item 1': r'Item\s+1[\.\s]+Business\s+(.*?)(?=Item\s+1A|Item\s+2|$)',
                'Item 1A': r'Item\s+1A[\.\s]+Risk\s+Factors\s+(.*?)(?=Item\s+2|$)',
                'Item 7': r'Item\s+7[\.\s]+Management[\'\"]?s?\s+Discussion\s+(.*?)(?=Item\s+7A|Item\s+8|$)',
                'Item 7A': r'Item\s+7A[\.\s]+Quantitative\s+and\s+Qualitative\s+Disclosures\s+(.*?)(?=Item\s+8|$)',
                'Item 8': r'Item\s+8[\.\s]+Financial\s+Statements\s+(.*?)(?=Item\s+9|$)'
            }
            for name, pattern in section_patterns.items():
                m = re.search(pattern, cleaned_text, re.IGNORECASE | re.DOTALL)
                if m:
                    sections[name] = re.sub(r'\s+', ' ', m.group(1).strip())[:100000]

        # Final fallback: use cleaned_text as Full Document but trimmed
        if not sections:
            fallback = re.sub(r'\s+', ' ', cleaned_text)[:100000]
            sections['Full Document'] = fallback if fallback else re.sub(r'\s+', ' ', text)[:100000]

        return sections
    
    def get_10k_text(self, ticker: str) -> Dict[str, str]:
        """
        Download and parse 10-K report for a ticker
        Returns: Dict with 'sections' (parsed sections), 'full_text', and 'metadata'
        """
        # Check cache first
        cache_path = os.path.join(self.cache_dir, f"{ticker}_10k_parsed.json")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Try to download and parse
        try:
            html_path = self.download_10k(ticker)
            sections = self.parse_10k_html(html_path)
            
            # Extract full text from the HTML (for metadata tracking)
            try:
                with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(f.read(), 'lxml')
                    for elem in soup(['script', 'style']):
                        elem.decompose()
                    full_text = soup.get_text()
            except Exception:
                full_text = ' '.join(v for v in sections.values() if isinstance(v, str))
            
            # Create return structure
            result = {
                'sections': sections,
                'full_text': full_text,
                'metadata': {
                    'file_path': html_path,
                    'parsed_date': datetime.now().isoformat(),
                    'total_length': len(full_text) if full_text else 0
                }
            }
            
            # Save to cache
            try:
                with open(cache_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Warning: Could not save cache: {e}")
            
            return result
        except (FileNotFoundError, RuntimeError) as e:
            # Re-raise with clearer, shorter message (automatic-only; do not suggest manual upload)
            error_msg = str(e)
            if "No 10-K filings found" in error_msg:
                raise ValueError("Le téléchargement automatique du rapport 10-K a échoué : aucun filing 10-K trouvé pour ce ticker. Vérifiez le symbole boursier et la disponibilité des données.")
            else:
                raise ValueError(f"Le téléchargement automatique a échoué : {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la récupération du rapport 10-K: {str(e)}")




