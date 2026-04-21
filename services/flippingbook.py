import time
import requests
from config.settings import FLIPPINGBOOK_API_KEY, FLIPPINGBOOK_API_URL

class FlippingBookService:
    def __init__(self):
        self.api_key = FLIPPINGBOOK_API_KEY
        self.base_url = FLIPPINGBOOK_API_URL
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def publish(self, drive_file_id: str, title: str) -> str:
        from services.drive import DriveService
        pdf_bytes = DriveService().download_file(drive_file_id)
        doc_id = self._upload_pdf(pdf_bytes, title)
        return self._wait_for_publish(doc_id)

    def _upload_pdf(self, pdf_bytes: bytes, title: str) -> str:
        files = {"file": (f"{title}.pdf", pdf_bytes, "application/pdf")}
        resp = requests.post(f"{self.base_url}/publications", headers=self.headers, files=files, data={"title": title}, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        doc_id = result.get("publication", {}).get("id") or result.get("id")
        if not doc_id:
            raise ValueError(f"FlippingBook error: {result}")
        return doc_id

    def _wait_for_publish(self, doc_id: str, timeout: int = 60) -> str:
        deadline = time.time() + timeout
        while time.time() < deadline:
            resp = requests.get(f"{self.base_url}/publications/{doc_id}", headers=self.headers, timeout=15)
            resp.raise_for_status()
            pub = resp.json().get("publication", {})
            if pub.get("status") in ("published", "ready") and pub.get("link"):
                return pub["link"]
            if pub.get("status") == "error":
                raise ValueError(f"FlippingBook failed: {pub}")
            time.sleep(3)
        raise TimeoutError(f"FlippingBook not ready after {timeout}s")
