from security.pyjwt_generator import PyJWTGenerator

def fake_time_getter() -> float:
  return 12345

def test_pyjwt_with_specific_payloads():
  jwt_generator = PyJWTGenerator("foo", "bar")
  jwt_generator.time_getter = fake_time_getter

  access_token = jwt_generator.generate_access_token(1, "johndoe")
  assert access_token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpvaG5kb2UiLCJpYXQiOjEyMzQ1fQ.kcaR3p4IO84q_UdUBt_e8WWg01K5k6ZgshTlZTsjS8A"

  refresh_token = jwt_generator.generate_refresh_token(2, "janedoe")
  assert refresh_token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImphbmVkb2UiLCJpYXQiOjEyMzQ1fQ.gW_G9gAX4UHoAoIgfDtcnt3SId7T97ugOQm4nT7ScVM"
