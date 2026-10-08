\# 🛒 IntelliCart — Agentic AI Shopping Assistant



IntelliCart is an \*\*Agentic AI-powered shopping assistant\*\* designed to help users make better purchasing decisions by autonomously researching products, comparing specifications, analyzing reviews, and generating personalized recommendations.



Instead of simply returning search results, IntelliCart uses a multi-agent workflow to understand the user's requirements, retrieve relevant products, analyze reviews, generate recommendations, and maintain conversation context.



\---



\## 🎯 Project Objective



The objective of IntelliCart is to develop an intelligent shopping assistant that can:



\* Understand natural-language shopping requirements

\* Research products from available sources

\* Compare product specifications and prices

\* Analyze product reviews

\* Recommend products based on user preferences and budget

\* Provide personalized purchasing suggestions

\* Support budget-aware upselling and cross-selling

\* Consider promotions and offers

\* Maintain conversation context across interactions

\* Provide a structured backend through REST APIs



\---



\## ✨ Key Features



\### 🤖 Agentic AI Workflow



IntelliCart uses multiple specialized AI agents that work together rather than relying on a single chatbot response.



\### 🔍 Product Research



The system can retrieve product information and research available products based on the user's requirements.



\### ⚖️ Product Comparison



Products can be compared using factors such as:



\* Price

\* Specifications

\* Performance

\* Ratings

\* Features

\* Value for money



\### ⭐ Review Analysis



The Review Analysis Agent processes available product reviews and identifies useful information such as:



\* Positive aspects

\* Negative aspects

\* Overall sentiment

\* Important user feedback



\### 🎯 Personalized Recommendations



Recommendations consider factors such as:



\* Budget

\* Brand preference

\* Product category

\* Intended usage

\* User priorities

\* Deal breakers



\### 💰 Upselling \& Cross-Selling



IntelliCart can identify opportunities for:



\* Budget-aware upgrades

\* Complementary products

\* Relevant accessories

\* Promotions and offers



The system aims to keep recommendations relevant to the user's requirements and budget.



\### 🧠 Conversation Memory



The system includes memory functionality to maintain relevant information from the user's shopping conversation.



\### 🛡️ Guardrails



User queries are validated before being processed by the agentic workflow.



\### 📊 Observability



OpenTelemetry is integrated into the backend to provide visibility into the execution of the agent workflow.



\---



\# 🧠 Agentic AI Architecture



IntelliCart follows a multi-agent architecture.



```text

&#x20;                        User Query

&#x20;                             │

&#x20;                             ▼

&#x20;                   ┌──────────────────┐

&#x20;                   │    Guardrails    │

&#x20;                   └────────┬─────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌──────────────────┐

&#x20;                   │   Intent Agent   │

&#x20;                   └────────┬─────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                ┌───────────────────────┐

&#x20;                │ Product Retrieval     │

&#x20;                │       Agent           │

&#x20;                └───────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                ┌───────────────────────┐

&#x20;                │ Review Analysis       │

&#x20;                │       Agent           │

&#x20;                └───────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                ┌───────────────────────┐

&#x20;                │ Recommendation Agent  │

&#x20;                └───────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌──────────────────┐

&#x20;                   │   Memory Agent   │

&#x20;                   └────────┬─────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                      Final Response

```



The \*\*Orchestrator Agent\*\* coordinates the complete workflow and handles communication between the specialized agents.



\---



\# 🤖 AI Agents



| Agent                   | Responsibility                               |

| ----------------------- | -------------------------------------------- |

| Intent Agent            | Understands the user's shopping requirements |

| Product Retrieval Agent | Retrieves relevant product information       |

| Review Analysis Agent   | Analyzes product reviews                     |

| Recommendation Agent    | Generates personalized recommendations       |

| Memory Agent            | Maintains relevant conversation information  |

| Orchestrator Agent      | Coordinates the complete agentic workflow    |



\---



