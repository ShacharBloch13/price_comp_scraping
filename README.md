# price_comp_scraping
``` https://youtu.be/2oezjE9hr3I ```

This project features a full-stack application designed for web scraping and price comparison. It is comprised of a backend component built with Python for scraping and data handling, and a frontend component utilizing Next.js for a dynamic user interface.

# Technology Stack

1) FastAPI - for API handeling
2) Beautiful Soup and Selenium - web scraping
3) Next.js - React framework
4) Tailwind CSS - styling
5) TypeScript

# Prerequisites

To use the application, you need:
1) Python 3.8 or higher
2) Node.js 12.x or higher
3) npm (typically comes with Node.js)
4) An OpenAI API key (for reccomendation feature)
5) An updated ChromeDriver
6) next
7) react + reack-dom
8) teilwindcss
9) typescript @types/react @types/node
10) flask
11) requests
12) beautifulsoup4
13) selenium

# Installation Instructions and starting the program

1)  ``` git clone https://github.com/ShacharBloch13/price_comp_scraping/with_next.js ```
2) ``` cd backend ```
3) ```python main.py```
4) ``` cd .. ```
5) ``` cd frontend ```
6) ``` npm run dev ```

# Directory tree
```
├── .pytest_cache/
├── backend/
│   ├── .env
│   ├── main.py
│   ├── price_comparison_scraping.py
│   └── __pycache__/
├── frontend/
│   ├── .next/
│   ├── .eslintrc.json
│   ├── next.config.mjs
│   ├── package.json
│   ├── public/
│   └── pages/
│       ├── _app.js
│       └── index.js
```
# How to use
1) Start both the backend and frontend as described.
2) Access the frontend through your browser at http://localhost:3000 (default URL for Next.js apps).
3) Use the web interface to initiate scraping processes and view price comparisons.
4) Note - to get the reccoemendation for additional product, set your OPENAI API key in a .env file





   
   
   
