from locust import HttpUser, task, between


class ClubUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # 1. Connexion (login du secrétaire de club)
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(2)
    def view_competitions(self):
        # 2. Consultation de la liste des compétitions
        self.client.get("/showSummary")

    @task(1)
    def book_places(self):
        # 3. Réservation de places
        self.client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift",
                "competition": "Spring Festival",
                "places": "1",
            },
        )

    @task(1)
    def view_points(self):
        # 4. Consultation du tableau des points
        self.client.get("/points")