\# 🛠️ Tools



The project contains specialized tools supporting the agents.



\### Product \& Web Research



\* Web search

\* Product scraping

\* Review scraping

\* Product comparison



\### Database



\* Product retrieval

\* Review storage

\* Recommendation storage

\* User/session information



\### Recommendation



\* Recommendation generation

\* Selling strategy

\* Memory handling



\### Safety



\* Query validation

\* Guardrail processing



\---



\# 💻 Technology Stack



\### Backend



\* \*\*Python\*\*

\* \*\*FastAPI\*\*

\* \*\*Uvicorn\*\*

\* \*\*SQLAlchemy\*\*

\* \*\*PostgreSQL\*\*



\### Agentic AI



\* \*\*Agno\*\*

\* \*\*NVIDIA NIM\*\*

\* \*\*Meta Llama 3.3 70B Instruct\*\*



\### Frontend



\* \*\*Streamlit\*\*



\### Web Research



\* \*\*DDGS\*\*

\* \*\*BeautifulSoup\*\*

\* \*\*Requests\*\*



\### Observability



\* \*\*OpenTelemetry\*\*

\* \*\*OTLP\*\*

\* \*\*Aspire Dashboard\*\*



\### Deployment \& Development



\* \*\*Docker\*\*

\* \*\*Docker Compose\*\*

\* \*\*Git\*\*

\* \*\*GitHub\*\*



\---



\# 📁 Project Structure



```text

IntelliCart/

│

├── app/

│   ├── agents/

│   │   ├── intent\_agent.py

│   │   ├── memory\_agent.py

│   │   ├── orchestrator\_agent.py

│   │   ├── product\_retrieval\_agent.py

│   │   ├── recommendation\_agent.py

│   │   └── review\_analysis\_agent.py

│   │

│   ├── routes/

│   │   ├── chat\_routes.py

│   │   ├── conversation\_history\_routes.py

│   │   ├── cross\_sell\_routes.py

│   │   ├── product\_routes.py

│   │   ├── promotion\_routes.py

│   │   ├── recommendation\_routes.py

│   │   ├── review\_routes.py

│   │   ├── search\_history\_routes.py

│   │   ├── session\_routes.py

│   │   └── upsell\_routes.py

│   │

│   ├── tools/

│   │   ├── comparison\_tool.py

│   │   ├── database\_tool.py

│   │   ├── guardrail\_tool.py

│   │   ├── memory\_tool.py

│   │   ├── product\_scraper\_tool.py

│   │   ├── recommendation\_tool.py

│   │   ├── review\_scraper\_tool.py

│   │   ├── review\_tool.py

│   │   ├── selling\_strategy\_tool.py

│   │   └── web\_search\_tool.py

│   │

│   ├── database.py

│   ├── models.py

│   ├── schemas.py

│   ├── telemetry.py

│   └── main.py

│

├── Dockerfile

├── docker-compose.yaml

├── requirements.txt

├── streamlit\_app.py

├── .gitignore

└── README.md

```



\---



\# 🔌 API Endpoints



The FastAPI backend provides endpoints for different IntelliCart operations.



| Endpoint                | Purpose                              |

| ----------------------- | ------------------------------------ |

| `/products`             | Product management                   |

| `/reviews`              | Review management                    |

| `/recommendations`      | Recommendation management            |

| `/promotions`           | Promotion management                 |

| `/cross-sell`           | Cross-selling functionality          |

| `/upsell`               | Upselling functionality              |

| `/sessions`             | User session management              |

| `/search-history`       | Search history                       |

| `/conversation-history` | Conversation history                 |

| `/chat`                 | IntelliCart conversational interface |



FastAPI automatically provides interactive API documentation through Swagger UI.



After starting the backend, open:



```text

http://127.0.0.1:8000/docs

```



\---



\# ⚙️ Installation



\## 1. Clone the repository



```bash

git clone https://github.com/anfy3/IntelliCart.git

cd IntelliCart

```



