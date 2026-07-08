import requests
import time

url = "http://192.168.1.27:8000/api/chat"
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "http://192.168.1.27:8000",
    "Referer": "http://192.168.1.27:8000/",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

payload_file = "/home/erpuser/rag-server/questions.txt"

def main():
    try:
        with open(payload_file, 'r', encoding='utf-8') as f:
            for line in f:
                query = line.strip()
                if not query:
                    continue  # Skip empty lines
                
                # Construct the payload for this line
                payload = {
                    "message": query,
                    "role": "principal",
                    "office_id": 1,
                    "session_id": "s-1783428714137-v7l2ev"
                }
                
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=10)
                    
                    # Try to parse the response as JSON
                    try:
                        resp_json = response.json()
                        reply_message = resp_json.get("message", "No message field in response")
                        report_url = resp_json.get("report_url")
                        
                        print(f"\n[{response.status_code}] Query: {query}")
                        print(f"  -> Reply: {reply_message}")
                        if report_url:
                            print(f"  -> Link : {report_url}")
                        print("-" * 60)
                        
                    except ValueError:
                        # Fallback if response is not valid JSON
                        print(f"[{response.status_code}] Query: {query}")
                        print(f"  -> Raw Response: {response.text}")
                        print("-" * 60)

                except requests.exceptions.RequestException as e:
                    print(f"[ERROR] Query: {query}")
                    print(f"  -> Request failed: {e}")
                    print("-" * 60)
                
                # Optional: sleep to avoid rate limiting
                time.sleep(3)
                
    except FileNotFoundError:
        print(f"Error: The file {payload_file} was not found.")
    except KeyboardInterrupt:
        print("Script interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()