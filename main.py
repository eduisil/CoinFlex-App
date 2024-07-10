from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

app = FastAPI()

# Montar archivos estáticos
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Agregar middleware para sesiones
app.add_middleware(SessionMiddleware, secret_key="tu_secreto_super_secreto")

templates = Jinja2Templates(directory="pages")

# Mock database
fake_users_db = {
    "sam": {
        "username": "sam",
        "full_name": "Admin user",
        "email": "admin@example.com",
        "hashed_password": "isil123",
        "disabled": False,
    },
}

# Función para verificar las credenciales del usuario
def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict
    return None

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user(fake_users_db, username)
    if not user or not verify_password(password, user['hashed_password']):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})
    
    request.session['username'] = username
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    username = request.session.get('username')
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    username = request.session.get('username')
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username})

@app.get("/mercados", response_class=HTMLResponse)
async def market_page(request: Request):
    username = request.session.get('username')
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("market.html", {"request": request, "username": username})

@app.get("/pagos", response_class=HTMLResponse)
async def bill_page(request: Request):
    username = request.session.get('username')
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("billing.html", {"request": request, "username": username})

@app.get("/perfil", response_class=HTMLResponse)
async def profil_page(request: Request):
    username = request.session.get('username')
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("profile.html", {"request": request, "username": username})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
