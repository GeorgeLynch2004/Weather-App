from flask import Flask, render_template, request, redirect, url_for
import python_weather
import asyncio
import os
import tracemalloc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Key'

tracemalloc.start()

@app.route("/", methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        location = request.form.get("location")
        return redirect(url_for('weather', location=location))
    
    return render_template('index.html')

@app.route("/<location>", methods=['GET', 'POST'])
async def weather(location):
    if request.method == "POST":
        location = request.form.get("location")
        
    if location == None:
        location = "Cardiff"
    
    weather = await get_weather(location)
    
    return render_template("weather.html", location=location, weather=weather)

async def get_weather(location):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(location)
    return weather

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.run(debug=True)

