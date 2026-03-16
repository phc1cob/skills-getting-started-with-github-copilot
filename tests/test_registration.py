from urllib.parse import quote


def test_signup_with_new_email_returns_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_with_existing_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_with_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Underwater Robotics"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_existing_participant_returns_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_non_member_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-in-club@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_then_unregister_same_student_succeeds(client):
    # Arrange
    activity_name = "Science Club"
    email = "flowtest@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )
    unregister_response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]
