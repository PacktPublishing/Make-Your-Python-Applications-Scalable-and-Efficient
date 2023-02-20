from locust import FastHttpUser, task


class FibonacciTest(FastHttpUser):
    @task
    def fibonacci(self):
        self.client.get("/fibonacci/")
