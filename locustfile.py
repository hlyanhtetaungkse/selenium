from locust import HttpUser, task, between

class SauceDemoUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def browse_site(self):
        self.client.get("/")
        self.client.get("/inventory")