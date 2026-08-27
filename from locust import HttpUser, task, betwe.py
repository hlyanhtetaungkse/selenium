from locust import HttpUser, task, between, events, LoadTestShape
import os

class WebsiteUser(HttpUser):
    # Use FastHttpUser for very high concurrency if needed:
    # from locust import FastHttpUser as HttpUser
    wait_time = between(1, 3)  # seconds between tasks per user

    def on_start(self):
        # Example: authenticate once at start and store token for subsequent requests.
        # Uses environment variables for credentials (safer than hardcoding).
        username = os.getenv("LOADTEST_USER", "testuser")
        password = os.getenv("LOADTEST_PASS", "testpass")
        resp = self.client.post("/api/login", json={"username": username, "password": password})
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("access_token")
            if token:
                self.client.headers.update({"Authorization": f"Bearer {token}"})
        else:
            # If login fails, stop this user instance (optional)
            # raise StopUser()  # uncomment if you want to stop users that fail auth
            pass

    @task(3)
    def list_items(self):
        # example GET
        self.client.get("/api/items", name="/api/items")

    @task(1)
    def create_item(self):
        # example POST
        payload = {"title": "Load test item", "value": 123}
        self.client.post("/api/items", json=payload, name="/api/items")

    @task(2)
    def item_detail(self):
        # example hitting a parameterized endpoint
        item_id = 1
        self.client.get(f"/api/items/{item_id}", name="/api/items/[id]")

# Optional: define a custom load shape (stages). Remove if not needed.
class StagesShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 2},   # ramp to 10 users over 60s
        {"duration": 180, "users": 50, "spawn_rate": 5},  # ramp to 50 users
        {"duration": 300, "users": 200, "spawn_rate": 20},# ramp to 200 users
        {"duration": 360, "users": 0, "spawn_rate": 200}, # ramp down to 0 users
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
            run_time -= stage["duration"]
        return None