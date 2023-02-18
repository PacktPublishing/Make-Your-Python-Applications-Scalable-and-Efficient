from locust import FastHttpUser, task


class FibonacciDjangoTest(FastHttpUser):
    @task
    def fibonacci(self):
        self.client.get("/fibonacci/")
