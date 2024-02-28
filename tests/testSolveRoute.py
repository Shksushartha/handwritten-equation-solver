from main import app

def testSolveRouteCase1():
    with app.test_client() as c:
        response = c.post("/solve", json={
            "equation": [
                "x+3y=18",
                "2x+y=11"
            ]
        })
        expectedResult = {'result': 'The values are: [3.][5.]'}
        jsonResponse = response.get_json()
        assert jsonResponse == expectedResult
        assert response.status_code == 200

def testSolveRouteCase2():
    with app.test_client() as c:
        response = c.post("/solve", json={
            "equation": [
                "x+3y+5z=18",
                "2x+y+z=11",
                "3x+y+z=12"
            ]
        })
        expectedResult = {'result': 'The values are: [1.][14.][-5.]'}
        jsonResponse = response.get_json()
        assert jsonResponse == expectedResult
        assert response.status_code == 200

def testSolveRouteCase3():
    with app.test_client() as c:
        response = c.post("/solve", json={
            "equation": [
                "x+3y+5z=18",
                "2x+y+z=11"
            ]
        })
        expectedResult = {"error": "Last 2 dimensions of the array must be square"}
        jsonResponse = response.get_json()
        assert jsonResponse == expectedResult

def testSolveRouteCase4():
    with app.test_client() as c:
        response = c.post("/solve", json={
            "equation": [
                "2x2+4x-18=0(3)"
            ]
        })
        expectedResult = {
            "result": "The root is 2.1623"
        }
        jsonResponse = response.get_json()
        assert jsonResponse == expectedResult
        assert response.status_code == 200

def testSolveRouteCase5():
    with app.test_client() as c:
        response = c.post("/solve", json={
            "equation": [
                "(3*(5+3/3))"
            ]
        })
        expectedResult = {
            "result": "18.0"
        }
        jsonResponse = response.get_json()
        assert jsonResponse == expectedResult
        assert response.status_code == 200