\## 2. Create a virtual environment



\### Windows



```bash

python -m venv venv

venv\\Scripts\\activate

```



\### macOS / Linux



```bash

python3 -m venv venv

source venv/bin/activate

```



\## 3. Install dependencies



```bash

pip install -r requirements.txt

```



\---



\# 🔐 Environment Variables



Create a `.env` file in the project root.



```env

NVIDIA\_API\_KEY=your\_nvidia\_api\_key\_here

DATABASE\_URL=your\_database\_connection\_string

```



\*\*Never commit the `.env` file or API keys to GitHub.\*\*



The `.gitignore` file is configured to prevent sensitive environment files from being committed.



\---



\# 🚀 Running the Backend



Start the FastAPI application using:



```bash

uvicorn app.main:app --reload

```



The backend will be available at:



```text

http://127.0.0.1:8000

```



Swagger API documentation:



```text

http://127.0.0.1:8000/docs

```



\---



\# 🖥️ Running the Streamlit Interface



Run:



```bash

streamlit run streamlit\_app.py

```



Streamlit will provide the local URL for the IntelliCart user interface.



\---



\# 🐳 Running with Docker



Build and start the services using:



```bash

docker compose up --build

```



To stop the services:



```bash

docker compose down

```



\---



\# 📊 Observability



IntelliCart integrates \*\*OpenTelemetry\*\* to monitor the execution of the agentic workflow.



Tracing can provide visibility into operations such as:



```text

User Query

&#x20;   ↓

Guardrail Validation

&#x20;   ↓

Intent Agent

&#x20;   ↓

Product Retrieval Agent

&#x20;   ↓

Review Analysis Agent

&#x20;   ↓

Recommendation Agent

&#x20;   ↓

Memory Agent

&#x20;   ↓

Final Response

```



This makes it easier to understand agent execution and identify failures or performance issues.



\---



\# 🔄 Example Workflow



Example user query:



> "Suggest a Samsung phone under ₹50,000 for gaming with a good camera."



The system can process the request through the following stages:



\### 1. Intent Understanding



The Intent Agent identifies:



```text

Category: Smartphone

Brand: Samsung

Budget: ₹50,000

Usage: Gaming

Priority: Camera + Performance

```



\### 2. Product Retrieval



Relevant Samsung products are retrieved using the available research tools.



\### 3. Review Analysis



Available review information is analyzed to identify important user feedback.



\### 4. Recommendation



The Recommendation Agent evaluates the products based on the user's requirements.



\### 5. Memory



Relevant conversation information can be retained for future interactions.



\### 6. Final Recommendation



The user receives a structured recommendation explaining why the selected product fits their requirements.



\---



\# 🎓 Internship Project



\*\*Project:\*\* IntelliCart — Agentic AI Shopping Assistant



\*\*Domain:\*\* Artificial Intelligence / Agentic AI / Web Development



\*\*Technologies:\*\* Python, FastAPI, Agno, NVIDIA NIM, PostgreSQL, Streamlit, Docker, OpenTelemetry



The project was developed as part of an internship to explore the practical implementation of \*\*multi-agent AI systems for personalized e-commerce assistance\*\*.



\---



\# 🔮 Future Enhancements



Potential future improvements include:



\* More extensive product sources

\* Improved personalization

\* Advanced user preference memory

\* More sophisticated product ranking

\* Better price tracking

\* Real-time price and availability monitoring

\* Additional e-commerce integrations

\* Improved recommendation explanations

\* Enhanced observability dashboards

\* Production deployment



\---



\# 📌 Project Status



🚧 \*\*Active Development\*\*



IntelliCart is being developed as an Agentic AI shopping assistant with a modular multi-agent architecture.



\---



\## 👩‍💻 Author



\*\*Anfy Sony\*\*



B.Tech Computer Science

VIT Vellore



GitHub: https://github.com/anfy3



