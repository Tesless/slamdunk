from fastapi import FastAPI, Request, responses
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return """
        <html>
            <head>
                <title>GUI TEST_SLAMDUNK</title>
            </head>
            <body>
                <h1>Welcome to SLAMDUNK TEST</h1>
                    <form method="post" action="/button/a">
                        <button type="submit">아침인사</button>
                    </form>
                    <form method="post" action="/button/b">
                        <button type="submit">저녁인사</button>
                    </form>
            </body>
        </html>
    """

@app.post("/button/{button_name}")
def button_click(button_name: str):
    print(button_name)
    # if button_name == "a":
    #     subprocess.run(["echo", "안녕하세요"])
        
    # elif button_name == "b":
    #     subprocess.run(["echo", "안녕히가세요"])
    # else:
    #     return {"error": "Invalid button name"}

    return responses.RedirectResponse(url="/", status_code=303)