import os
import csv
import json
import xml.etree.ElementTree as ET
import asyncio
import logging
from collections import deque
from typing import List, Dict, Any, Union, AsyncGenerator
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class Membrane:
    """
    Ingests and standardizes data from files or online sources.
    Attaches context and streams data.
    """
    def __init__(self, data_source: str = "data.json"):
        self.data_source = data_source
        self.clients = set()

    async def initialize(self):
        logger.info("Membrane initialized.")

    async def ingest_data(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.data_source):
            ext = os.path.splitext(self.data_source)[-1].lower()
            if ext == ".json":
                return self.load_json()
            elif ext == ".csv":
                return self.load_csv()
            elif ext == ".xml":
                return self.load_xml()
            elif ext == ".txt":
                return self.load_txt()
            else:
                return self.load_txt()
        else:
            return await self.fetch_online_data(self.data_source)

    def load_json(self) -> List[Dict[str, Any]]:
        try:
            with open(self.data_source, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else [data]
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            return

    def load_csv(self) -> List[Dict[str, Any]]:
        data =
        try:
            with open(self.data_source, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(dict(row))
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
        return data

    def load_xml(self) -> List[Dict[str, Any]]:
        try:
            tree = ET.parse(self.data_source)
            root = tree.getroot()
            return [{elem.tag: elem.text for elem in child} for child in root]
        except Exception as e:
            logger.error(f"Error parsing XML: {e}")
            return

    def load_txt(self) -> List[Dict[str, Any]]:
        data =
        try:
            with open(self.data_source, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f.readlines()):
                    if line.strip():
                        data.append({"line": idx + 1, "content": line.strip()})
        except Exception as e:
            logger.error(f"Error reading TXT: {e}")
        return data

    async def fetch_online_data(self, url: str) -> List[Dict[str, Any]]:
        logger.info(f"Fetching online data from {url}...")
        try:
            visited = set()
            queue = deque([url])
            data =
            async with aiohttp.ClientSession() as session:
                while queue:
                    current_url = queue.popleft()
                    if current_url in visited:
                        continue
                    visited.add(current_url)
                    async with session.get(current_url) as response:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        paragraphs = soup.find_all("p")
                        for idx, p in enumerate(paragraphs):
                            text = p.get_text(strip=True)
                            if text:
                                data.append({"line": idx + 1, "content": text, "source": current_url})
                        # Extract links and add them to the queue
                        links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http")]
                        queue.extend(links)
            return data
        except Exception as e:
            logger.error(f"Error fetching online data: {e}")
            return

    def parse_universal(self, raw: Union[str, bytes, Dict, List]) -> List[Dict[str, Any]]:
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="ignore")
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict):
                    return [parsed]
            except Exception:
                return [{"content": line} for line in raw.splitlines() if line.strip()]
        if isinstance(raw, dict):
            return [raw]
        if isinstance(raw, list):
            return [item if isinstance(item, dict) else {"content": str(item)} for item in raw]
        return

    async def stream_data(self) -> AsyncGenerator[Dict[str, Any], None]:
        raw_data = await self.ingest_data()
        parsed_data = self.parse_universal(raw_data)
        for chunk in parsed_data:
            # Attach a context snippet (first 50 characters)
            content = chunk.get("content", "")
            chunk["context"] = content[:50] if isinstance(content, str) else ""
            yield chunk
            await asyncio.sleep(0.1)

    async def stream_updates(self, websocket):
        await websocket.accept()
        self.clients.add(websocket)
        try:
            async for chunk in self.stream_data():
                await websocket.send_json(chunk)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            self.clients.remove(websocket)

    async def ingest_and_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder: process the provided data (e.g., add to a queue)
        logger.info("Ingesting data...")
        return {"status": "ingested", "data": data}

    async def save_state(self):
        logger.info("State saved (placeholder).")
